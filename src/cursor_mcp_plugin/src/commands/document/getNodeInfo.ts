/// <reference types="@figma/plugin-typings" />

// Get node info command

import { filterFigmaNode } from '../../utils/node-filters';

// Helper function to recursively add missing node properties
function addMissingNodeProperties(exportedNode: any, figmaNode: any) {
  // Add missing properties to current node
  if ('absoluteBoundingBox' in figmaNode && figmaNode.absoluteBoundingBox) {
    exportedNode.absoluteBoundingBox = figmaNode.absoluteBoundingBox;
  }
  
  if ('x' in figmaNode) {
    exportedNode.x = figmaNode.x;
  }
  
  if ('y' in figmaNode) {
    exportedNode.y = figmaNode.y;
  }
  
  if ('width' in figmaNode) {
    exportedNode.width = figmaNode.width;
  }
  
  if ('height' in figmaNode) {
    exportedNode.height = figmaNode.height;
  }
  
  if ('relativeTransform' in figmaNode) {
    exportedNode.relativeTransform = figmaNode.relativeTransform;
  }
  
  if ('absoluteTransform' in figmaNode) {
    exportedNode.absoluteTransform = figmaNode.absoluteTransform;
  }

  // Recursively process children
  if (exportedNode.children && figmaNode.children) {
    for (let i = 0; i < exportedNode.children.length; i++) {
      if (figmaNode.children[i]) {
        addMissingNodeProperties(exportedNode.children[i], figmaNode.children[i]);
      }
    }
  }
}

export async function getNodeInfo(nodeId: string) {
  const node = await figma.getNodeByIdAsync(nodeId);

  if (!node) {
    throw new Error(`Node not found with ID: ${nodeId}`);
  }

  // Check if node supports exportAsync
  if (!('exportAsync' in node)) {
    throw new Error(`Node does not support exporting: ${nodeId}`);
  }

  const response = await (node as any).exportAsync({
    format: "JSON_REST_V1",
  });

  // Merge exported data with direct node properties
  const exportedNode = response.document;
  
  // Recursively add missing properties for the node and all its children
  addMissingNodeProperties(exportedNode, node);

  return filterFigmaNode(exportedNode);
}