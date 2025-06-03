export const state = {
  serverPort: 3055,
};

export async function loadSettings() {
  try {
    const savedSettings = await figma.clientStorage.getAsync("settings");
    if (savedSettings && savedSettings.serverPort) {
      state.serverPort = savedSettings.serverPort;
    }
  } catch (error) {
    console.error("Error loading settings:", error);
  }
}

export async function updateSettings(settings) {
  if (settings.serverPort) {
    state.serverPort = settings.serverPort;
  }
  await figma.clientStorage.setAsync("settings", {
    serverPort: state.serverPort,
  });
}
