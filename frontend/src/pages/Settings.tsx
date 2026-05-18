import React, { useState, useEffect } from "react";
import {
  Save,
  RotateCcw,
  Settings as SettingsIcon,
  Database,
  Zap,
  Shield,
} from "lucide-react";
import { useSystemStore } from "../store/systemStore";
import { useWebSocketClient } from "../hooks/useWebSocket";

interface SettingsForm {
  apiHost: string;
  apiPort: number;
  maxAgents: number;
  maxQueueSize: number;
  enableGpu: boolean;
  gpuMemory: number;
  memoryCompactInterval: number;
  autoSaveInterval: number;
  logLevel: string;
}

const Settings: React.FC = () => {
  const { status } = useSystemStore();
  const { send } = useWebSocketClient();
  const [settings, setSettings] = useState<SettingsForm>({
    apiHost: "localhost",
    apiPort: 8000,
    maxAgents: 10,
    maxQueueSize: 100,
    enableGpu: true,
    gpuMemory: 24,
    memoryCompactInterval: 3600,
    autoSaveInterval: 300,
    logLevel: "INFO",
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      send({ type: "status" });
    }, 5000);
    return () => clearInterval(interval);
  }, [send]);

  const handleSettingChange = (
    key: keyof SettingsForm,
    value: string | number | boolean
  ) => {
    setSettings((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleSaveSettings = () => {
    setIsSaving(true);
    send({
      type: "task",
      payload: {
        action: "update_settings",
        settings,
      },
    });
    setTimeout(() => {
      setIsSaving(false);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    }, 1000);
  };

  const handleResetSettings = () => {
    setSettings({
      apiHost: "localhost",
      apiPort: 8000,
      maxAgents: 10,
      maxQueueSize: 100,
      enableGpu: true,
      gpuMemory: 24,
      memoryCompactInterval: 3600,
      autoSaveInterval: 300,
      logLevel: "INFO",
    });
  };

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Settings</h1>
        <p className="text-gray-400">Configure system parameters and preferences</p>
      </div>

      {/* Success Message */}
      {saveSuccess && (
        <div className="p-4 bg-green-500/20 border border-green-500/30 rounded-lg text-green-300 flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-green-400" />
          Settings saved successfully
        </div>
      )}

      {/* Settings Sections */}
      <div className="space-y-6">
        {/* API Configuration */}
        <div className="card space-y-6">
          <div className="flex items-center gap-3 pb-4 border-b border-white/10">
            <SettingsIcon className="w-5 h-5 text-primary-400" />
            <h2 className="text-xl font-semibold text-white">API Configuration</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                API Host
              </label>
              <input
                type="text"
                value={settings.apiHost}
                onChange={(e) =>
                  handleSettingChange("apiHost", e.target.value)
                }
                className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-primary-500/50"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                API Port
              </label>
              <input
                type="number"
                value={settings.apiPort}
                onChange={(e) =>
                  handleSettingChange("apiPort", parseInt(e.target.value))
                }
                className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-primary-500/50"
              />
            </div>
          </div>
        </div>

        {/* Agent Configuration */}
        <div className="card space-y-6">
          <div className="flex items-center gap-3 pb-4 border-b border-white/10">
            <Zap className="w-5 h-5 text-yellow-400" />
            <h2 className="text-xl font-semibold text-white">Agent Configuration</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Maximum Agents
              </label>
              <input
                type="number"
                value={settings.maxAgents}
                onChange={(e) =>
                  handleSettingChange("maxAgents", parseInt(e.target.value))
                }
                className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-primary-500/50"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Max Queue Size
              </label>
              <input
                type="number"
                value={settings.maxQueueSize}
                onChange={(e) =>
                  handleSettingChange("maxQueueSize", parseInt(e.target.value))
                }
                className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-primary-500/50"
              />
            </div>
          </div>
        </div>

        {/* GPU Configuration */}
        <div className="card space-y-6">
          <div className="flex items-center gap-3 pb-4 border-b border-white/10">
            <Shield className="w-5 h-5 text-cyan-400" />
            <h2 className="text-xl font-semibold text-white">GPU Configuration</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-300">
                Enable GPU Acceleration
              </label>
              <button
                onClick={() =>
                  handleSettingChange("enableGpu", !settings.enableGpu)
                }
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.enableGpu
                    ? "bg-green-500"
                    : "bg-gray-600"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.enableGpu ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>

            {settings.enableGpu && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  GPU Memory Allocation (GB)
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min="1"
                    max="48"
                    value={settings.gpuMemory}
                    onChange={(e) =>
                      handleSettingChange("gpuMemory", parseInt(e.target.value))
                    }
                    className="w-full"
                  />
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">1GB</span>
                    <span className="text-primary-400 font-semibold">
                      {settings.gpuMemory}GB
                    </span>
                    <span className="text-gray-400">48GB</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Memory Configuration */}
        <div className="card space-y-6">
          <div className="flex items-center gap-3 pb-4 border-b border-white/10">
            <Database className="w-5 h-5 text-purple-400" />
            <h2 className="text-xl font-semibold text-white">Memory Configuration</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Memory Compact Interval (seconds)
              </label>
              <input
                type="number"
                value={settings.memoryCompactInterval}
                onChange={(e) =>
                  handleSettingChange(
                    "memoryCompactInterval",
                    parseInt(e.target.value)
                  )
                }
                className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-primary-500/50"
              />
              <p className="text-xs text-gray-500 mt-1">
                {(settings.memoryCompactInterval / 60).toFixed(1)} minutes
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Auto-Save Interval (seconds)
              </label>
              <input
                type="number"
                value={settings.autoSaveInterval}
                onChange={(e) =>
                  handleSettingChange(
                    "autoSaveInterval",
                    parseInt(e.target.value)
                  )
                }
                className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-primary-500/50"
              />
              <p className="text-xs text-gray-500 mt-1">
                {(settings.autoSaveInterval / 60).toFixed(1)} minutes
              </p>
            </div>
          </div>
        </div>

        {/* Logging Configuration */}
        <div className="card space-y-6">
          <div className="flex items-center gap-3 pb-4 border-b border-white/10">
            <SettingsIcon className="w-5 h-5 text-orange-400" />
            <h2 className="text-xl font-semibold text-white">Logging</h2>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Log Level
            </label>
            <select
              value={settings.logLevel}
              onChange={(e) =>
                handleSettingChange("logLevel", e.target.value)
              }
              className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 focus:outline-none focus:border-primary-500/50"
            >
              <option value="DEBUG">Debug</option>
              <option value="INFO">Info</option>
              <option value="WARNING">Warning</option>
              <option value="ERROR">Error</option>
              <option value="CRITICAL">Critical</option>
            </select>
          </div>
        </div>
      </div>

      {/* System Information */}
      <div className="card space-y-4">
        <h3 className="text-lg font-semibold text-white">System Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-dark-800/50 rounded-lg">
            <p className="text-xs text-gray-500 mb-1">System Status</p>
            <p className="text-white font-semibold">
              {status?.running ? "🟢 Running" : "🔴 Offline"}
            </p>
          </div>
          <div className="p-4 bg-dark-800/50 rounded-lg">
            <p className="text-xs text-gray-500 mb-1">System Uptime</p>
            <p className="text-white font-semibold">
              {status?.uptime ? `${Math.floor(status.uptime / 60)}m` : "N/A"}
            </p>
          </div>
          <div className="p-4 bg-dark-800/50 rounded-lg">
            <p className="text-xs text-gray-500 mb-1">Total Memory Entries</p>
            <p className="text-white font-semibold">
              {status?.memory.total_entries || 0}
            </p>
          </div>
          <div className="p-4 bg-dark-800/50 rounded-lg">
            <p className="text-xs text-gray-500 mb-1">Cache Size</p>
            <p className="text-white font-semibold">
              {status?.memory.cache_size
                ? `${(status.memory.cache_size / 1024 / 1024).toFixed(1)}MB`
                : "0MB"}
            </p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4">
        <button
          onClick={handleSaveSettings}
          disabled={isSaving}
          className="flex-1 px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <Save className="w-5 h-5" />
          {isSaving ? "Saving..." : "Save Settings"}
        </button>
        <button
          onClick={handleResetSettings}
          className="flex-1 px-6 py-3 bg-dark-800 hover:bg-dark-700 text-gray-300 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 border border-white/10"
        >
          <RotateCcw className="w-5 h-5" />
          Reset to Default
        </button>
      </div>
    </div>
  );
};

export default Settings;
