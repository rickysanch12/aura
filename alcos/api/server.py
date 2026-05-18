"""FastAPI server for ALCOS."""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ..core import get_core_os, AgenticCoreOS
from ..config import get_config

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create FastAPI application."""

    config = get_config()
    app = FastAPI(
        title="Agentic Local Core OS",
        description="Elite local autonomous AI system",
        version="1.0.0",
    )

    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    core_os = get_core_os()

    # ============================================================================
    # HEALTH & STATUS ENDPOINTS
    # ============================================================================

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        status = await core_os.get_status()
        return {
            "status": "healthy" if core_os.is_running else "offline",
            "running": core_os.is_running,
            "version": "1.0.0",
        }

    @app.get("/status")
    async def get_status():
        """Get system status."""
        return await core_os.get_status()

    # ============================================================================
    # INITIALIZATION ENDPOINTS
    # ============================================================================

    @app.post("/init")
    async def initialize():
        """Initialize ALCOS."""
        success = await core_os.initialize()
        if success:
            return {"status": "initialized"}
        raise HTTPException(status_code=500, detail="Initialization failed")

    @app.post("/start")
    async def start(background_tasks: BackgroundTasks):
        """Start ALCOS."""
        background_tasks.add_task(core_os.start)
        return {"status": "starting"}

    @app.post("/stop")
    async def stop():
        """Stop ALCOS."""
        await core_os.stop()
        return {"status": "stopped"}

    # ============================================================================
    # TASK ENDPOINTS
    # ============================================================================

    @app.post("/task")
    async def process_task(task: Dict[str, Any]):
        """Process a task."""
        result = await core_os.process_task(task)
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result)
        return result

    # ============================================================================
    # AGENT ENDPOINTS
    # ============================================================================

    @app.get("/agents")
    async def get_agents():
        """Get all agents."""
        agents = await core_os.get_agents()
        return {"agents": agents}

    @app.get("/agents/{agent_id}")
    async def get_agent(agent_id: str):
        """Get specific agent."""
        agent = await core_os.agent_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return await agent.get_status()

    @app.post("/agents/{agent_id}/task")
    async def submit_task_to_agent(agent_id: str, task: Dict[str, Any]):
        """Submit task to specific agent."""
        agent = await core_os.agent_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        task_id = await agent.queue_task(task)
        return {"task_id": task_id, "agent_id": agent_id}

    # ============================================================================
    # MODEL ENDPOINTS
    # ============================================================================

    @app.get("/models")
    async def get_models():
        """Get available models."""
        models = await core_os.get_available_models()
        return {"models": models}

    @app.get("/models/{model_id}")
    async def get_model(model_id: str):
        """Get model info."""
        info = await core_os.model_manager.get_model_info(model_id)
        if not info:
            raise HTTPException(status_code=404, detail="Model not found")
        return info

    @app.post("/models/{model_id}/load")
    async def load_model(model_id: str):
        """Load a model."""
        success = await core_os.model_manager.load_model(model_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to load model")
        return {"status": "loaded", "model": model_id}

    @app.post("/models/{model_id}/unload")
    async def unload_model(model_id: str):
        """Unload a model."""
        success = await core_os.model_manager.unload_model(model_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to unload model")
        return {"status": "unloaded", "model": model_id}

    # ============================================================================
    # MEMORY ENDPOINTS
    # ============================================================================

    @app.post("/memory")
    async def add_memory(
        content: str,
        memory_type: str = "general",
        project: Optional[str] = None,
        tags: Optional[list] = None,
    ):
        """Add memory entry."""
        doc_id = await core_os.memory_manager.add_memory(
            content=content,
            memory_type=memory_type,
            project=project,
            tags=tags,
        )
        return {"doc_id": doc_id, "status": "added"}

    @app.get("/memory/search")
    async def search_memory(q: str, limit: int = 5):
        """Search memory."""
        results = await core_os.search_memory(q, limit)
        return {"query": q, "results": results}

    @app.get("/memory/stats")
    async def get_memory_stats():
        """Get memory statistics."""
        stats = await core_os.memory_manager.get_memory_stats()
        return stats

    # ============================================================================
    # WEBSOCKET ENDPOINT
    # ============================================================================

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket for real-time updates."""
        await websocket.accept()

        try:
            while True:
                # Receive message
                message = await websocket.receive_text()
                data = json.loads(message)

                # Handle different message types
                if data.get("type") == "task":
                    result = await core_os.process_task(data.get("payload", {}))
                    await websocket.send_json({
                        "type": "task_result",
                        "payload": result,
                    })

                elif data.get("type") == "status":
                    status = await core_os.get_status()
                    await websocket.send_json({
                        "type": "status_update",
                        "payload": status,
                    })

                elif data.get("type") == "memory_search":
                    query = data.get("query", "")
                    results = await core_os.search_memory(query, limit=5)
                    await websocket.send_json({
                        "type": "memory_result",
                        "payload": results,
                    })

                elif data.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": __import__("datetime").datetime.now().isoformat(),
                    })

                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {data.get('type')}",
                    })

        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            await websocket.close()

    return app


async def run_server():
    """Run the API server."""
    config = get_config()
    app = create_app()

    config_dict = {
        "app": app,
        "host": config.settings.api_host,
        "port": config.settings.api_port,
        "workers": 1,  # Single worker for now
        "log_level": config.settings.log_level.lower(),
    }

    server = uvicorn.Server(uvicorn.Config(**config_dict))
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_server())
