import React, { useState, useEffect } from "react";
import { Play, Pause, Trash2, Plus, MoreVertical } from "lucide-react";
import { useSystemStore } from "../store/systemStore";
import { useWebSocketClient } from "../hooks/useWebSocket";

const Agents: React.FC = () => {
  const { agents } = useSystemStore();
  const { send } = useWebSocketClient();
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null);
  const [taskInput, setTaskInput] = useState("");
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      send({ type: "status" });
    }, 5000);
    return () => clearInterval(interval);
  }, [send]);

  const handleSubmitTask = (agentId: string) => {
    if (taskInput.trim()) {
      send({
        type: "task",
        payload: {
          agent_id: agentId,
          task: taskInput,
        },
      });
      setTaskInput("");
      setSelectedAgent(null);
    }
  };

  const agentTypeColors: Record<string, string> = {
    planner: "bg-blue-500/20 text-blue-300 border border-blue-500/30",
    coder: "bg-green-500/20 text-green-300 border border-green-500/30",
    debugger: "bg-red-500/20 text-red-300 border border-red-500/30",
    researcher: "bg-purple-500/20 text-purple-300 border border-purple-500/30",
    monitor: "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30",
  };

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Agents</h1>
        <p className="text-gray-400">
          Manage and monitor autonomous agents
        </p>
      </div>

      {/* Agent List */}
      <div className="space-y-4">
        {agents.length === 0 ? (
          <div className="card p-8 text-center">
            <p className="text-gray-400">No agents available</p>
          </div>
        ) : (
          agents.map((agent) => (
            <div key={agent.agent_id} className="card overflow-hidden">
              {/* Agent Header */}
              <div
                className="p-6 flex items-center justify-between cursor-pointer hover:bg-dark-800/30 transition-colors"
                onClick={() =>
                  setExpandedAgent(
                    expandedAgent === agent.agent_id ? null : agent.agent_id
                  )
                }
              >
                <div className="flex items-center space-x-4 flex-1">
                  <div
                    className={`w-3 h-3 rounded-full ${
                      agent.is_active
                        ? "bg-green-500 animate-pulse"
                        : "bg-gray-600"
                    }`}
                  />
                  <div>
                    <h3 className="text-lg font-semibold text-white">
                      {agent.name}
                    </h3>
                    <div className="flex items-center space-x-3 mt-2">
                      <span
                        className={`text-xs px-3 py-1 rounded-full ${
                          agentTypeColors[agent.type.toLowerCase()] ||
                          "bg-gray-500/20 text-gray-300"
                        }`}
                      >
                        {agent.type}
                      </span>
                      <span className="text-xs text-gray-500">
                        ID: {agent.agent_id.substring(0, 8)}...
                      </span>
                    </div>
                  </div>
                </div>

                <div className="text-right mr-4">
                  <p className="text-sm text-gray-300">
                    {agent.stats.tasks_completed || 0} tasks completed
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Queue: {agent.queue_size}
                  </p>
                </div>

                <button className="p-2 rounded-lg hover:bg-dark-800 text-gray-400 hover:text-gray-300">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>

              {/* Agent Details (Expanded) */}
              {expandedAgent === agent.agent_id && (
                <div className="border-t border-white/10 p-6 bg-dark-800/30 space-y-6">
                  {/* Stats Grid */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Status</p>
                      <p className="text-white font-semibold">
                        {agent.is_active ? "Active" : "Inactive"}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Created</p>
                      <p className="text-white font-semibold text-sm">
                        {new Date(agent.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Queue Size</p>
                      <p className="text-white font-semibold">
                        {agent.queue_size} task{agent.queue_size !== 1 ? "s" : ""}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Success Rate</p>
                      <p className="text-white font-semibold">
                        {agent.stats.success_rate
                          ? `${Math.round(agent.stats.success_rate * 100)}%`
                          : "N/A"}
                      </p>
                    </div>
                  </div>

                  {/* Task Submission */}
                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-300">
                      Submit New Task
                    </label>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        placeholder="Describe the task..."
                        value={selectedAgent === agent.agent_id ? taskInput : ""}
                        onChange={(e) => {
                          setSelectedAgent(agent.agent_id);
                          setTaskInput(e.target.value);
                        }}
                        onKeyPress={(e) => {
                          if (e.key === "Enter") {
                            handleSubmitTask(agent.agent_id);
                          }
                        }}
                        className="flex-1 px-4 py-2 bg-dark-700 border border-white/10 rounded-lg text-gray-300 placeholder-gray-500 focus:outline-none focus:border-primary-500/50"
                      />
                      <button
                        onClick={() => handleSubmitTask(agent.agent_id)}
                        className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Submit
                      </button>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <button
                      className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 ${
                        agent.is_active
                          ? "bg-red-500/20 text-red-300 hover:bg-red-500/30 border border-red-500/30"
                          : "bg-green-500/20 text-green-300 hover:bg-green-500/30 border border-green-500/30"
                      }`}
                    >
                      {agent.is_active ? (
                        <>
                          <Pause className="w-4 h-4" />
                          Stop Agent
                        </>
                      ) : (
                        <>
                          <Play className="w-4 h-4" />
                          Start Agent
                        </>
                      )}
                    </button>
                    <button className="px-4 py-2 bg-red-500/20 text-red-300 hover:bg-red-500/30 border border-red-500/30 rounded-lg font-medium transition-colors flex items-center gap-2">
                      <Trash2 className="w-4 h-4" />
                      Remove
                    </button>
                  </div>

                  {/* Agent Stats Detail */}
                  {agent.stats && Object.keys(agent.stats).length > 0 && (
                    <div className="border-t border-white/10 pt-4">
                      <p className="text-sm font-medium text-gray-300 mb-3">
                        Statistics
                      </p>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {Object.entries(agent.stats).map(([key, value]) => (
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
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Total Agents</p>
          <p className="text-3xl font-bold text-white">{agents.length}</p>
        </div>
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Active Agents</p>
          <p className="text-3xl font-bold text-white">
            {agents.filter((a) => a.is_active).length}
          </p>
        </div>
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Pending Tasks</p>
          <p className="text-3xl font-bold text-white">
            {agents.reduce((sum, a) => sum + a.queue_size, 0)}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Agents;
