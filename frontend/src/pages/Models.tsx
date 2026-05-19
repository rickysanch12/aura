import React, { useState, useEffect } from "react";
import {
  Download,
  Trash2,
  Zap,
  Eye,
  Code,
  ImageIcon,
  MoreVertical,
} from "lucide-react";
import { useSystemStore } from "../store/systemStore";
import { useWebSocketClient } from "../hooks/useWebSocket";

const Models: React.FC = () => {
  const { models } = useSystemStore();
  const { send } = useWebSocketClient();
  const [expandedModel, setExpandedModel] = useState<string | null>(null);
  const [loadingModelId, setLoadingModelId] = useState<string | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      send({ type: "status" });
    }, 5000);
    return () => clearInterval(interval);
  }, [send]);

  const handleLoadModel = (modelId: string) => {
    setLoadingModelId(modelId);
    send({
      type: "task",
      payload: {
        action: "load_model",
        model_id: modelId,
      },
    });
  };

  const handleUnloadModel = (modelId: string) => {
    setLoadingModelId(modelId);
    send({
      type: "task",
      payload: {
        action: "unload_model",
        model_id: modelId,
      },
    });
  };

  const handleDownloadModel = (modelId: string) => {
    setLoadingModelId(modelId);
    send({
      type: "task",
      payload: {
        action: "download_model",
        model_id: modelId,
      },
    });
  };

  const getModelSizeColor = (size: string): string => {
    const sizeNum = parseInt(size);
    if (sizeNum < 7) return "text-green-400";
    if (sizeNum < 13) return "text-yellow-400";
    if (sizeNum < 35) return "text-orange-400";
    return "text-red-400";
  };

  const getVramPercentage = (vram: number): number => {
    // Assuming 24GB GPU (typical for local models)
    return Math.min((vram / 24) * 100, 100);
  };

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Models</h1>
        <p className="text-gray-400">
          Manage and monitor AI models
        </p>
      </div>

      {/* Models Grid */}
      <div className="space-y-4">
        {models.length === 0 ? (
          <div className="card p-8 text-center">
            <p className="text-gray-400">No models available</p>
          </div>
        ) : (
          models.map((model) => (
            <div key={model.id} className="card overflow-hidden">
              {/* Model Header */}
              <div
                className="p-6 flex items-center justify-between cursor-pointer hover:bg-dark-800/30 transition-colors"
                onClick={() =>
                  setExpandedModel(
                    expandedModel === model.id ? null : model.id
                  )
                }
              >
                <div className="flex items-center space-x-4 flex-1">
                  <div
                    className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                      model.is_loaded
                        ? "bg-green-500/20"
                        : "bg-gray-700/30"
                    }`}
                  >
                    <Zap className={`w-6 h-6 ${model.is_loaded ? "text-green-400" : "text-gray-500"}`} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">
                      {model.name}
                    </h3>
                    <div className="flex items-center space-x-3 mt-2">
                      <span className="text-xs px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30">
                        {model.type}
                      </span>
                      <span
                        className={`text-xs px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 ${getModelSizeColor(
                          model.size
                        )}`}
                      >
                        {model.size}B
                      </span>
                      {model.is_loaded && (
                        <span className="text-xs px-3 py-1 rounded-full bg-green-500/20 text-green-300 border border-green-500/30">
                          Loaded
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="text-right mr-4">
                  <p className="text-sm text-gray-300">
                    VRAM: {model.vram.toFixed(1)}GB
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Downloaded: {model.is_downloaded ? "Yes" : "No"}
                  </p>
                </div>

                <button className="p-2 rounded-lg hover:bg-dark-800 text-gray-400 hover:text-gray-300">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>

              {/* Model Details (Expanded) */}
              {expandedModel === model.id && (
                <div className="border-t border-white/10 p-6 bg-dark-800/30 space-y-6">
                  {/* Capabilities */}
                  <div>
                    <p className="text-sm font-medium text-gray-300 mb-3">
                      Capabilities
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {model.supports_tools && (
                        <div className="flex items-center gap-2 px-3 py-2 bg-blue-500/20 text-blue-300 border border-blue-500/30 rounded-lg text-xs">
                          <Code className="w-4 h-4" />
                          Tool Use
                        </div>
                      )}
                      {model.supports_vision && (
                        <div className="flex items-center gap-2 px-3 py-2 bg-purple-500/20 text-purple-300 border border-purple-500/30 rounded-lg text-xs">
                          <ImageIcon className="w-4 h-4" />
                          Vision
                        </div>
                      )}
                      <div className="flex items-center gap-2 px-3 py-2 bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 rounded-lg text-xs">
                        <Eye className="w-4 h-4" />
                        Context: 4K
                      </div>
                    </div>
                  </div>

                  {/* VRAM Usage */}
                  <div>
                    <p className="text-sm font-medium text-gray-300 mb-2">
                      VRAM Allocation
                    </p>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-400">
                          {model.vram.toFixed(1)}GB / 24GB
                        </span>
                        <span className="text-gray-500">
                          {getVramPercentage(model.vram).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-dark-700 rounded-full h-2 overflow-hidden">
                        <div
                          className={`h-full transition-all ${
                            getVramPercentage(model.vram) > 80
                              ? "bg-red-500"
                              : getVramPercentage(model.vram) > 50
                              ? "bg-yellow-500"
                              : "bg-green-500"
                          }`}
                          style={{
                            width: `${getVramPercentage(model.vram)}%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Stats */}
                  {model.stats && Object.keys(model.stats).length > 0 && (
                    <div className="border-t border-white/10 pt-4">
                      <p className="text-sm font-medium text-gray-300 mb-3">
                        Statistics
                      </p>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {Object.entries(model.stats).map(([key, value]) => (
                          <div
                            key={key}
                            className="p-3 bg-dark-700/50 rounded-lg"
                          >
                            <p className="text-xs text-gray-500 capitalize mb-1">
                              {key.replace(/_/g, " ")}
                            </p>
                            <p className="text-white font-semibold">
                              {typeof value === "number"
                                ? value.toFixed(2)
                                : String(value)}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex gap-2 border-t border-white/10 pt-6">
                    {!model.is_downloaded ? (
                      <button
                        onClick={() => handleDownloadModel(model.id)}
                        disabled={loadingModelId === model.id}
                        className="flex-1 px-4 py-2 bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 border border-blue-500/30 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                      >
                        <Download className="w-4 h-4" />
                        {loadingModelId === model.id
                          ? "Downloading..."
                          : "Download & Load"}
                      </button>
                    ) : model.is_loaded ? (
                      <button
                        onClick={() => handleUnloadModel(model.id)}
                        disabled={loadingModelId === model.id}
                        className="flex-1 px-4 py-2 bg-red-500/20 text-red-300 hover:bg-red-500/30 border border-red-500/30 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                      >
                        <Download className="w-4 h-4" />
                        {loadingModelId === model.id
                          ? "Unloading..."
                          : "Unload Model"}
                      </button>
                    ) : (
                      <button
                        onClick={() => handleLoadModel(model.id)}
                        disabled={loadingModelId === model.id}
                        className="flex-1 px-4 py-2 bg-green-500/20 text-green-300 hover:bg-green-500/30 border border-green-500/30 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                      >
                        <Download className="w-4 h-4" />
                        {loadingModelId === model.id
                          ? "Loading..."
                          : "Load Model"}
                      </button>
                    )}
                    <button className="px-4 py-2 bg-red-500/20 text-red-300 hover:bg-red-500/30 border border-red-500/30 rounded-lg font-medium transition-colors flex items-center gap-2">
                      <Trash2 className="w-4 h-4" />
                      Delete
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Total Models</p>
          <p className="text-3xl font-bold text-white">{models.length}</p>
        </div>
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Loaded</p>
          <p className="text-3xl font-bold text-green-400">
            {models.filter((m) => m.is_loaded).length}
          </p>
        </div>
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Total VRAM Used</p>
          <p className="text-3xl font-bold text-cyan-400">
            {models
              .filter((m) => m.is_loaded)
              .reduce((sum, m) => sum + m.vram, 0)
              .toFixed(1)}
            GB
          </p>
        </div>
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Downloaded</p>
          <p className="text-3xl font-bold text-blue-400">
            {models.filter((m) => m.is_downloaded).length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Models;
