#!/usr/bin/env python3
"""Test script for MCP server."""

import asyncio
import json
import sys
import subprocess
import os

async def test_mcp_server():
    """Test MCP server with join_channel tool."""
    
    # Start MCP server
    cmd = [sys.executable, "-m", "src.figma_mcp.server", "--server", "localhost:3055"]
    
    print("Starting MCP server...")
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        # Initialize connection
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        print("Sending initialize request...")
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        print(f"Initialize response: {response.strip()}")
        
        # Send initialized notification
        initialized = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        print("Sending initialized notification...")
        process.stdin.write(json.dumps(initialized) + '\n')
        process.stdin.flush()
        
        # Join channel
        join_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "join_channel",
                "arguments": {
                    "channel": "neygy5j0"
                }
            }
        }
        
        print("Sending join_channel request...")
        process.stdin.write(json.dumps(join_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        print(f"Join channel response: {response.strip()}")
        
        # Test get_document_info
        doc_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_document_info",
                "arguments": {}
            }
        }
        
        print("Sending get_document_info request...")
        process.stdin.write(json.dumps(doc_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        print(f"Document info response: {response.strip()}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()
        process.wait()


if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 