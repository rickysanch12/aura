import React, { useEffect } from "react";
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Activity, Zap, Brain, Cpu } from "lucide-react";
import { useSystemStore } from "../store/systemStore";
import { useWebSocketClient } from "../hooks/useWebSocket";

const Dashboard: React.FC = () => {
  const { status, agents } = useSystemStore();
  const { send } = useWebSocketClient();

  useEffect(() => {
    // Request status updates
    const interval = setInterval(() => {
      send({ type: "status" });
    }, 5000);

    return () => clearInterval(interval);
  }, [send]);

  // Mock data for charts
  const performanceData = [
    { time: "0m", cpu: 30, memory: 45, gpu: 60 },
    { time: "5m", cpu: 35, memory: 50, gpu: 65 },
    { time: "10m", cpu: 40, memory: 55, gpu: 70 },
    { time: "15m", cpu: 38, memory: 52, gpu: 68 },
    { time: "20m", cpu: 42, memory: 58, gpu: 72 },
  ];

  const agentActivityData = [
    { time: "0m", tasks: 5 },
    { time: "5m", tasks: 8 },
    { time: "10m", tasks: 12 },
    { time: "15m", tasks: 10 },
    { time: "20m", tasks: 15 },
  ];

  const activeAgents = agents.filter((a) => a.is_active).length;
  const totalTasks = agents.reduce((sum, a) => sum + a.stats.tasks_completed, 0);

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">
          System Status: {status?.running ? "🟢 Running" : "🔴 Offline"}
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Agents</p>
              <p className="text-3xl font-bold text-white mt-1">
                {activeAgents}
              </p>
            </div>
            <Zap className="w-8 h-8 text-primary-500 opacity-50" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Tasks Completed</p>
              <p className="text-3xl font-bold text-white mt-1">{totalTasks}</p>
            </div>
            <Activity className="w-8 h-8 text-green-500 opacity-50" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Memory Entries</p>
              <p className="text-3xl font-bold text-white mt-1">
                {status?.memory.total_entries || 0}
              </p>
            </div>
            <Brain className="w-8 h-8 text-purple-500 opacity-50" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">System Uptime</p>
              <p className="text-3xl font-bold text-white mt-1">
                {status?.uptime ? Math.floor(status.uptime / 60) : 0}m
              </p>
            </div>
            <Cpu className="w-8 h-8 text-cyan-500 opacity-50" />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Performance */}
        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">
            System Performance
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis stroke="rgba(255,255,255,0.3)" />
              <YAxis stroke="rgba(255,255,255,0.3)" />
              <Tooltip contentStyle={{ backgroundColor: "rgba(0,0,0,0.8)" }} />
              <Line
                type="monotone"
                dataKey="cpu"
                stroke="#0ea5e9"
                dot={false}
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="memory"
                stroke="#8b5cf6"
                dot={false}
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="gpu"
                stroke="#10b981"
                dot={false}
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Agent Activity */}
        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">
            Agent Activity
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={agentActivityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis stroke="rgba(255,255,255,0.3)" />
              <YAxis stroke="rgba(255,255,255,0.3)" />
              <Tooltip contentStyle={{ backgroundColor: "rgba(0,0,0,0.8)" }} />
              <Area
                type="monotone"
                dataKey="tasks"
                stroke="#0ea5e9"
                fill="rgba(14, 165, 233, 0.1)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Active Agents */}
      <div className="card">
        <h3 className="text-lg font-semibold text-white mb-4">Active Agents</h3>
        <div className="space-y-2">
          {agents.map((agent) => (
            <div
              key={agent.agent_id}
              className="flex items-center justify-between p-3 bg-dark-800/50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                <div
                  className={`w-2 h-2 rounded-full ${
                    agent.is_active ? "bg-green-500 animate-pulse" : "bg-gray-600"
                  }`}
                />
                <div>
                  <p className="font-medium text-white">{agent.name}</p>
                  <p className="text-sm text-gray-400">{agent.type}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-300">
                  {agent.stats.tasks_completed} tasks
                </p>
                <p className="text-xs text-gray-500">Queue: {agent.queue_size}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
