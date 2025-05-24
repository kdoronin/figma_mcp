#!/usr/bin/env python3
"""Entry point for Figma MCP Server."""

import asyncio
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from figma_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main()) 