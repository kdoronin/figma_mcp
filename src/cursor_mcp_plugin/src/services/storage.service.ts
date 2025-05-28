// Storage service for plugin settings and data

import { PluginState } from '../types';
import { DEFAULT_SERVER_PORT } from '../constants';

export class StorageService {
  static async loadSettings(): Promise<PluginState> {
    try {
      const savedSettings = await figma.clientStorage.getAsync("settings");
      if (savedSettings) {
        return {
          serverPort: savedSettings.serverPort || DEFAULT_SERVER_PORT,
        };
      }
    } catch (error) {
      console.error("Error loading settings:", error);
    }

    return {
      serverPort: DEFAULT_SERVER_PORT,
    };
  }

  static async saveSettings(settings: Partial<PluginState>): Promise<void> {
    try {
      const currentSettings = await this.loadSettings();
      const updatedSettings = { ...currentSettings, ...settings };
      await figma.clientStorage.setAsync("settings", updatedSettings);
    } catch (error) {
      console.error("Error saving settings:", error);
    }
  }

  static async setDefaultConnector(connectorId: string): Promise<void> {
    await figma.clientStorage.setAsync('defaultConnectorId', connectorId);
  }

  static async getDefaultConnector(): Promise<string | null> {
    try {
      return await figma.clientStorage.getAsync('defaultConnectorId');
    } catch (error) {
      console.error("Error getting default connector:", error);
      return null;
    }
  }
}