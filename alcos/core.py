"""Core orchestration engine for ALCOS."""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, Optional, List
from datetime import datetime

from .config import get_config
from .logger import setup_logging, get_logger
from .memory import MemoryManager, ChromaVectorStore
from .models import ModelManager, ModelRouter
from .executor import CodeExecutor
from .agents import (
    AgentManager,
    PlannerAgent,
    CoderAgent,
    DebuggerAgent,
    ResearcherAgent,
    MonitorAgent,
)

logger = get_logger("alcos.core")


class AgenticCoreOS:
    """Main orchestration engine for ALCOS."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config = get_config()
        self.logger = setup_logging(level=self.config.settings.log_level)

        # Initialize subsystems
        self.memory_store = ChromaVectorStore(
            persist_dir=self.config.settings.memory_dir,
        )
        self.memory_manager = MemoryManager(self.memory_store)

        self.model_manager = ModelManager(
            models_dir=self.config.settings.models_dir,
            ollama_base_url=self.config.settings.ollama_base_url,
        )
        self.model_router = ModelRouter(self.model_manager)

        self.executor = CodeExecutor(
            timeout=self.config.settings.execution_timeout,
            max_concurrent=self.config.settings.max_concurrent_executions,
            enable_docker=self.config.settings.sandbox_isolation == "docker",
        )

        self.agent_manager = AgentManager()

        self.is_running = False
        self.initialized = False
        self.start_time = None

        logger.info("Initialized Agentic Core OS")

    async def initialize(self) -> bool:
        """Initialize all subsystems."""
        try:
            logger.info("Initializing ALCOS...")

            # Register agents
            agents = [
                PlannerAgent(),
                CoderAgent(),
                DebuggerAgent(),
                ResearcherAgent(),
                MonitorAgent(),
            ]

            for agent in agents:
                await self.agent_manager.register_agent(agent)

            logger.info(f"Registered {len(agents)} agents")

            # Load essential models
            essential_models = ["openclaw", "hermes"]
            for model_id in essential_models:
                can_load = await self.model_manager.can_load_model(model_id)
                if can_load:
                    await self.model_manager.load_model(model_id)
                    logger.info(f"Loaded model: {model_id}")

            self.initialized = True
            logger.info("ALCOS initialization complete")
            return True

        except Exception as e:
            logger.error(f"Initialization failed: {e}", exc_info=True)
            return False

    async def start(self) -> None:
        """Start the ALCOS system."""
        if not self.initialized:
            success = await self.initialize()
            if not success:
                logger.error("Cannot start ALCOS: initialization failed")
                return

        self.is_running = True
        self.start_time = datetime.now()

        try:
            # Start all agents
            await self.agent_manager.start_all()

            # Start monitor loop
            monitor_task = asyncio.create_task(self._monitor_loop())

            logger.info("ALCOS started successfully")

        except Exception as e:
            logger.error(f"Failed to start ALCOS: {e}", exc_info=True)
            self.is_running = False

    async def stop(self) -> None:
        """Stop the ALCOS system."""
        if not self.is_running:
            return

        try:
            logger.info("Stopping ALCOS...")

            await self.agent_manager.stop_all()
            await self.executor.cleanup()
            self.memory_store.persist()

            self.is_running = False
            logger.info("ALCOS stopped")

        except Exception as e:
            logger.error(f"Error stopping ALCOS: {e}", exc_info=True)

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task through the system."""
        if not self.is_running:
            return {"error": "ALCOS not running"}

        try:
            task_id = task.get("task_id")
            task_type = task.get("type", "general")

            logger.info(f"Processing task {task_id}: {task_type}")

            # Store in memory
            await self.memory_manager.add_memory(
                str(task),
                memory_type="task",
                tags=["task", task_type],
            )

            # Route to optimal model
            model_id = await self.model_router.route_task(
                task=str(task),
                task_type=task_type,
            )

            # Delegate to agent
            agent_type = task.get("preferred_agent", task_type)
            agents = await self.agent_manager.get_agents_by_type(agent_type)

            if agents:
                agent = agents[0]
                task_queue_id = await agent.queue_task(task)
                result = await agent.process_task(task)
                agent.record_completion(task_queue_id, 0.1)

                return {
                    "status": "success",
                    "task_id": task_id,
                    "model": model_id,
                    "agent": agent.name,
                    "result": result,
                }
            else:
                return {
                    "status": "error",
                    "error": f"No agent found for type: {agent_type}",
                }

        except Exception as e:
            logger.error(f"Error processing task: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
            }

    async def _monitor_loop(self) -> None:
        """Monitor loop for system health."""
        while self.is_running:
            try:
                # Get system status
                agents_status = await self.agent_manager.get_status_report()
                models_status = await self.model_manager.get_available_models()
                memory_stats = await self.memory_manager.get_memory_stats()

                # Log status periodically (every 60 seconds)
                logger.debug(
                    f"System status - Agents: {len(agents_status['agents'])}, "
                    f"Memory entries: {memory_stats['total_entries']}"
                )

                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                await asyncio.sleep(30)

    async def get_status(self) -> Dict[str, Any]:
        """Get system status."""
        uptime = None
        if self.start_time:
            uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "running": self.is_running,
            "initialized": self.initialized,
            "uptime": uptime,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "agents": await self.agent_manager.get_status_report(),
            "memory": await self.memory_manager.get_memory_stats(),
            "timestamp": datetime.now().isoformat(),
        }

    async def search_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search memory."""
        return await self.memory_manager.search_memory(query, limit)

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get available models."""
        return await self.model_manager.get_available_models()

    async def execute_python(
        self,
        code: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute Python code."""
        result = await self.executor.execute_python(code, variables)
        return result.to_dict()

    async def execute_shell(self, command: str) -> Dict[str, Any]:
        """Execute shell command."""
        result = await self.executor.execute_shell(command)
        return result.to_dict()

    async def get_execution_status(self) -> Dict[str, Any]:
        """Get executor status."""
        return self.executor.get_execution_status()

    async def get_agents(self) -> List[Dict[str, Any]]:
        """Get all agents."""
        agents = await self.agent_manager.get_all_agents()
        return [await agent.get_status() for agent in agents]


# Global instance
_core_os: Optional[AgenticCoreOS] = None


def get_core_os() -> AgenticCoreOS:
    """Get or create the core OS instance."""
    global _core_os
    if _core_os is None:
        _core_os = AgenticCoreOS()
    return _core_os
