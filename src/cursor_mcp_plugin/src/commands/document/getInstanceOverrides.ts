/// <reference types="@figma/plugin-typings" />

/**
 * Get instance overrides for a component instance.
 * @param instanceNodeId - Optional ID of the instance node. If not provided, uses current selection.
 * @returns Information about instance overrides
 */
export async function getInstanceOverrides(instanceNodeId?: string): Promise<any> {
  console.log("=== getInstanceOverrides called ===");

  let sourceInstance: InstanceNode | null = null;

  // Check if an instance node ID was provided
  if (instanceNodeId) {
    console.log("Using provided instance node ID:", instanceNodeId);

    // Get the instance node by ID
    const node = await figma.getNodeByIdAsync(instanceNodeId);
    if (!node) {
      throw new Error(`Instance node not found with ID: ${instanceNodeId}`);
    }

    // Validate that the node is an instance
    if (node.type !== "INSTANCE") {
      throw new Error("Provided node is not a component instance");
    }

    sourceInstance = node as InstanceNode;
  } else {
    // No node provided, use selection
    console.log("No node provided, using current selection");

    // Get the current selection
    const selection = figma.currentPage.selection;

    // Check if there's anything selected
    if (selection.length === 0) {
      throw new Error("No nodes selected. Please select at least one instance");
    }

    // Filter for instances in the selection
    const instances = selection.filter(node => node.type === "INSTANCE") as InstanceNode[];

    if (instances.length === 0) {
      throw new Error("No instances found in selection. Please select at least one component instance");
    }

    // Take the first instance from the selection
    sourceInstance = instances[0];
  }

  try {
    console.log("Getting instance information:", sourceInstance);

    // Get component overrides and main component
    const overrides = sourceInstance.overrides || [];
    console.log("Raw Overrides:", overrides);

    // Get main component
    const mainComponent = await sourceInstance.getMainComponentAsync();
    if (!mainComponent) {
      throw new Error("Failed to get main component");
    }

    // Return data to MCP server
    const returnData = {
      success: true,
      message: `Got component information from "${sourceInstance.name}" for overrides.length: ${overrides.length}`,
      sourceInstanceId: sourceInstance.id,
      mainComponentId: mainComponent.id,
      overridesCount: overrides.length
    };

    console.log("Data to return to MCP server:", returnData);
    figma.notify(`Got component information from "${sourceInstance.name}"`);

    return returnData;
  } catch (error: any) {
    console.error("Error in getInstanceOverrides:", error);
    figma.notify(`Error: ${error.message}`);
    throw new Error(`Error: ${error.message}`);
  }
} 