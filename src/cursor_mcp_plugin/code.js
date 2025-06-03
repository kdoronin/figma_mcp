import { state, updateSettings, loadSettings } from "./modules/state.js";
import { handleCommand } from "./modules/commands.js";

figma.showUI(__html__, { width: 350, height: 450 });

figma.ui.onmessage = async (msg) => {
  switch (msg.type) {
    case "update-settings":
      updateSettings(msg);
      break;
    case "notify":
      figma.notify(msg.message);
      break;
    case "close-plugin":
      figma.closePlugin();
      break;
    case "execute-command":
      try {
        const result = await handleCommand(msg.command, msg.params);
        figma.ui.postMessage({
          type: "command-result",
          id: msg.id,
          result,
        });
      } catch (error) {
        figma.ui.postMessage({
          type: "command-error",
          id: msg.id,
          error: error.message || "Error executing command",
        });
      }
      break;
  }
};

figma.on("run", () => {
  figma.ui.postMessage({ type: "auto-connect" });
});

await loadSettings();
figma.ui.postMessage({
  type: "init-settings",
  settings: { serverPort: state.serverPort },
});
