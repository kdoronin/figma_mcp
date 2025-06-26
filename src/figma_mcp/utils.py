"""Utility functions for Figma data processing."""

from typing import Any, Dict, List, Optional, Union
import json
from src.figma_mcp.figma_types import rgba_to_hex


def filter_figma_node(node: Any) -> Dict[str, Any]:
    """Filter and process Figma node data to remove sensitive information and format colors."""
    if not node:
        return {}
    
    # Convert to dict if it's not already
    if not isinstance(node, dict):
        try:
            node = json.loads(str(node)) if hasattr(node, '__str__') else {}
        except:
            return {}
    
    filtered = {}
    
    # Basic node properties
    basic_props = [
        'id', 'name', 'type', 'visible', 'locked', 'x', 'y', 'width', 'height',
        'rotation', 'opacity', 'blendMode', 'isMask', 'effects', 'effectStyleId',
        'characters', 'style', 'characterStyleOverrides', 'styleOverrideTable'
    ]
    
    for prop in basic_props:
        if prop in node:
            filtered[prop] = node[prop]
    
    # Handle fills with color conversion
    if 'fills' in node and node['fills']:
        filtered['fills'] = []
        for fill in node['fills']:
            if isinstance(fill, dict):
                fill_copy = fill.copy()
                if 'color' in fill_copy:
                    fill_copy['colorHex'] = rgba_to_hex(fill_copy['color'])
                filtered['fills'].append(fill_copy)
    
    # Handle strokes with color conversion
    if 'strokes' in node and node['strokes']:
        filtered['strokes'] = []
        for stroke in node['strokes']:
            if isinstance(stroke, dict):
                stroke_copy = stroke.copy()
                if 'color' in stroke_copy:
                    stroke_copy['colorHex'] = rgba_to_hex(stroke_copy['color'])
                filtered['strokes'].append(stroke_copy)
    
    # Layout properties
    layout_props = [
        'layoutMode', 'itemSpacing', 'counterAxisSpacing', 'primaryAxisAlignItems',
        'counterAxisAlignItems', 'paddingLeft', 'paddingRight', 'paddingTop',
        'paddingBottom', 'layoutGrow', 'layoutAlign', 'layoutSizingHorizontal',
        'layoutSizingVertical'
    ]
    
    for prop in layout_props:
        if prop in node:
            filtered[prop] = node[prop]
    
    # Corner properties
    corner_props = [
        'cornerRadius', 'topLeftRadius', 'topRightRadius', 'bottomLeftRadius',
        'bottomRightRadius'
    ]
    
    for prop in corner_props:
        if prop in node:
            filtered[prop] = node[prop]
    
    # Text properties
    text_props = [
        'fontSize', 'fontName', 'textAlignHorizontal', 'textAlignVertical',
        'letterSpacing', 'lineHeight', 'paragraphSpacing', 'paragraphIndent',
        'textDecoration', 'textCase'
    ]
    
    for prop in text_props:
        if prop in node:
            filtered[prop] = node[prop]
    
    # Component properties
    component_props = [
        'componentId', 'componentProperties', 'variantProperties', 'exposedInstances',
        'overrides', 'mainComponent'
    ]
    
    for prop in component_props:
        if prop in node:
            filtered[prop] = node[prop]
    
    # Constraints
    if 'constraints' in node:
        filtered['constraints'] = node['constraints']
    
    # Export settings
    if 'exportSettings' in node:
        filtered['exportSettings'] = node['exportSettings']
    
    # Reactions (prototyping)
    if 'reactions' in node:
        filtered['reactions'] = node['reactions']
    
    # Children (recursively filter)
    if 'children' in node and isinstance(node['children'], list):
        filtered['children'] = []
        for child in node['children']:
            filtered_child = filter_figma_node(child)
            if filtered_child:
                filtered['children'].append(filtered_child)
    
    # Parent information (without full recursion)
    if 'parent' in node and isinstance(node['parent'], dict):
        parent = node['parent']
        filtered['parent'] = {
            'id': parent.get('id'),
            'name': parent.get('name'),
            'type': parent.get('type')
        }
    
    return filtered


def process_figma_node_response(result: Any) -> Any:
    """Process Figma node response and filter sensitive data."""
    if not result:
        return result
    
    # Handle different response structures
    if isinstance(result, dict):
        if 'node' in result:
            # Single node response
            result_copy = result.copy()
            result_copy['node'] = filter_figma_node(result['node'])
            return result_copy
        elif 'nodes' in result:
            # Multiple nodes response
            result_copy = result.copy()
            if isinstance(result['nodes'], dict):
                result_copy['nodes'] = {}
                for node_id, node_data in result['nodes'].items():
                    if isinstance(node_data, dict) and 'document' in node_data:
                        result_copy['nodes'][node_id] = {
                            **node_data,
                            'document': filter_figma_node(node_data['document'])
                        }
                    else:
                        result_copy['nodes'][node_id] = filter_figma_node(node_data)
            elif isinstance(result['nodes'], list):
                result_copy['nodes'] = [filter_figma_node(node) for node in result['nodes']]
            return result_copy
        elif 'children' in result:
            # Direct node with children
            return filter_figma_node(result)
        else:
            # Other response types (styles, components, etc.)
            return result
    elif isinstance(result, list):
        # Array of nodes
        return [filter_figma_node(node) for node in result]
    else:
        # Other data types
        return result


def format_node_info(node: Dict[str, Any]) -> str:
    """Format node information for display."""
    if not node:
        return "No node data available"
    
    info_parts = []
    
    # Basic info
    if 'name' in node:
        info_parts.append(f"Name: {node['name']}")
    if 'type' in node:
        info_parts.append(f"Type: {node['type']}")
    if 'id' in node:
        info_parts.append(f"ID: {node['id']}")
    
    # Dimensions
    if 'width' in node and 'height' in node:
        info_parts.append(f"Size: {node['width']}×{node['height']}")
    
    # Position
    if 'x' in node and 'y' in node:
        info_parts.append(f"Position: ({node['x']}, {node['y']})")
    
    # Colors
    if 'fills' in node and node['fills']:
        fills = []
        for fill in node['fills']:
            if isinstance(fill, dict) and 'colorHex' in fill:
                fills.append(fill['colorHex'])
        if fills:
            info_parts.append(f"Fill colors: {', '.join(fills)}")
    
    # Text content
    if 'characters' in node:
        text_preview = node['characters'][:50] + "..." if len(node['characters']) > 50 else node['characters']
        info_parts.append(f"Text: {text_preview}")
    
    # Children count
    if 'children' in node and isinstance(node['children'], list):
        info_parts.append(f"Children: {len(node['children'])}")
    
    # If no info found, return a message
    if not info_parts:
        return "No node data available"
    
    return "\n".join(info_parts)


def validate_node_id(node_id: str) -> bool:
    """Validate if a node ID is in the correct format."""
    if not node_id or not isinstance(node_id, str):
        return False
    
    # Figma node IDs are typically in format like "I123:456" or "123:456"
    # Check for basic format with colon and minimum length
    if ':' in node_id and len(node_id) >= 3:  # Changed from > 3 to >= 3
        return True
    
    return False


def safe_get_nested(data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """Safely get nested dictionary value."""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def extract_text_nodes(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all text nodes from a Figma node tree."""
    text_nodes = []
    
    if not isinstance(node, dict):
        return text_nodes
    
    # Check if current node is a text node
    if node.get('type') == 'TEXT' and 'characters' in node:
        text_nodes.append({
            'id': node.get('id'),
            'name': node.get('name'),
            'characters': node.get('characters'),
            'fontSize': safe_get_nested(node, ['style', 'fontSize']),
            'fontFamily': safe_get_nested(node, ['style', 'fontFamily']),
        })
    
    # Recursively check children
    if 'children' in node and isinstance(node['children'], list):
        for child in node['children']:
            text_nodes.extend(extract_text_nodes(child))
    
    return text_nodes


def extract_component_instances(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all component instances from a Figma node tree."""
    instances = []
    
    if not isinstance(node, dict):
        return instances
    
    # Check if current node is a component instance
    if node.get('type') == 'INSTANCE' and 'componentId' in node:
        instances.append({
            'id': node.get('id'),
            'name': node.get('name'),
            'componentId': node.get('componentId'),
            'overrides': node.get('overrides', [])
        })
    
    # Recursively check children
    if 'children' in node and isinstance(node['children'], list):
        for child in node['children']:
            instances.extend(extract_component_instances(child))
    
    return instances


def count_nodes_by_type(node: Dict[str, Any]) -> Dict[str, int]:
    """Count nodes by type in a Figma node tree."""
    counts = {}
    
    if not isinstance(node, dict):
        return counts
    
    # Count current node
    node_type = node.get('type', 'UNKNOWN')
    counts[node_type] = counts.get(node_type, 0) + 1
    
    # Recursively count children
    if 'children' in node and isinstance(node['children'], list):
        for child in node['children']:
            child_counts = count_nodes_by_type(child)
            for child_type, count in child_counts.items():
                counts[child_type] = counts.get(child_type, 0) + count
    
    return counts 