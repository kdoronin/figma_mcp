#!/usr/bin/env python3
"""WebSocket server for Figma plugin and MCP communication."""

import asyncio
import json
import logging
import websockets
from websockets.server import serve
from typing import Dict, Set, Any
import argparse
import signal
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Connected clients storage
clients: Set[websockets.WebSocketServerProtocol] = set()
channels: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}


async def register_client(websocket: websockets.WebSocketServerProtocol) -> None:
    """Register a new client connection."""
    clients.add(websocket)
    logger.info(f"Client connected from {websocket.remote_address}. Total clients: {len(clients)}")


async def unregister_client(websocket: websockets.WebSocketServerProtocol) -> None:
    """Unregister a client connection."""
    clients.discard(websocket)
    
    # Remove from all channels
    channels_to_remove = []
    for channel_name, channel_clients in channels.items():
        channel_clients.discard(websocket)
        if not channel_clients:  # Remove empty channels
            channels_to_remove.append(channel_name)
    
    for channel_name in channels_to_remove:
        del channels[channel_name]
        logger.info(f"Removed empty channel: {channel_name}")
    
    logger.info(f"Client disconnected from {getattr(websocket, 'remote_address', 'unknown')}. Total clients: {len(clients)}")


async def join_channel(websocket: websockets.WebSocketServerProtocol, channel: str) -> None:
    """Add client to a channel."""
    if channel not in channels:
        channels[channel] = set()
    
    channels[channel].add(websocket)
    logger.info(f"Client from {getattr(websocket, 'remote_address', 'unknown')} joined channel '{channel}'. Channel size: {len(channels[channel])}")


async def broadcast_to_channel(channel: str, message: Dict[str, Any], sender: websockets.WebSocketServerProtocol = None) -> None:
    """Broadcast message to all clients in a channel except sender."""
    if channel not in channels:
        logger.warning(f"Attempted to broadcast to non-existent channel: {channel}")
        return
    
    message_str = json.dumps(message)
    disconnected = set()
    broadcast_count = 0
    
    for client in channels[channel]:
        if client != sender:  # Don't send back to sender
            try:
                await client.send(message_str)
                broadcast_count += 1
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(client)
    
    # Clean up disconnected clients
    for client in disconnected:
        channels[channel].discard(client)
        clients.discard(client)
    
    if broadcast_count > 0:
        logger.debug(f"Broadcasted message to {broadcast_count} clients in channel '{channel}'")


async def handle_client(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    """Handle individual client connection."""
    await register_client(websocket)
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.debug(f"Received from {getattr(websocket, 'remote_address', 'unknown')}: {data}")
                
                # Handle join channel requests
                if data.get("type") == "join":
                    channel = data.get("channel")
                    if channel:
                        await join_channel(websocket, channel)
                        
                        # Send acknowledgment back to joining client
                        # This is what Figma plugin expects for join confirmation
                        response = {
                            "type": "system",
                            "channel": channel,
                            "message": {
                                "result": {"status": "joined", "channel": channel}
                            }
                        }
                        await websocket.send(json.dumps(response))
                        logger.info(f"Sent join confirmation to client for channel: {channel}")
                    else:
                        # Send error response
                        response = {
                            "type": "error", 
                            "message": "Channel name is required"
                        }
                        await websocket.send(json.dumps(response))
                
                # Handle regular messages that should be broadcasted
                elif data.get("type") == "message":
                    channel = data.get("channel")
                    if channel and channel in channels:
                        # Forward the entire message structure to other clients in the channel
                        await broadcast_to_channel(channel, data, websocket)
                    else:
                        # Send error response
                        response = {
                            "id": data.get("id"),
                            "error": f"Channel '{channel}' not found or not joined"
                        }
                        await websocket.send(json.dumps(response))
                
                # Handle direct messages (without broadcast)
                elif "id" in data and "message" in data:
                    # This might be a direct response, just log it
                    logger.debug(f"Received direct message: {data}")
                
                # Handle other message types
                else:
                    logger.warning(f"Unknown message type from {getattr(websocket, 'remote_address', 'unknown')}: {data.get('type', 'no-type')}")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from {getattr(websocket, 'remote_address', 'unknown')}: {e}")
                error_response = {
                    "error": "Invalid JSON format"
                }
                try:
                    await websocket.send(json.dumps(error_response))
                except:
                    pass  # Connection might be broken
            except Exception as e:
                logger.error(f"Error handling message from {getattr(websocket, 'remote_address', 'unknown')}: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client connection closed: {getattr(websocket, 'remote_address', 'unknown')}")
    except Exception as e:
        logger.error(f"Error in client handler for {getattr(websocket, 'remote_address', 'unknown')}: {e}")
    finally:
        await unregister_client(websocket)


async def health_check(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    """Health check endpoint."""
    if path == "/health":
        await websocket.send(json.dumps({
            "status": "healthy",
            "clients": len(clients),
            "channels": {name: len(client_set) for name, client_set in channels.items()}
        }))
        await websocket.close()


async def main():
    """Main function to start the WebSocket server."""
    parser = argparse.ArgumentParser(description="WebSocket server for Figma plugin and MCP communication")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=3055, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Setup graceful shutdown
    loop = asyncio.get_event_loop()
    
    def signal_handler():
        logger.info("Received interrupt signal, shutting down...")
        for client in clients.copy():
            asyncio.create_task(client.close())
        loop.stop()
    
    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, signal_handler)
    
    logger.info(f"Starting WebSocket server on {args.host}:{args.port}")
    
    # Start the server
    server = await serve(
        handle_client,
        args.host,
        args.port,
        ping_interval=20,
        ping_timeout=10,
        close_timeout=10
    )
    
    logger.info(f"WebSocket server listening on ws://{args.host}:{args.port}")
    logger.info("Server ready to accept connections from Figma plugin and MCP server")
    
    try:
        await server.wait_closed()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    finally:
        server.close()
        await server.wait_closed()
        logger.info("Server stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server interrupted")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1) 