const { contextBridge, ipcRenderer } = require("electron");

// Expose IPC methods to the renderer process
contextBridge.exposeInMainWorld("electron", {
  getAppVersion: () => ipcRenderer.invoke("get-app-version"),
  getOSInfo: () => ipcRenderer.invoke("get-os-info"),
  send: (channel, args) => {
    if (["close-window"].includes(channel)) {
      ipcRenderer.send(channel, args);
    }
  },
  receive: (channel, func) => {
    const validChannels = ["update-available", "update-downloaded"];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => func(...args));
    }
  },
});
