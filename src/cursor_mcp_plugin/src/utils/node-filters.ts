// Node filtering utilities

import { rgbaToHex } from './helpers';

interface FilteredNode {
  id: string;
  name: string;
  type: string;
  fills?: any[];
  strokes?: any[];
  cornerRadius?: number;
  absoluteBoundingBox?: any;
  characters?: string;
  style?: any;
  children?: FilteredNode[];
  
  // Layout positioning properties
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  
  // Transform matrices
  relativeTransform?: any;
  absoluteTransform?: any;
  absoluteRenderBounds?: any;
  
  // Layout constraints
  constraints?: any;
  
  // Auto-layout properties
  layoutAlign?: 'MIN' | 'CENTER' | 'MAX' | 'STRETCH' | 'INHERIT';
  layoutGrow?: number;
  layoutPositioning?: 'AUTO' | 'ABSOLUTE';
  
  // Size constraints
  minWidth?: number | null;
  maxWidth?: number | null;
  minHeight?: number | null;
  maxHeight?: number | null;
  
  // Grid layout properties
  gridRowAnchorIndex?: number;
  gridColumnAnchorIndex?: number;
  gridRowSpan?: number;
  gridColumnSpan?: number;
}

export function filterFigmaNode(node: any): FilteredNode | null {
  if (node.type === "VECTOR") {
    return null;
  }

  const filtered: FilteredNode = {
    id: node.id,
    name: node.name,
    type: node.type,
  };

  if (node.fills && node.fills.length > 0) {
    filtered.fills = node.fills.map((fill: any) => {
      const processedFill = Object.assign({}, fill);
      delete processedFill.boundVariables;
      delete processedFill.imageRef;

      if (processedFill.gradientStops) {
        processedFill.gradientStops = processedFill.gradientStops.map(
          (stop: any) => {
            const processedStop = Object.assign({}, stop);
            if (processedStop.color) {
              processedStop.color = rgbaToHex(processedStop.color);
            }
            delete processedStop.boundVariables;
            return processedStop;
          }
        );
      }

      if (processedFill.color) {
        processedFill.color = rgbaToHex(processedFill.color);
      }

      return processedFill;
    });
  }

  if (node.strokes && node.strokes.length > 0) {
    filtered.strokes = node.strokes.map((stroke: any) => {
      const processedStroke = Object.assign({}, stroke);
      delete processedStroke.boundVariables;
      if (processedStroke.color) {
        processedStroke.color = rgbaToHex(processedStroke.color);
      }
      return processedStroke;
    });
  }

  if (node.cornerRadius !== undefined) {
    filtered.cornerRadius = node.cornerRadius;
  }

  if (node.absoluteBoundingBox) {
    filtered.absoluteBoundingBox = node.absoluteBoundingBox;
  }

  if (node.characters) {
    filtered.characters = node.characters;
  }

  if (node.style) {
    filtered.style = {
      fontFamily: node.style.fontFamily,
      fontStyle: node.style.fontStyle,
      fontWeight: node.style.fontWeight,
      fontSize: node.style.fontSize,
      textAlignHorizontal: node.style.textAlignHorizontal,
      letterSpacing: node.style.letterSpacing,
      lineHeightPx: node.style.lineHeightPx,
    };
  }

  // Layout positioning properties
  if (node.x !== undefined) {
    filtered.x = node.x;
  }

  if (node.y !== undefined) {
    filtered.y = node.y;
  }

  if (node.width !== undefined) {
    filtered.width = node.width;
  }

  if (node.height !== undefined) {
    filtered.height = node.height;
  }

  // Transform matrices
  if (node.relativeTransform) {
    filtered.relativeTransform = node.relativeTransform;
  }

  if (node.absoluteTransform) {
    filtered.absoluteTransform = node.absoluteTransform;
  }

  if (node.absoluteRenderBounds) {
    filtered.absoluteRenderBounds = node.absoluteRenderBounds;
  }

  // Layout constraints
  if (node.constraints) {
    filtered.constraints = node.constraints;
  }

  // Auto-layout properties
  if (node.layoutAlign) {
    filtered.layoutAlign = node.layoutAlign;
  }

  if (node.layoutGrow !== undefined) {
    filtered.layoutGrow = node.layoutGrow;
  }

  if (node.layoutPositioning) {
    filtered.layoutPositioning = node.layoutPositioning;
  }

  // Size constraints
  if (node.minWidth !== undefined) {
    filtered.minWidth = node.minWidth;
  }

  if (node.maxWidth !== undefined) {
    filtered.maxWidth = node.maxWidth;
  }

  if (node.minHeight !== undefined) {
    filtered.minHeight = node.minHeight;
  }

  if (node.maxHeight !== undefined) {
    filtered.maxHeight = node.maxHeight;
  }

  // Grid layout properties
  if (node.gridRowAnchorIndex !== undefined) {
    filtered.gridRowAnchorIndex = node.gridRowAnchorIndex;
  }

  if (node.gridColumnAnchorIndex !== undefined) {
    filtered.gridColumnAnchorIndex = node.gridColumnAnchorIndex;
  }

  if (node.gridRowSpan !== undefined) {
    filtered.gridRowSpan = node.gridRowSpan;
  }

  if (node.gridColumnSpan !== undefined) {
    filtered.gridColumnSpan = node.gridColumnSpan;
  }

  if (node.children) {
    filtered.children = node.children
      .map((child: any) => filterFigmaNode(child))
      .filter((child: any) => child !== null);
  }

  return filtered;
}