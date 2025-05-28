/// <reference types="@figma/plugin-typings" />

// Set fill color command

import { Color } from '../../types';

interface SetFillColorParams {
  nodeId: string;
  color: Color;
}

export async function setFillColor(params: SetFillColorParams) {
  const { nodeId, color } = params || {};

  if (!nodeId) {
    throw new Error("Missing nodeId parameter");
  }

  if (!color) {
    throw new Error("Missing color parameter");
  }

  const node = await figma.getNodeByIdAsync(nodeId);
  if (!node) {
    throw new Error(`Node not found with ID: ${nodeId}`);
  }

  if (!("fills" in node)) {
    throw new Error(`Node does not support fills: ${nodeId}`);
  }

  // Create RGBA color
  const rgbColor = {
    r: parseFloat(String(color.r)) || 0,
    g: parseFloat(String(color.g)) || 0,
    b: parseFloat(String(color.b)) || 0,
    a: parseFloat(String(color.a)) || 1,
  };

  // Set fill
  const paintStyle: SolidPaint = {
    type: "SOLID",
    color: {
      r: rgbColor.r,
      g: rgbColor.g,
      b: rgbColor.b,
    },
    opacity: rgbColor.a,
  };

  (node as any).fills = [paintStyle];

  return {
    id: node.id,
    name: node.name,
    fills: [paintStyle],
  };
}