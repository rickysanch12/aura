import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Agents from "./pages/Agents";
import Models from "./pages/Models";
import Memory from "./pages/Memory";
import Settings from "./pages/Settings";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import { useSystemStore } from "./store/systemStore";
import { useWebSocketClient } from "./hooks/useWebSocket";

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const { initializeConnection } = useWebSocketClient();
  const { setSystemStatus } = useSystemStore();

  useEffect(() => {
    const initialize = async () => {
      try {
        // Initialize WebSocket connection
        initializeConnection("ws://localhost:8000/ws");
        setIsLoading(false);
      } catch (error) {
        console.error("Initialization error:", error);
        setIsLoading(false);
      }
    };

    initialize();
  }, []);

  if (isLoading) {
    return (
      <div className="w-full h-screen bg-gradient-to-br from-dark-950 to-dark-900 flex items-center justify-center">
        <div className="text-center">
          <div className="mb-4 flex justify-center">
            <div className="w-12 h-12 rounded-full border-4 border-primary-500/20 border-t-primary-500 animate-spin"></div>
          </div>
          <h1 className="text-2xl font-bold text-white">Initializing ALCOS</h1>
          <p className="text-gray-400 mt-2">Starting autonomous systems...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="flex h-screen bg-dark-950 text-gray-100 overflow-hidden">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <Header />
          <main className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/agents" element={<Agents />} />
              <Route path="/models" element={<Models />} />
              <Route path="/memory" element={<Memory />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
