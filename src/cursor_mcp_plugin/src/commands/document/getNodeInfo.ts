/// <reference types="@figma/plugin-typings" />

// Get node info command

import { filterFigmaNode } from '../../utils/node-filters';

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

  return filterFigmaNode(response.document);
}