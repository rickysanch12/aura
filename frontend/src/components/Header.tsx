import React, { useEffect, useState } from "react";
import { Bell, Search, Activity } from "lucide-react";
import { useSystemStore } from "../store/systemStore";

const Header: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const { status } = useSystemStore();

  return (
    <header className="h-16 bg-dark-900 border-b border-white/10 px-6 flex items-center justify-between">
      {/* Search bar */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <input
            type="text"
            placeholder="Search agents, models, memory..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 bg-dark-800 border border-white/10 rounded-lg text-gray-300 placeholder-gray-500 focus:outline-none focus:border-primary-500/50"
          />
          <Search className="absolute right-3 top-2.5 w-4 h-4 text-gray-500" />
        </div>
      </div>

      {/* Right side items */}
      <div className="flex items-center space-x-4 ml-6">
        {/* System status */}
        <div className="flex items-center space-x-2">
          <Activity className="w-4 h-4 text-green-500" />
          <span className="text-sm font-medium text-gray-300">
            {status?.running ? "Running" : "Offline"}
          </span>
        </div>

        {/* Uptime */}
        {status?.uptime && (
          <div className="text-sm text-gray-400">
            Uptime: {Math.floor(status.uptime / 60)}m
          </div>
        )}

        {/* Notifications */}
        <button className="p-2 rounded-lg hover:bg-dark-800 text-gray-400 hover:text-gray-300 relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-orange-500 rounded-full animate-pulse" />
        </button>

        {/* User menu */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-cyan-500 cursor-pointer hover:opacity-80 transition-opacity" />
      </div>
    </header>
  );
};

export default Header;
