/// <reference types="@figma/plugin-typings" />

// Main command handler

import { COMMANDS } from '../constants';
import { CommandParams, CommandResult } from '../types';

// Import document commands
import { getDocumentInfo, getSelection, getNodeInfo, getNodeChildren, getInstanceOverrides, exportNodeAsImage } from '../commands/document';

// Import create commands  
import { createRectangle, createFrame } from '../commands/create';

// Import style commands
import { setFillColor } from '../commands/style';

export async function handleCommand(command: string, params: CommandParams): Promise<CommandResult> {
  switch (command) {
    // Document commands
    case COMMANDS.GET_DOCUMENT_INFO:
      return await getDocumentInfo();
    
    case COMMANDS.GET_SELECTION:
      return await getSelection();
    
    case COMMANDS.GET_NODE_INFO:
      if (!params || !params.nodeId) {
        throw new Error("Missing nodeId parameter");
      }
      const nodeInfo = await getNodeInfo(params.nodeId);
      if (!nodeInfo) {
        throw new Error(`Failed to get node info for ID: ${params.nodeId}`);
      }
      return nodeInfo;
    
    case COMMANDS.GET_NODE_CHILDREN:
      if (!params || !params.nodeId) {
        throw new Error("Missing nodeId parameter");
      }
      const childrenIds = await getNodeChildren(params.nodeId);
      return childrenIds;
    
    case COMMANDS.GET_INSTANCE_OVERRIDES:
      return await getInstanceOverrides(params?.instanceNodeId);
    
    case COMMANDS.EXPORT_NODE_AS_IMAGE:
      if (!params || !params.nodeId) {
        throw new Error("Missing nodeId parameter");
      }
      return await exportNodeAsImage({
        nodeId: params.nodeId,
        format: params.format,
        scale: params.scale
      });
    
    // Create commands
    case COMMANDS.CREATE_RECTANGLE:
      return await createRectangle(params);
    
    case COMMANDS.CREATE_FRAME:
      return await createFrame(params);
    
    // Style commands
    case COMMANDS.SET_FILL_COLOR:
      return await setFillColor(params as any);
    
    // TODO: Add more commands here as we refactor them
    
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}