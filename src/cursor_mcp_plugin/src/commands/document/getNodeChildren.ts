/// <reference types="@figma/plugin-typings" />

// Get node children IDs command

export async function getNodeChildren(nodeId: string): Promise<string[]> {
  const node = await figma.getNodeByIdAsync(nodeId);

  if (!node) {
    throw new Error(`Node not found with ID: ${nodeId}`);
  }

  const childrenIds: string[] = [];

  function collectChildrenIds(currentNode: BaseNode): void {
    // Check if node has children property
    if ('children' in currentNode && currentNode.children) {
      for (const child of currentNode.children) {
        childrenIds.push(child.id);
        // Recursively collect children from nested nodes
        collectChildrenIds(child);
      }
    }
  }

  // Start collecting from the specified node
  collectChildrenIds(node);

  return childrenIds;
} 