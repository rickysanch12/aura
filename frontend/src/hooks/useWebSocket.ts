import { useCallback, useRef, useEffect, useState } from "react";
import { useSystemStore } from "../store/systemStore";

export const useWebSocketClient = () => {
  const ws = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const { setSystemStatus, setAgents, setModels } = useSystemStore();

  const initializeConnection = useCallback((url: string) => {
    try {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        console.log("WebSocket connected");
        setConnected(true);

        // Send initial ping
        if (ws.current) {
          ws.current.send(JSON.stringify({ type: "ping" }));
        }
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          switch (data.type) {
            case "status_update":
              setSystemStatus(data.payload);
              break;

            case "agents_update":
              setAgents(data.payload);
              break;

            case "models_update":
              setModels(data.payload);
              break;

            case "pong":
              console.log("Pong received");
              break;

            default:
              console.log("Unknown message type:", data.type);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.current.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      ws.current.onclose = () => {
        console.log("WebSocket disconnected");
        setConnected(false);
        // Attempt reconnect after 3 seconds
        setTimeout(() => initializeConnection(url), 3000);
      };
    } catch (error) {
      console.error("Failed to initialize WebSocket:", error);
    }
  }, []);

  const send = useCallback((message: any) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  const disconnect = useCallback(() => {
    if (ws.current) {
      ws.current.close();
      ws.current = null;
      setConnected(false);
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, []);

  return {
    connected,
    send,
    disconnect,
    initializeConnection,
  };
};
