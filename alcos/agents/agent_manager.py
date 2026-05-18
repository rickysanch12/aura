"""Agent lifecycle management."""

from typing import Any, Dict, List, Optional
import logging
import asyncio

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages agent lifecycle and communication."""

    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.agent_by_type: Dict[str, List[str]] = {}
        self.running = False

    async def register_agent(self, agent) -> str:
        """Register an agent."""
        agent_id = agent.agent_id
        self.agents[agent_id] = agent

        if agent.agent_type not in self.agent_by_type:
            self.agent_by_type[agent.agent_type] = []
        self.agent_by_type[agent.agent_type].append(agent_id)

        logger.info(f"Registered agent: {agent.name} ({agent_id})")
        return agent_id

    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id not in self.agents:
            return False

        agent = self.agents[agent_id]
        agent_type = agent.agent_type

        if agent_type in self.agent_by_type:
            self.agent_by_type[agent_type].remove(agent_id)

        del self.agents[agent_id]
        logger.info(f"Unregistered agent: {agent_id}")
        return True

    async def get_agent(self, agent_id: str) -> Optional[Any]:
        """Get an agent by ID."""
        return self.agents.get(agent_id)

    async def get_agents_by_type(self, agent_type: str) -> List[Any]:
        """Get all agents of a specific type."""
        agent_ids = self.agent_by_type.get(agent_type, [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]

    async def get_all_agents(self) -> List[Any]:
        """Get all registered agents."""
        return list(self.agents.values())

    async def start_agent(self, agent_id: str) -> bool:
        """Start an agent."""
        agent = await self.get_agent(agent_id)
        if not agent:
            return False

        await agent.start()
        return True

    async def stop_agent(self, agent_id: str) -> bool:
        """Stop an agent."""
        agent = await self.get_agent(agent_id)
        if not agent:
            return False

        await agent.stop()
        return True

    async def start_all(self) -> None:
        """Start all agents."""
        self.running = True
        for agent in await self.get_all_agents():
            await agent.start()
        logger.info("Started all agents")

    async def stop_all(self) -> None:
        """Stop all agents."""
        self.running = False
        for agent in await self.get_all_agents():
            await agent.stop()
        logger.info("Stopped all agents")

    async def delegate_task(
        self,
        task: Dict[str, Any],
        agent_id: Optional[str] = None,
    ) -> Optional[str]:
        """Delegate a task to an agent."""
        if not agent_id:
            # Find suitable agent
            agent_type = task.get("preferred_agent_type")
            if agent_type:
                agents = await self.get_agents_by_type(agent_type)
                if agents:
                    agent = agents[0]  # Simple selection
                    agent_id = agent.agent_id

        if agent_id:
            agent = await self.get_agent(agent_id)
            if agent:
                return await agent.queue_task(task)

        logger.warning(f"Could not delegate task: {task.get('type')}")
        return None

    async def get_status_report(self) -> Dict[str, Any]:
        """Get status report for all agents."""
        agents_status = []
        for agent in await self.get_all_agents():
            agents_status.append(await agent.get_status())

        return {
            "total_agents": len(self.agents),
            "active_agents": sum(1 for a in agents_status if a["is_active"]),
            "agents": agents_status,
            "running": self.running,
        }

    async def broadcast_message(self, message: str) -> None:
        """Broadcast message to all agents."""
        for agent in await self.get_all_agents():
            logger.info(f"Broadcasting to {agent.name}: {message[:50]}")

    async def request_agent_help(
        self,
        source_agent_id: str,
        help_type: str,
    ) -> Optional[str]:
        """Request help from another agent."""
        source_agent = await self.get_agent(source_agent_id)
        if not source_agent:
            return None

        agents = await self.get_all_agents()
        for agent in agents:
            if agent.agent_id != source_agent_id:
                logger.info(f"{source_agent.name} requesting help from {agent.name}")
                return agent.agent_id

        return None
