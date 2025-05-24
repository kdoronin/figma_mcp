"""WebSocket client for MCP server to communicate with Figma plugin."""

import asyncio
import json
import logging
import sys
import uuid
import websockets
from typing import Any, Dict, Optional
import time

# Setup logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


class FigmaWebSocketClient:
    """WebSocket client for MCP server to communicate with Figma plugin."""
    
    def __init__(self, server_url: str = "localhost:3055"):
        # Parse server URL
        if ":" in server_url:
            host, port = server_url.split(":", 1)
            self.ws_url = f"ws://{host}:{port}"
        else:
            self.ws_url = f"ws://{server_url}:3055"
        
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.connected = False
        self.current_channel: Optional[str] = None
        self.pending_requests: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"Initialized WebSocket client for {self.ws_url}")
    
    async def connect(self) -> None:
        """Connect to the WebSocket server."""
        try:
            logger.info(f"Connecting to {self.ws_url}...")
            self.websocket = await websockets.connect(
                self.ws_url,
                ping_interval=20,
                ping_timeout=10,
                close_timeout=10
            )
            self.connected = True
            logger.info("Successfully connected to WebSocket server")
            
            # Start message handler
            asyncio.create_task(self._handle_messages())
            
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket server: {e}")
            self.connected = False
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from the WebSocket server."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.connected = False
            self.current_channel = None
            logger.info("Disconnected from WebSocket server")
    
    async def join_channel(self, channel: str) -> None:
        """Join a specific channel."""
        if not self.connected or not self.websocket:
            await self.connect()
        
        try:
            join_message = {
                "type": "join",
                "channel": channel
            }
            
            await self.websocket.send(json.dumps(join_message))
            logger.info(f"Sent join request for channel: {channel}")
            
            # Wait for join confirmation with timeout
            timeout = time.time() + 10  # 10 seconds timeout
            while time.time() < timeout:
                await asyncio.sleep(0.1)
                if self.current_channel == channel:
                    break
            else:
                raise TimeoutError(f"Failed to join channel {channel} within timeout")
            
            logger.info(f"Successfully joined channel: {channel}")
            
        except Exception as e:
            logger.error(f"Failed to join channel {channel}: {e}")
            raise
    
    async def send_command(self, command: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to Figma and wait for response."""
        if not self.connected or not self.websocket:
            await self.connect()
        
        if not self.current_channel:
            raise RuntimeError("Must join a channel before sending commands")
        
        request_id = str(uuid.uuid4())
        
        # Format message exactly like TypeScript version
        message = {
            "id": request_id,
            "type": "message",
            "channel": self.current_channel,
            "message": {
                "id": request_id,
                "command": command,
                "params": {
                    **(params or {}),
                    "commandId": request_id  # Include commandId like TypeScript version
                }
            }
        }
        
        # Create promise for response
        future = asyncio.Future()
        self.pending_requests[request_id] = {
            "future": future,
            "timestamp": time.time()
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            logger.info(f"Sending command to Figma: {command}")
            logger.debug(f"Request details: {json.dumps(message)}")
            
            # Wait for response with 30 second timeout
            result = await asyncio.wait_for(future, timeout=30.0)
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"Command {command} timed out after 30 seconds")
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
            raise
        except Exception as e:
            logger.error(f"Error sending command {command}: {e}")
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
            raise
    
    async def _handle_messages(self) -> None:
        """Handle incoming WebSocket messages."""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._process_message(data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
            self.connected = False
        except Exception as e:
            logger.error(f"Error in message handler: {e}")
            self.connected = False
    
    async def _process_message(self, data: Dict[str, Any]) -> None:
        """Process incoming message from WebSocket."""
        logger.debug(f"Received message: {data}")
        
        # Handle system messages (like join confirmations)
        if data.get("type") == "system":
            if data.get("channel") and data.get("message", {}).get("result"):
                self.current_channel = data["channel"]
                logger.info(f"Joined channel: {data['channel']}")
            return
        
        # Handle error messages
        if data.get("type") == "error":
            logger.error(f"Received error: {data.get('message')}")
            return
        
        # Handle regular messages from Figma plugin
        if data.get("type") == "message":
            message = data.get("message", {})
            message_id = message.get("id")
            
            # If this is a response to our request
            if message_id and message_id in self.pending_requests:
                request_info = self.pending_requests.pop(message_id)
                future = request_info["future"]
                
                if message.get("error"):
                    future.set_exception(Exception(message["error"]))
                else:
                    future.set_result(message.get("result", {}))
                return
        
        # Handle broadcast messages or events
        logger.info(f"Received broadcast message: {json.dumps(data)}") 