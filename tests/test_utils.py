"""Tests for utility functions."""

import pytest
import json

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from figma_mcp.utils import (
    filter_figma_node, process_figma_node_response, format_node_info,
    validate_node_id, safe_get_nested, extract_text_nodes, 
    extract_component_instances, count_nodes_by_type
)


class TestFilterFigmaNode:
    """Test filter_figma_node function."""
    
    def test_filter_empty_node(self):
        """Test filtering empty node."""
        result = filter_figma_node(None)
        assert result == {}
        
        result = filter_figma_node({})
        assert result == {}
    
    def test_filter_basic_properties(self):
        """Test filtering basic node properties."""
        node = {
            "id": "123:456",
            "name": "Test Node",
            "type": "RECTANGLE",
            "x": 100,
            "y": 200,
            "width": 300,
            "height": 400,
            "visible": True,
            "locked": False,
            "rotation": 0,
            "opacity": 1.0
        }
        
        result = filter_figma_node(node)
        
        assert result["id"] == "123:456"
        assert result["name"] == "Test Node"
        assert result["type"] == "RECTANGLE"
        assert result["x"] == 100
        assert result["y"] == 200
        assert result["width"] == 300
        assert result["height"] == 400
    
    def test_filter_fills_with_colors(self):
        """Test filtering fills and converting colors."""
        node = {
            "id": "123:456",
            "fills": [
                {
                    "type": "SOLID",
                    "color": {"r": 1.0, "g": 0.5, "b": 0.0, "a": 1.0}
                }
            ]
        }
        
        result = filter_figma_node(node)
        
        assert "fills" in result
        assert len(result["fills"]) == 1
        assert result["fills"][0]["colorHex"] == "#ff7f00"
        assert result["fills"][0]["type"] == "SOLID"
    
    def test_filter_children_recursively(self):
        """Test recursive filtering of children."""
        node = {
            "id": "parent",
            "name": "Parent",
            "type": "FRAME",
            "children": [
                {
                    "id": "child1",
                    "name": "Child 1",
                    "type": "TEXT",
                    "characters": "Hello"
                },
                {
                    "id": "child2",
                    "name": "Child 2",
                    "type": "RECTANGLE",
                    "fills": [
                        {
                            "type": "SOLID",
                            "color": {"r": 0.0, "g": 1.0, "b": 0.0}
                        }
                    ]
                }
            ]
        }
        
        result = filter_figma_node(node)
        
        assert "children" in result
        assert len(result["children"]) == 2
        assert result["children"][0]["id"] == "child1"
        assert result["children"][0]["characters"] == "Hello"
        assert result["children"][1]["fills"][0]["colorHex"] == "#00ff00"
    
    def test_filter_text_properties(self):
        """Test filtering text-specific properties."""
        node = {
            "id": "text-node",
            "type": "TEXT",
            "characters": "Sample text",
            "fontSize": 16,
            "fontName": {"family": "Roboto", "style": "Regular"},
            "textAlignHorizontal": "LEFT",
            "textAlignVertical": "TOP"
        }
        
        result = filter_figma_node(node)
        
        assert result["characters"] == "Sample text"
        assert result["fontSize"] == 16
        assert result["fontName"]["family"] == "Roboto"
        assert result["textAlignHorizontal"] == "LEFT"


class TestProcessFigmaNodeResponse:
    """Test process_figma_node_response function."""
    
    def test_process_single_node_response(self):
        """Test processing single node response."""
        response = {
            "node": {
                "id": "123:456",
                "name": "Test",
                "fills": [{"type": "SOLID", "color": {"r": 1.0, "g": 0, "b": 0}}]
            }
        }
        
        result = process_figma_node_response(response)
        
        assert "node" in result
        assert result["node"]["id"] == "123:456"
        assert result["node"]["fills"][0]["colorHex"] == "#ff0000"
    
    def test_process_multiple_nodes_response(self):
        """Test processing multiple nodes response."""
        response = {
            "nodes": {
                "123:456": {
                    "document": {
                        "id": "123:456",
                        "name": "Node 1"
                    }
                },
                "789:012": {
                    "document": {
                        "id": "789:012",
                        "name": "Node 2"
                    }
                }
            }
        }
        
        result = process_figma_node_response(response)
        
        assert "nodes" in result
        assert "123:456" in result["nodes"]
        assert result["nodes"]["123:456"]["document"]["name"] == "Node 1"
    
    def test_process_direct_node(self):
        """Test processing direct node data."""
        node = {
            "id": "123:456",
            "name": "Direct Node",
            "children": [
                {"id": "child1", "name": "Child"}
            ]
        }
        
        result = process_figma_node_response(node)
        
        assert result["id"] == "123:456"
        assert result["name"] == "Direct Node"
        assert len(result["children"]) == 1


class TestFormatNodeInfo:
    """Test format_node_info function."""
    
    def test_format_basic_node_info(self):
        """Test formatting basic node information."""
        node = {
            "id": "123:456",
            "name": "Test Node",
            "type": "RECTANGLE",
            "width": 100,
            "height": 50,
            "x": 10,
            "y": 20
        }
        
        result = format_node_info(node)
        
        assert "Name: Test Node" in result
        assert "Type: RECTANGLE" in result
        assert "ID: 123:456" in result
        assert "Size: 100×50" in result
        assert "Position: (10, 20)" in result
    
    def test_format_text_node_info(self):
        """Test formatting text node information."""
        node = {
            "id": "text:123",
            "name": "Text Node",
            "type": "TEXT",
            "characters": "This is a very long text that should be truncated when displayed"
        }
        
        result = format_node_info(node)
        
        assert "Text: This is a very long text that should be truncated ..." in result
    
    def test_format_node_with_fills(self):
        """Test formatting node with fill colors."""
        node = {
            "id": "rect:123",
            "name": "Colored Rectangle",
            "fills": [
                {"colorHex": "#ff0000"},
                {"colorHex": "#00ff00"}
            ]
        }
        
        result = format_node_info(node)
        
        assert "Fill colors: #ff0000, #00ff00" in result
    
    def test_format_empty_node(self):
        """Test formatting empty node."""
        result = format_node_info(None)
        assert result == "No node data available"
        
        result = format_node_info({})
        assert result == "No node data available"  # Empty dict should also return no data available message


class TestValidateNodeId:
    """Test validate_node_id function."""
    
    def test_valid_node_ids(self):
        """Test valid node ID formats."""
        assert validate_node_id("123:456") == True
        assert validate_node_id("I123:456") == True
        assert validate_node_id("1:2") == True
        assert validate_node_id("abc:def") == True
    
    def test_invalid_node_ids(self):
        """Test invalid node ID formats."""
        assert validate_node_id("") == False
        assert validate_node_id(None) == False
        assert validate_node_id("123") == False  # No colon
        assert validate_node_id("12") == False   # Too short
        assert validate_node_id(123) == False    # Not string


class TestSafeGetNested:
    """Test safe_get_nested function."""
    
    def test_get_nested_existing_path(self):
        """Test getting existing nested value."""
        data = {
            "level1": {
                "level2": {
                    "level3": "value"
                }
            }
        }
        
        result = safe_get_nested(data, ["level1", "level2", "level3"])
        assert result == "value"
    
    def test_get_nested_missing_path(self):
        """Test getting missing nested value."""
        data = {
            "level1": {
                "level2": "value"
            }
        }
        
        result = safe_get_nested(data, ["level1", "missing", "level3"])
        assert result is None
        
        result = safe_get_nested(data, ["level1", "missing", "level3"], "default")
        assert result == "default"
    
    def test_get_nested_empty_data(self):
        """Test getting from empty data."""
        result = safe_get_nested({}, ["key"])
        assert result is None


class TestExtractTextNodes:
    """Test extract_text_nodes function."""
    
    def test_extract_single_text_node(self):
        """Test extracting a single text node."""
        node = {
            "id": "text:123",
            "name": "Text Node",
            "type": "TEXT",
            "characters": "Hello World",
            "style": {
                "fontSize": 16,
                "fontFamily": "Roboto"
            }
        }
        
        result = extract_text_nodes(node)
        
        assert len(result) == 1
        assert result[0]["id"] == "text:123"
        assert result[0]["characters"] == "Hello World"
        assert result[0]["fontSize"] == 16
    
    def test_extract_text_nodes_from_frame(self):
        """Test extracting text nodes from a frame with children."""
        frame = {
            "id": "frame:123",
            "type": "FRAME",
            "children": [
                {
                    "id": "text:1",
                    "type": "TEXT",
                    "characters": "First text"
                },
                {
                    "id": "rect:1",
                    "type": "RECTANGLE"
                },
                {
                    "id": "text:2",
                    "type": "TEXT", 
                    "characters": "Second text"
                }
            ]
        }
        
        result = extract_text_nodes(frame)
        
        assert len(result) == 2
        assert result[0]["characters"] == "First text"
        assert result[1]["characters"] == "Second text"
    
    def test_extract_no_text_nodes(self):
        """Test extracting from node without text."""
        node = {
            "id": "rect:123",
            "type": "RECTANGLE",
            "children": [
                {"id": "rect:child", "type": "RECTANGLE"}
            ]
        }
        
        result = extract_text_nodes(node)
        assert len(result) == 0


class TestExtractComponentInstances:
    """Test extract_component_instances function."""
    
    def test_extract_single_instance(self):
        """Test extracting a single component instance."""
        node = {
            "id": "instance:123",
            "name": "Button Instance",
            "type": "INSTANCE",
            "componentId": "component:456",
            "overrides": [{"id": "text:789", "property": "characters"}]
        }
        
        result = extract_component_instances(node)
        
        assert len(result) == 1
        assert result[0]["id"] == "instance:123"
        assert result[0]["componentId"] == "component:456"
        assert len(result[0]["overrides"]) == 1
    
    def test_extract_instances_from_frame(self):
        """Test extracting instances from frame with children."""
        frame = {
            "id": "frame:123",
            "type": "FRAME",
            "children": [
                {
                    "id": "instance:1",
                    "type": "INSTANCE",
                    "componentId": "comp:1"
                },
                {
                    "id": "rect:1",
                    "type": "RECTANGLE"
                },
                {
                    "id": "instance:2",
                    "type": "INSTANCE",
                    "componentId": "comp:2"
                }
            ]
        }
        
        result = extract_component_instances(frame)
        
        assert len(result) == 2
        assert result[0]["componentId"] == "comp:1"
        assert result[1]["componentId"] == "comp:2"


class TestCountNodesByType:
    """Test count_nodes_by_type function."""
    
    def test_count_single_node(self):
        """Test counting a single node."""
        node = {
            "type": "RECTANGLE"
        }
        
        result = count_nodes_by_type(node)
        
        assert result["RECTANGLE"] == 1
        assert len(result) == 1
    
    def test_count_frame_with_children(self):
        """Test counting frame with various children."""
        frame = {
            "type": "FRAME",
            "children": [
                {"type": "TEXT"},
                {"type": "RECTANGLE"},
                {"type": "TEXT"},
                {
                    "type": "FRAME",
                    "children": [
                        {"type": "ELLIPSE"},
                        {"type": "TEXT"}
                    ]
                }
            ]
        }
        
        result = count_nodes_by_type(frame)
        
        assert result["FRAME"] == 2  # Main frame + nested frame
        assert result["TEXT"] == 3   # 2 in main + 1 in nested
        assert result["RECTANGLE"] == 1
        assert result["ELLIPSE"] == 1
    
    def test_count_empty_node(self):
        """Test counting empty or invalid node."""
        result = count_nodes_by_type(None)
        assert result == {}
        
        result = count_nodes_by_type({})
        assert result["UNKNOWN"] == 1 