import React, { useState, useEffect } from "react";
import { Search, Trash2, Copy, Filter, Download } from "lucide-react";
import { useSystemStore } from "../store/systemStore";
import { useWebSocketClient } from "../hooks/useWebSocket";

interface MemoryEntry {
  id: string;
  content: string;
  type: string;
  tags: string[];
  relevance_score: number;
  created_at: string;
  agent_id?: string;
}

const Memory: React.FC = () => {
  const { status } = useSystemStore();
  const { send } = useWebSocketClient();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<MemoryEntry[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedType, setSelectedType] = useState("all");
  const [expandedEntry, setExpandedEntry] = useState<string | null>(null);

  const memoryTypes = [
    { value: "all", label: "All Types" },
    { value: "conversation", label: "Conversations" },
    { value: "task", label: "Tasks" },
    { value: "code", label: "Code" },
    { value: "research", label: "Research" },
    { value: "system", label: "System" },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      send({ type: "status" });
    }, 5000);
    return () => clearInterval(interval);
  }, [send]);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setIsSearching(true);
      send({
        type: "memory_search",
        payload: {
          query: searchQuery,
          limit: 20,
          filters:
            selectedType !== "all" ? { type: selectedType } : undefined,
        },
      });
      setTimeout(() => setIsSearching(false), 1000);
    }
  };

  const handleCopyContent = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  const getTypeColor = (type: string): string => {
    const colors: Record<string, string> = {
      conversation: "bg-blue-500/20 text-blue-300 border border-blue-500/30",
      task: "bg-green-500/20 text-green-300 border border-green-500/30",
      code: "bg-purple-500/20 text-purple-300 border border-purple-500/30",
      research: "bg-orange-500/20 text-orange-300 border border-orange-500/30",
      system: "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30",
    };
    return colors[type] || "bg-gray-500/20 text-gray-300 border border-gray-500/30";
  };

  const getRelevanceColor = (score: number): string => {
    if (score > 0.8) return "text-green-400";
    if (score > 0.6) return "text-yellow-400";
    if (score > 0.4) return "text-orange-400";
    return "text-red-400";
  };

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Memory</h1>
        <p className="text-gray-400">
          Search and manage persistent memory entries
        </p>
      </div>

      {/* Search Section */}
      <div className="card space-y-4">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search memories by content, task, or concept..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSearch();
                }
              }}
              className="w-full px-4 py-3 bg-dark-800 border border-white/10 rounded-lg text-gray-300 placeholder-gray-500 focus:outline-none focus:border-primary-500/50"
            />
            <Search className="absolute right-4 top-3.5 w-5 h-5 text-gray-500" />
          </div>
          <button
            onClick={handleSearch}
            disabled={isSearching}
            className="px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            {isSearching ? "Searching..." : "Search"}
          </button>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3">
          <Filter className="w-4 h-4 text-gray-400" />
          <div className="flex flex-wrap gap-2">
            {memoryTypes.map((type) => (
              <button
                key={type.value}
                onClick={() => setSelectedType(type.value)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  selectedType === type.value
                    ? "bg-primary-500 text-white"
                    : "bg-dark-800 text-gray-400 hover:text-gray-300"
                }`}
              >
                {type.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Memory Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Total Entries</p>
          <p className="text-3xl font-bold text-white">
            {status?.memory.total_entries || 0}
          </p>
        </div>
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Cache Size</p>
          <p className="text-3xl font-bold text-cyan-400">
            {status?.memory.cache_size
              ? `${(status.memory.cache_size / 1024 / 1024).toFixed(1)}MB`
              : "0MB"}
          </p>
        </div>
        <div className="card">
          <p className="text-gray-400 text-sm mb-2">Search Results</p>
          <p className="text-3xl font-bold text-green-400">
            {searchResults.length}
          </p>
        </div>
      </div>

      {/* Search Results */}
      <div className="space-y-4">
        {searchResults.length === 0 && searchQuery ? (
          <div className="card p-8 text-center">
            <p className="text-gray-400">
              No memory entries found for "{searchQuery}"
            </p>
          </div>
        ) : searchResults.length === 0 ? (
          <div className="card p-8 text-center">
            <p className="text-gray-400">Search memories to get started</p>
          </div>
        ) : (
          searchResults.map((entry) => (
            <div key={entry.id} className="card overflow-hidden">
              {/* Entry Header */}
              <div
                className="p-6 flex items-center justify-between cursor-pointer hover:bg-dark-800/30 transition-colors"
                onClick={() =>
                  setExpandedEntry(
                    expandedEntry === entry.id ? null : entry.id
                  )
                }
              >
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span
                      className={`text-xs px-3 py-1 rounded-full capitalize ${getTypeColor(
                        entry.type
                      )}`}
                    >
                      {entry.type}
                    </span>
                    <span
                      className={`text-sm font-semibold ${getRelevanceColor(
                        entry.relevance_score
                      )}`}
                    >
                      Relevance: {(entry.relevance_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="text-gray-300 line-clamp-2">
                    {entry.content}
                  </p>
                  {entry.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3">
                      {entry.tags.map((tag) => (
                        <span
                          key={tag}
                          className="text-xs px-2 py-1 bg-dark-700 text-gray-400 rounded"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <div className="text-right ml-4 text-gray-500 text-sm">
                  {new Date(entry.created_at).toLocaleDateString()}
                </div>
              </div>

              {/* Entry Details (Expanded) */}
              {expandedEntry === entry.id && (
                <div className="border-t border-white/10 p-6 bg-dark-800/30 space-y-4">
                  {/* Full Content */}
                  <div>
                    <p className="text-sm font-medium text-gray-300 mb-2">
                      Content
                    </p>
                    <div className="p-4 bg-dark-700/50 rounded-lg max-h-64 overflow-y-auto">
                      <p className="text-gray-300 font-mono text-sm whitespace-pre-wrap">
                        {entry.content}
                      </p>
                    </div>
                  </div>

                  {/* Metadata */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Created</p>
                      <p className="text-white text-sm">
                        {new Date(entry.created_at).toLocaleString()}
                      </p>
                    </div>
                    {entry.agent_id && (
                      <div>
                        <p className="text-xs text-gray-500 mb-1">Agent ID</p>
                        <p className="text-white text-sm">
                          {entry.agent_id.substring(0, 8)}...
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 border-t border-white/10 pt-4">
                    <button
                      onClick={() => handleCopyContent(entry.content)}
                      className="flex-1 px-4 py-2 bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 border border-blue-500/30 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <Copy className="w-4 h-4" />
                      Copy Content
                    </button>
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

      {/* Export Button */}
      {status?.memory.total_entries ? (
        <div className="text-center">
          <button className="px-6 py-3 bg-dark-800 hover:bg-dark-700 text-gray-300 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 mx-auto border border-white/10">
            <Download className="w-4 h-4" />
            Export Memory
          </button>
        </div>
      ) : null}
    </div>
  );
};

export default Memory;
