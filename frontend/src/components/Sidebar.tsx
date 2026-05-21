import React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Home,
  Zap,
  Cpu,
  Brain,
  Settings,
  Database,
} from "lucide-react";

const Sidebar: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Dashboard", icon: Home },
    { path: "/agents", label: "Agents", icon: Zap },
    { path: "/models", label: "Models", icon: Cpu },
    { path: "/memory", label: "Memory", icon: Brain },
    { path: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-dark-900 border-r border-white/10 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-cyan-500 flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">ALCOS</h1>
            <p className="text-xs text-gray-400">v1.0.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-300 group ${
                isActive
                  ? "bg-primary-500/20 text-primary-400 border border-primary-500/30"
                  : "text-gray-400 hover:bg-dark-800 hover:text-gray-300"
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
              {isActive && (
                <div className="ml-auto w-2 h-2 rounded-full bg-primary-400 animate-pulse" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Status indicator */}
      <div className="p-4 border-t border-white/10">
        <div className="flex items-center space-x-2 px-4 py-3 rounded-lg bg-dark-800/50">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-sm font-medium text-gray-300">System Ready</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
