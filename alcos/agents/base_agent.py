"""Base agent class."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(
        self,
        name: str,
        agent_type: str,
        description: str = "",
        model: str = "openclaw",
    ):
        self.agent_id = str(uuid.uuid4())
        self.name = name
        self.agent_type = agent_type
        self.description = description
        self.model = model
        self.created_at = datetime.now()
        self.is_active = False
        self.task_queue = []
        self.completed_tasks = []
        self.stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_completion_time": 0.0,
            "total_tokens_used": 0,
        }

    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task."""
        pass

    async def start(self) -> None:
        """Start the agent."""
        self.is_active = True
        logger.info(f"Started agent: {self.name} ({self.agent_id})")

    async def stop(self) -> None:
        """Stop the agent."""
        self.is_active = False
        logger.info(f"Stopped agent: {self.name} ({self.agent_id})")

    async def queue_task(self, task: Dict[str, Any]) -> str:
        """Queue a task."""
        task_id = str(uuid.uuid4())
        task["task_id"] = task_id
        task["created_at"] = datetime.now().isoformat()
        self.task_queue.append(task)
        logger.debug(f"Queued task {task_id} for {self.name}")
        return task_id

    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.agent_type,
            "is_active": self.is_active,
            "queue_size": len(self.task_queue),
            "stats": self.stats,
            "created_at": self.created_at.isoformat(),
        }

    async def get_memory_context(self) -> str:
        """Get agent memory context."""
        return f"Agent {self.name} ({self.agent_type}): {len(self.completed_tasks)} tasks completed"

    def record_completion(self, task_id: str, duration: float, tokens: int = 0) -> None:
        """Record task completion."""
        self.stats["tasks_completed"] += 1
        self.stats["total_tokens_used"] += tokens
        # Update average completion time
        old_avg = self.stats["average_completion_time"]
        total = self.stats["tasks_completed"]
        self.stats["average_completion_time"] = (old_avg * (total - 1) + duration) / total

    def record_failure(self) -> None:
        """Record task failure."""
        self.stats["tasks_failed"] += 1

    async def think(self, context: str) -> str:
        """Think/reason about a task."""
        # Placeholder for agent thinking
        return f"{self.name} thinking about: {context[:100]}"

    async def communicate(self, recipient_agent: "BaseAgent", message: str) -> None:
        """Send message to another agent."""
        logger.info(f"{self.name} -> {recipient_agent.name}: {message[:50]}")

    async def request_delegation(
        self,
        task: Dict[str, Any],
        target_agent: Optional[str] = None,
    ) -> Optional[str]:
        """Request task delegation."""
        logger.info(f"{self.name} requesting delegation for task: {task.get('type')}")
        return None
