import create from "zustand";

interface Agent {
  agent_id: string;
  name: string;
  type: string;
  is_active: boolean;
  queue_size: number;
  stats: Record<string, any>;
  created_at: string;
}

interface Model {
  id: string;
  name: string;
  type: string;
  size: string;
  vram: number;
  is_loaded: boolean;
  is_downloaded: boolean;
  supports_tools: boolean;
  supports_vision: boolean;
  stats: Record<string, any>;
}

interface SystemStatus {
  running: boolean;
  initialized: boolean;
  uptime: number | null;
  start_time: string | null;
  agents: {
    total_agents: number;
    active_agents: number;
    agents: Agent[];
  };
  memory: {
    total_entries: number;
    cache_size: number;
    timestamp: string;
  };
  timestamp: string;
}

interface SystemStore {
  status: SystemStatus | null;
  agents: Agent[];
  models: Model[];
  setSystemStatus: (status: SystemStatus) => void;
  setAgents: (agents: Agent[]) => void;
  setModels: (models: Model[]) => void;
  updateAgent: (agentId: string, updates: Partial<Agent>) => void;
  updateModel: (modelId: string, updates: Partial<Model>) => void;
}

export const useSystemStore = create<SystemStore>((set) => ({
  status: null,
  agents: [],
  models: [],

  setSystemStatus: (status) =>
    set({
      status,
      agents: status.agents.agents,
    }),

  setAgents: (agents) => set({ agents }),

  setModels: (models) => set({ models }),

  updateAgent: (agentId, updates) =>
    set((state) => ({
      agents: state.agents.map((a) =>
        a.agent_id === agentId ? { ...a, ...updates } : a
      ),
    })),

  updateModel: (modelId, updates) =>
    set((state) => ({
      models: state.models.map((m) =>
        m.id === modelId ? { ...m, ...updates } : m
      ),
    })),
}));
