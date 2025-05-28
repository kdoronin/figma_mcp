/// <reference types="@figma/plugin-typings" />

// Main plugin file - entry point

import { PLUGIN_DIMENSIONS, MESSAGE_TYPES } from './constants';
import { PluginState, UIMessage, CommandMessage } from './types';
import { StorageService } from './services/storage.service';
import { ProgressService } from './services/progress.service';
import { handleCommand } from './handlers/commandHandler';

// Plugin state
const state: PluginState = {
  serverPort: 3055, // Default port
};

// Initialize plugin
async function initializePlugin() {
  try {
    // Load saved settings
    const settings = await StorageService.loadSettings();
    state.serverPort = settings.serverPort;

    // Send initial settings to UI
    figma.ui.postMessage({
      type: MESSAGE_TYPES.INIT_SETTINGS,
      settings: {
        serverPort: state.serverPort,
      },
    });
  } catch (error) {
    console.error("Error loading settings:", error);
  }
}

// Handle messages from UI
async function handleUIMessage(msg: UIMessage) {
  switch (msg.type) {
    case MESSAGE_TYPES.UPDATE_SETTINGS:
      await updateSettings(msg);
      break;
    
    case MESSAGE_TYPES.NOTIFY:
      figma.notify(msg.message);
      break;
    
    case MESSAGE_TYPES.CLOSE_PLUGIN:
      figma.closePlugin();
      break;
    
    case MESSAGE_TYPES.EXECUTE_COMMAND:
      const commandMsg = msg as CommandMessage;
      try {
        const result = await handleCommand(commandMsg.command, commandMsg.params);
        // Send result back to UI
        figma.ui.postMessage({
          type: MESSAGE_TYPES.COMMAND_RESULT,
          id: commandMsg.id,
          result,
        });
      } catch (error: any) {
        figma.ui.postMessage({
          type: MESSAGE_TYPES.COMMAND_ERROR,
          id: commandMsg.id,
          error: error.message || "Error executing command",
        });
      }
      break;
  }
}

// Update plugin settings
async function updateSettings(settings: any) {
  if (settings.serverPort) {
    state.serverPort = settings.serverPort;
  }

  await StorageService.saveSettings({
    serverPort: state.serverPort,
  });
}

// Helper to send progress updates
export function sendProgressUpdate(
  commandId: string,
  commandType: string,
  status: any,
  progress: number,
  totalItems: number,
  processedItems: number,
  message: string,
  payload: any = null
) {
  const update = ProgressService.sendProgressUpdate(
    commandId,
    commandType,
    status,
    progress,
    totalItems,
    processedItems,
    message,
    payload
  );
  
  // Send to UI
  figma.ui.postMessage(update);
  
  return update;
}

// Show UI
figma.showUI(__html__, {
  width: PLUGIN_DIMENSIONS.width,
  height: PLUGIN_DIMENSIONS.height
});

// Set up message handler
figma.ui.onmessage = handleUIMessage;

// Listen for plugin commands from menu
figma.on("run", ({ command }) => {
  figma.ui.postMessage({ type: MESSAGE_TYPES.AUTO_CONNECT });
});

// Initialize plugin on load
initializePlugin();