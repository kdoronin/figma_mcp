"""File management utilities for Figma MCP Server."""

import base64
import os
from pathlib import Path
from typing import Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class ImageFileManager:
    """Manages saving and organizing exported images."""
    
    @staticmethod
    def ensure_directory(directory_path: str) -> Path:
        """Ensure directory exists, create if necessary."""
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def get_file_extension(format_name: str) -> str:
        """Get file extension for format."""
        format_map = {
            "PNG": ".png",
            "JPG": ".jpg",
            "JPEG": ".jpg", 
            "SVG": ".svg",
            "PDF": ".pdf"
        }
        return format_map.get(format_name.upper(), ".png")
    
    @staticmethod
    def save_base64_image(
        base64_data: str, 
        output_path: str, 
        filename: str, 
        format_name: str
    ) -> str:
        """Save base64 image data to file."""
        try:
            # Ensure directory exists
            directory = ImageFileManager.ensure_directory(output_path)
            
            # Generate full filename with extension
            extension = ImageFileManager.get_file_extension(format_name)
            if not filename.endswith(extension):
                filename = f"{filename}{extension}"
            
            file_path = directory / filename
            
            # Decode and save binary data
            image_data = base64.b64decode(base64_data)
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            logger.info(f"Saved {format_name} image: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving base64 image: {e}")
            raise Exception(f"Failed to save image file: {str(e)}")
    
    @staticmethod
    def save_svg_string(
        svg_content: str, 
        output_path: str, 
        filename: str
    ) -> str:
        """Save SVG string content to file."""
        try:
            # Ensure directory exists
            directory = ImageFileManager.ensure_directory(output_path)
            
            # Generate filename with .svg extension
            if not filename.endswith('.svg'):
                filename = f"{filename}.svg"
            
            file_path = directory / filename
            
            # Save SVG content as UTF-8 text
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            logger.info(f"Saved SVG image: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving SVG file: {e}")
            raise Exception(f"Failed to save SVG file: {str(e)}")
    

    
    @staticmethod
    def process_figma_export_result(
        export_result: Dict[str, Any],
        output_path: str,
        filename: str,
        node_id: str,
        format_name: str,
        scale: float
    ) -> Dict[str, Any]:
        """Process Figma export result and save to file system."""
        try:
            if not export_result.get('success'):
                raise Exception(f"Export failed: {export_result.get('error', 'Unknown error')}")
            
            saved_file_path = ""
            metadata_path = ""
            
            # Handle different formats
            if format_name.upper() == "SVG":
                # SVG is returned as string
                svg_content = export_result.get('imageData', '')
                if not svg_content:
                    raise Exception("No SVG content received from export")
                
                saved_file_path = ImageFileManager.save_svg_string(
                    svg_content, output_path, filename
                )
            else:
                # Binary formats (PNG, JPG, PDF) are returned as base64
                base64_data = export_result.get('imageData', '')
                if not base64_data:
                    raise Exception("No image data received from export")
                
                saved_file_path = ImageFileManager.save_base64_image(
                    base64_data, output_path, filename, format_name
                )
            
            return {
                "success": True,
                "file_path": saved_file_path,
                "file_size": os.path.getsize(saved_file_path),
                "format": format_name,
                "message": f"Successfully saved {format_name} image: {saved_file_path}"
            }
            
        except Exception as e:
            logger.error(f"Error processing export result: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to save image: {str(e)}"
            }


def get_default_output_path() -> str:
    """Get default output path for exported images."""
    return os.path.join(os.getcwd(), "assets", "images")


def generate_filename_from_node_id(node_id: str, format_name: str) -> str:
    """Generate filename from node ID if none provided."""
    # Clean node ID for filename (replace : with -)
    clean_id = node_id.replace(":", "-")
    extension = ImageFileManager.get_file_extension(format_name)
    return f"node_{clean_id}{extension}"
