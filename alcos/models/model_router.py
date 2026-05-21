"""Intelligent model routing."""

from typing import Any, Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class ModelRouter:
    """Routes tasks to optimal models."""

    # Task type to model mappings
    TASK_MODEL_MAPPING = {
        "reasoning": ["openclaw", "hermes"],
        "coding": ["hermes", "blackbox", "openclaw"],
        "code_generation": ["blackbox", "hermes"],
        "code_review": ["hermes", "openclaw"],
        "debugging": ["hermes", "openclaw"],
        "research": ["openclaw", "hermes"],
        "planning": ["openclaw", "hermes"],
        "summarization": ["openclaw", "hermes"],
        "extraction": ["hermes", "openclaw"],
        "writing": ["openclaw", "hermes"],
        "chat": ["openclaw", "hermes", "neural-chat"],
        "general": ["openclaw", "hermes", "stablelm"],
    }

    def __init__(self, model_manager):
        self.model_manager = model_manager

    async def route_task(
        self,
        task: str,
        task_type: str = "general",
        required_capabilities: Optional[List[str]] = None,
        prefer_model: Optional[str] = None,
    ) -> Optional[str]:
        """Route a task to the best model."""

        # If specific model is preferred and available
        if prefer_model:
            can_use = await self.model_manager.can_load_model(prefer_model)
            if can_use:
                logger.info(f"Using preferred model: {prefer_model}")
                return prefer_model

        # Get candidate models
        candidates = self.TASK_MODEL_MAPPING.get(task_type, ["openclaw", "hermes"])

        # Filter by required capabilities
        if required_capabilities:
            candidates = await self._filter_by_capabilities(candidates, required_capabilities)

        # Find best available model
        for model_id in candidates:
            can_use = await self.model_manager.can_load_model(model_id)
            if can_use:
                logger.info(f"Routing {task_type} to {model_id}")
                return model_id

        logger.warning(f"No suitable model found for task: {task_type}")
        return None

    async def _filter_by_capabilities(
        self,
        models: List[str],
        required_capabilities: List[str],
    ) -> List[str]:
        """Filter models by required capabilities."""
        filtered = []
        for model_id in models:
            info = await self.model_manager.get_model_info(model_id)
            if info:
                has_capabilities = all(
                    self._has_capability(info, cap) for cap in required_capabilities
                )
                if has_capabilities:
                    filtered.append(model_id)
        return filtered or models

    def _has_capability(self, model_info: Dict[str, Any], capability: str) -> bool:
        """Check if model has a capability."""
        capability_map = {
            "tools": model_info.get("supports_tools", False),
            "vision": model_info.get("supports_vision", False),
            "long_context": model_info.get("size") in ["13b", "70b"],
            "coding": model_info.get("type") in ["coding", "code-generation"],
            "reasoning": model_info.get("type") in ["reasoning", "general"],
        }
        return capability_map.get(capability, False)

    async def get_routing_info(self) -> Dict[str, Any]:
        """Get routing information."""
        models = await self.model_manager.get_available_models()
        return {
            "task_mappings": self.TASK_MODEL_MAPPING,
            "available_models": models,
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        }

    async def optimize_routing(self, stats: Dict[str, Any]) -> None:
        """Optimize routing based on performance statistics."""
        # This would implement learning-based routing optimization
        logger.info("Analyzing routing performance for optimization")
        # Placeholder for optimization logic
        pass
