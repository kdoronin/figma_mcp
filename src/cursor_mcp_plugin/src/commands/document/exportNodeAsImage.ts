/// <reference types="@figma/plugin-typings" />

// Export node as image command

export interface ExportNodeAsImageParams {
  nodeId: string;
  format?: string;
  scale?: number;
}

export interface ExportNodeAsImageResult {
  nodeId: string;
  format: string;
  scale: number;
  mimeType: string;
  imageData: string;
  success: boolean;
  timestamp: number;
}

/**
 * Custom base64 encoding function for Uint8Array
 */
function customBase64Encode(bytes: Uint8Array): string {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  let base64 = "";

  const byteLength = bytes.byteLength;
  const byteRemainder = byteLength % 3;
  const mainLength = byteLength - byteRemainder;

  let a: number, b: number, c: number, d: number;
  let chunk: number;

  // Main loop deals with bytes in chunks of 3
  for (let i = 0; i < mainLength; i = i + 3) {
    // Combine the three bytes into a single integer
    chunk = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2];

    // Use bitmasks to extract 6-bit segments from the triplet
    a = (chunk & 16515072) >> 18; // 16515072 = (2^6 - 1) << 18
    b = (chunk & 258048) >> 12; // 258048 = (2^6 - 1) << 12
    c = (chunk & 4032) >> 6; // 4032 = (2^6 - 1) << 6
    d = chunk & 63; // 63 = 2^6 - 1

    // Convert the raw binary segments to the appropriate ASCII encoding
    base64 += chars[a] + chars[b] + chars[c] + chars[d];
  }

  // Deal with the remaining bytes and padding
  if (byteRemainder === 1) {
    chunk = bytes[mainLength];

    a = (chunk & 252) >> 2; // 252 = (2^6 - 1) << 2

    // Set the 4 least significant bits to zero
    b = (chunk & 3) << 4; // 3 = 2^2 - 1

    base64 += chars[a] + chars[b] + "==";
  } else if (byteRemainder === 2) {
    chunk = (bytes[mainLength] << 8) | bytes[mainLength + 1];

    a = (chunk & 64512) >> 10; // 64512 = (2^6 - 1) << 10
    b = (chunk & 1008) >> 4; // 1008 = (2^6 - 1) << 4

    // Set the 2 least significant bits to zero
    c = (chunk & 15) << 2; // 15 = 2^4 - 1

    base64 += chars[a] + chars[b] + chars[c] + "=";
  }

  return base64;
}

/**
 * Get MIME type for export format
 */
function getMimeType(format: string): string {
  switch (format.toUpperCase()) {
    case "PNG":
      return "image/png";
    case "JPG":
    case "JPEG":
      return "image/jpeg";
    case "SVG":
      return "image/svg+xml";
    case "PDF":
      return "application/pdf";
    default:
      return "application/octet-stream";
  }
}

/**
 * Export a node as an image with the specified format and scale
 */
export async function exportNodeAsImage(params: ExportNodeAsImageParams): Promise<ExportNodeAsImageResult> {
  const { nodeId, format = "PNG", scale = 1 } = params;

  if (!nodeId) {
    throw new Error("Missing nodeId parameter");
  }

  const node = await figma.getNodeByIdAsync(nodeId);
  if (!node) {
    throw new Error(`Node not found with ID: ${nodeId}`);
  }

  if (!("exportAsync" in node)) {
    throw new Error(`Node does not support exporting: ${nodeId}`);
  }

  try {
    const upperFormat = format.toUpperCase();
    
    // Handle SVG format differently
    if (upperFormat === "SVG") {
      const svgString = await (node as any).exportAsync({
        format: "SVG_STRING"
      });
      
      return {
        nodeId,
        format: upperFormat,
        scale,
        mimeType: getMimeType(upperFormat),
        imageData: svgString, // SVG is returned as string, not base64
        success: true,
        timestamp: Date.now()
      };
    } else {
      // Handle binary formats (PNG, JPG, PDF)
      const settings = {
        format: upperFormat,
        constraint: { type: "SCALE", value: scale },
      };

      const bytes = await (node as any).exportAsync(settings) as Uint8Array;
      const base64 = customBase64Encode(bytes);

      return {
        nodeId,
        format: upperFormat,
        scale,
        mimeType: getMimeType(upperFormat),
        imageData: base64,
        success: true,
        timestamp: Date.now()
      };
    }
  } catch (error: any) {
    throw new Error(`Error exporting node as image: ${error.message}`);
  }
}
