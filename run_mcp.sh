#!/bin/bash
cd /Users/dka/Documents/Solo/git/figma_mcp
source venv/bin/activate
exec python -m src.figma_mcp.server "$@" 