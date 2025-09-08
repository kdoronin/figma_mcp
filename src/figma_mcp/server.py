"""Figma MCP Server using FastMCP."""

import asyncio
import json
import logging
import sys
import os
from typing import Any, Dict, List, Optional
import argparse

# Add project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)



from fastmcp import FastMCP
from pydantic import Field

from src.figma_mcp.websocket_client import FigmaWebSocketClient
from src.figma_mcp.figma_types import (
    FigmaCommand, GetNodeInfoParams, GetNodesInfoParams, GetNodeChildrenParams,
    ScanTextNodesParams, GetAnnotationsParams, ScanNodesByTypesParams,
    GetInstanceOverridesParams, ExportNodeAsImageParams, GetReactionsParams
)
from src.figma_mcp.utils import process_figma_node_response, format_node_info


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    stream=sys.stderr  # Log to stderr to avoid stdout capture
)
logger = logging.getLogger(__name__)

# Global WebSocket client
figma_client: Optional[FigmaWebSocketClient] = None

# Create FastMCP app
mcp = FastMCP("TalkToFigmaMCP")


async def get_figma_client() -> FigmaWebSocketClient:
    """Get or create Figma WebSocket client."""
    global figma_client
    if figma_client is None:
        # Parse command line arguments for server URL
        parser = argparse.ArgumentParser()
        parser.add_argument('--server', default='localhost:3055', help='Server URL with port')
        args, _ = parser.parse_known_args()
        
        server_url = args.server
        # Ensure we have port in the URL
        if ':' not in server_url:
            server_url = f"{server_url}:3055"
        
        figma_client = FigmaWebSocketClient(server_url=server_url)
        
        # Try to connect
        try:
            await figma_client.connect()
        except Exception as e:
            logger.warning(f"Could not connect to Figma initially: {e}")
            logger.warning("Will try to connect when the first command is sent")
    
    return figma_client


@mcp.tool()
async def get_document_info() -> str:
    """Get detailed information about the current Figma document."""
    try:
        client = await get_figma_client()
        result = await client.send_command(FigmaCommand.GET_DOCUMENT_INFO)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting document info: {str(e)}"


@mcp.tool()
async def get_selection() -> str:
    """Get information about the current selection in Figma."""
    try:
        client = await get_figma_client()
        result = await client.send_command(FigmaCommand.GET_SELECTION)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting selection: {str(e)}"


@mcp.tool()
async def read_my_design() -> str:
    """Get detailed information about the current selection in Figma, including all node details."""
    try:
        client = await get_figma_client()
        result = await client.send_command(FigmaCommand.READ_MY_DESIGN)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting node info: {str(e)}"


@mcp.tool()
async def get_node_info(node_id: str = Field(description="The ID of the node to get information about")) -> str:
    """Get detailed information about a specific node in Figma."""
    try:
        client = await get_figma_client()
        result = await client.send_command(
            FigmaCommand.GET_NODE_INFO, 
            {"nodeId": node_id}
        )
        filtered_result = process_figma_node_response(result)
        return json.dumps(filtered_result, indent=2)
    except Exception as e:
        return f"Error getting node info: {str(e)}"


@mcp.tool()
async def get_nodes_info(node_ids: List[str] = Field(description="List of node IDs to get information about")) -> str:
    """Get detailed information about multiple nodes in Figma."""
    try:
        client = await get_figma_client()
        result = await client.send_command(
            FigmaCommand.GET_NODES_INFO, 
            {"nodeIds": node_ids}
        )
        filtered_result = process_figma_node_response(result)
        return json.dumps(filtered_result, indent=2)
    except Exception as e:
        return f"Error getting nodes info: {str(e)}"


@mcp.tool()
async def get_node_children(node_id: str = Field(description="The ID of the node to get all children IDs from")) -> str:
    """Get all children node IDs from a specified node, including all nested levels."""
    try:
        client = await get_figma_client()
        result = await client.send_command(
            FigmaCommand.GET_NODE_CHILDREN, 
            {"nodeId": node_id}
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting node children: {str(e)}"


@mcp.tool()
async def get_styles() -> str:
    """Get all styles from the current Figma document."""
    try:
        client = await get_figma_client()
        result = await client.send_command(FigmaCommand.GET_STYLES)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting styles: {str(e)}"


@mcp.tool()
async def get_local_components() -> str:
    """Get all local components from the current Figma document."""
    try:
        client = await get_figma_client()
        result = await client.send_command(FigmaCommand.GET_LOCAL_COMPONENTS)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting local components: {str(e)}"


@mcp.tool()
async def get_instance_overrides(
    instance_node_id: Optional[str] = Field(default=None, description="The ID of the instance node to get overrides for")
) -> str:
    """Get instance overrides for a component instance."""
    try:
        client = await get_figma_client()
        result = await client.send_command(
            FigmaCommand.GET_INSTANCE_OVERRIDES, 
            {"instanceNodeId": instance_node_id}
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting instance overrides: {str(e)}"


@mcp.tool()
async def export_node_as_image(
    node_id: str = Field(description="The ID of the node to export"),
    output_path: str = Field(description="REQUIRED: Full absolute path to output directory (e.g., '/Users/username/project/assets/images')"),
    format: str = Field(default="PNG", description="Export format (PNG, JPG, SVG, PDF)"),
    scale: float = Field(default=1.0, description="Export scale factor"),
    filename: Optional[str] = Field(default=None, description="Custom filename (without extension)")
) -> str:
    """Export a node as an image and save to file system.
    
    IMPORTANT: Always specify a full absolute path for output_path parameter. 
    This ensures images are saved exactly where you intend them to be.
    
    Example: output_path='/Users/username/Documents/my_project/assets/images'
    """
    try:
        import os
        from src.figma_mcp.file_manager import ImageFileManager, generate_filename_from_node_id
        
        # Validate output path
        if not output_path or not os.path.isabs(output_path):
            raise ValueError("output_path must be a full absolute path (e.g., '/Users/username/project/assets/images')")
        
        # Set values
        actual_output_path = output_path
        actual_filename = filename or generate_filename_from_node_id(node_id, format)
        
        logger.info(f"Exporting node {node_id} as {format} to {actual_output_path}/{actual_filename}")
        
        # Get image data from Figma
        client = await get_figma_client()
        figma_result = await client.send_command(
            FigmaCommand.EXPORT_NODE_AS_IMAGE, 
            {
                "nodeId": node_id,
                "format": format,
                "scale": scale
            }
        )
        
        # Process and save the exported image
        result = ImageFileManager.process_figma_export_result(
            export_result=figma_result,
            output_path=actual_output_path,
            filename=actual_filename,
            node_id=node_id,
            format_name=format,
            scale=scale
        )
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in export_node_as_image: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": f"Failed to export and save image: {str(e)}"
        }, indent=2)


@mcp.tool()
async def join_channel(channel: str = Field(description="The name of the channel to join")) -> str:
    """Join a specific channel to communicate with Figma."""
    try:
        if not channel:
            return "Please provide a channel name to join"
        
        client = await get_figma_client()
        await client.join_channel(channel)
        return f"Successfully joined channel: {channel}"
    except Exception as e:
        return f"Error joining channel: {str(e)}"


@mcp.tool()
async def scan_text_nodes(
    node_id: str = Field(description="The ID of the node to scan for text nodes"),
    use_chunking: bool = Field(default=True, description="Whether to use chunking for large operations"),
    chunk_size: int = Field(default=50, description="Number of nodes to process per chunk")
) -> str:
    """Scan for text nodes within a given node."""
    try:
        client = await get_figma_client()
        result = await client.send_command(
            FigmaCommand.SCAN_TEXT_NODES, 
            {
                "nodeId": node_id,
                "useChunking": use_chunking,
                "chunkSize": chunk_size
            }
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error scanning text nodes: {str(e)}"


@mcp.tool()
async def get_annotations(
    node_id: Optional[str] = Field(default=None, description="The ID of the node to get annotations for"),
    include_categories: bool = Field(default=False, description="Whether to include category information")
) -> str:
    """Get annotations for a node or the entire document."""
    try:
        client = await get_figma_client()
        params = {"includeCategories": include_categories}
        if node_id:
            params["nodeId"] = node_id
        
        result = await client.send_command(FigmaCommand.GET_ANNOTATIONS, params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting annotations: {str(e)}"


@mcp.tool()
async def scan_nodes_by_types(
    node_id: str = Field(description="The ID of the node to scan"),
    types: List[str] = Field(description="List of node types to scan for (e.g., ['TEXT', 'RECTANGLE', 'FRAME'])")
) -> str:
    """Scan for nodes of specific types within a given node."""
    try:
        client = await get_figma_client()
        result = await client.send_command(
            FigmaCommand.SCAN_NODES_BY_TYPES, 
            {
                "nodeId": node_id,
                "types": types
            }
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error scanning nodes by types: {str(e)}"


@mcp.tool()
async def get_reactions(
    node_ids: List[str] = Field(description="List of node IDs to get reactions for")
) -> str:
    """Get reactions (prototyping interactions) for nodes."""
    try:
        client = await get_figma_client()
        result = await client.send_command(
            FigmaCommand.GET_REACTIONS, 
            {"nodeIds": node_ids}
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting reactions: {str(e)}"


def main():
    """Main function to run the MCP server."""
    logger.info("Starting Figma MCP Server...")
    logger.info("WebSocket client will connect when first tool is called")
    
    # Run the MCP server (FastMCP handles the event loop)
    mcp.run()


if __name__ == "__main__":
    main() 