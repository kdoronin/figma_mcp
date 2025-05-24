"""Tests for type definitions."""

import pytest
from pydantic import ValidationError

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from figma_mcp.types import (
    FigmaCommand, Color, FigmaResponse, CommandProgressUpdate,
    GetNodeInfoParams, SetFillColorParams, rgba_to_hex, generate_id
)


class TestFigmaCommand:
    """Test FigmaCommand enum."""
    
    def test_command_values(self):
        """Test that command values are correct."""
        assert FigmaCommand.GET_DOCUMENT_INFO == "get_document_info"
        assert FigmaCommand.GET_SELECTION == "get_selection"
        assert FigmaCommand.GET_NODE_INFO == "get_node_info"
        assert FigmaCommand.JOIN == "join"
    
    def test_all_commands_defined(self):
        """Test that all expected commands are defined."""
        expected_commands = [
            "get_document_info", "get_selection", "get_node_info", "get_nodes_info",
            "read_my_design", "delete_node", "delete_multiple_nodes", "get_styles",
            "get_local_components", "join", "set_corner_radius", "clone_node"
        ]
        
        for cmd in expected_commands:
            assert cmd in [c.value for c in FigmaCommand]


class TestColor:
    """Test Color model."""
    
    def test_valid_color(self):
        """Test creating a valid color."""
        color = Color(r=1.0, g=0.5, b=0.0, a=0.8)
        assert color.r == 1.0
        assert color.g == 0.5
        assert color.b == 0.0
        assert color.a == 0.8
    
    def test_color_default_alpha(self):
        """Test color with default alpha."""
        color = Color(r=1.0, g=0.5, b=0.0)
        assert color.a == 1.0
    
    def test_invalid_color(self):
        """Test invalid color values."""
        with pytest.raises(ValidationError):
            Color(r="invalid", g=0.5, b=0.0)


class TestFigmaResponse:
    """Test FigmaResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid response."""
        response = FigmaResponse(id="test-id", result={"data": "test"})
        assert response.id == "test-id"
        assert response.result == {"data": "test"}
        assert response.error is None
    
    def test_error_response(self):
        """Test response with error."""
        response = FigmaResponse(id="test-id", error="Test error")
        assert response.id == "test-id"
        assert response.error == "Test error"
        assert response.result is None


class TestCommandProgressUpdate:
    """Test CommandProgressUpdate model."""
    
    def test_valid_progress_update(self):
        """Test creating a valid progress update."""
        update = CommandProgressUpdate(
            commandId="test-id",
            commandType="test_command",
            status="in_progress",
            progress=50,
            totalItems=100,
            processedItems=50,
            message="Processing...",
            timestamp=1234567890
        )
        assert update.commandId == "test-id"
        assert update.status == "in_progress"
        assert update.progress == 50


class TestParameterModels:
    """Test parameter models."""
    
    def test_get_node_info_params(self):
        """Test GetNodeInfoParams."""
        params = GetNodeInfoParams(nodeId="123:456")
        assert params.nodeId == "123:456"
    
    def test_set_fill_color_params(self):
        """Test SetFillColorParams."""
        params = SetFillColorParams(
            nodeId="123:456",
            r=1.0,
            g=0.5,
            b=0.0,
            a=0.8
        )
        assert params.nodeId == "123:456"
        assert params.r == 1.0
        assert params.a == 0.8
    
    def test_set_fill_color_params_default_alpha(self):
        """Test SetFillColorParams with default alpha."""
        params = SetFillColorParams(
            nodeId="123:456",
            r=1.0,
            g=0.5,
            b=0.0
        )
        assert params.a == 1.0


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_generate_id(self):
        """Test ID generation."""
        id1 = generate_id()
        id2 = generate_id()
        
        assert isinstance(id1, str)
        assert isinstance(id2, str)
        assert id1 != id2
        assert len(id1) > 10  # UUIDs are longer than 10 chars
    
    def test_rgba_to_hex_dict(self):
        """Test RGBA to hex conversion with dict input."""
        color = {"r": 1.0, "g": 0.5, "b": 0.0, "a": 1.0}
        hex_color = rgba_to_hex(color)
        assert hex_color == "#ff7f00"
    
    def test_rgba_to_hex_none(self):
        """Test RGBA to hex conversion with None input."""
        hex_color = rgba_to_hex(None)
        assert hex_color == "#000000"
    
    def test_rgba_to_hex_empty(self):
        """Test RGBA to hex conversion with empty input."""
        hex_color = rgba_to_hex({})
        assert hex_color == "#000000"
    
    def test_rgba_to_hex_partial(self):
        """Test RGBA to hex conversion with partial color data."""
        color = {"r": 1.0}
        hex_color = rgba_to_hex(color)
        assert hex_color == "#ff0000" 