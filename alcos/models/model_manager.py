"""Model management and lifecycle."""

from typing import Any, Dict, List, Optional
from pathlib import Path
import logging
import psutil
import json
from datetime import datetime
from .model_loader import ModelLoader
from .ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages model lifecycle and resources."""

    # Model registry
    KNOWN_MODELS = {
        "openclaw": {
            "name": "OpenClaw",
            "type": "reasoning",
            "size": "7b",
            "vram": 16,
            "supports_tools": True,
            "supports_vision": False,
            "default_params": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048,
            },
        },
        "hermes": {
            "name": "Hermes 2 Pro",
            "type": "coding",
            "size": "7b",
            "vram": 16,
            "supports_tools": True,
            "supports_vision": False,
            "default_params": {
                "temperature": 0.1,
                "top_p": 0.9,
                "max_tokens": 4096,
            },
        },
        "blackbox": {
            "name": "Blackbox",
            "type": "code-generation",
            "size": "7b",
            "vram": 16,
            "supports_tools": False,
            "supports_vision": False,
            "default_params": {
                "temperature": 0.2,
                "top_p": 0.95,
                "max_tokens": 8192,
            },
        },
        "neural-chat": {
            "name": "Neural Chat",
            "type": "chat",
            "size": "7b",
            "vram": 8,
            "supports_tools": False,
            "supports_vision": False,
            "default_params": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048,
            },
        },
        "stablelm": {
            "name": "StableLM Zephyr",
            "type": "general",
            "size": "3b",
            "vram": 8,
            "supports_tools": False,
            "supports_vision": False,
            "default_params": {
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 2048,
            },
        },
    }

    def __init__(
        self,
        models_dir: Optional[Path] = None,
        ollama_base_url: str = "http://localhost:11434",
    ):
        self.models_dir = models_dir or Path.home() / ".alcos" / "models"
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_models = {}
        self.model_stats = {}
        self.model_loader = ModelLoader(
            models_dir=self.models_dir,
            ollama_base_url=ollama_base_url,
        )
        self.ollama_client = OllamaClient(base_url=ollama_base_url)

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get all available models."""
        models = []
        for model_id, config in self.KNOWN_MODELS.items():
            model_path = self.models_dir / model_id
            is_loaded = model_id in self.loaded_models
            is_downloaded = model_path.exists()

            models.append({
                "id": model_id,
                "name": config["name"],
                "type": config["type"],
                "size": config["size"],
                "vram": config["vram"],
                "is_loaded": is_loaded,
                "is_downloaded": is_downloaded,
                "supports_tools": config["supports_tools"],
                "supports_vision": config["supports_vision"],
                "stats": self.model_stats.get(model_id, {}),
            })
        return models

    async def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        if model_id not in self.KNOWN_MODELS:
            return None

        config = self.KNOWN_MODELS[model_id]
        model_path = self.models_dir / model_id
        is_loaded = model_id in self.loaded_models

        return {
            "id": model_id,
            "name": config["name"],
            "type": config["type"],
            "size": config["size"],
            "vram": config["vram"],
            "is_loaded": is_loaded,
            "is_downloaded": model_path.exists(),
            "supports_tools": config["supports_tools"],
            "supports_vision": config["supports_vision"],
            "default_params": config["default_params"],
            "stats": self.model_stats.get(model_id, {}),
        }

    async def get_available_vram(self) -> int:
        """Get available GPU VRAM."""
        try:
            import torch
            if torch.cuda.is_available():
                return int(torch.cuda.get_device_properties(0).total_memory / 1024**3)
        except:
            pass
        return 0

    async def get_system_memory(self) -> Dict[str, Any]:
        """Get system memory information."""
        vm = psutil.virtual_memory()
        return {
            "total": vm.total // (1024**3),
            "available": vm.available // (1024**3),
            "percent": vm.percent,
        }

    async def can_load_model(self, model_id: str) -> bool:
        """Check if model can be loaded given current resources."""
        if model_id not in self.KNOWN_MODELS:
            return False

        config = self.KNOWN_MODELS[model_id]
        available_vram = await self.get_available_vram()

        # Add some headroom
        required_vram = config["vram"] + 2
        return available_vram >= required_vram

    async def load_model(self, model_id: str) -> bool:
        """Load a model through Ollama."""
        if model_id in self.loaded_models:
            logger.info(f"Model {model_id} already loaded")
            return True

        try:
            logger.info(f"Loading model: {model_id}")
            start_time = datetime.now()

            model_info = await self.model_loader.load_from_ollama(model_id)
            if not model_info:
                logger.error(f"Failed to load {model_id}: model not found in Ollama")
                return False

            load_time = (datetime.now() - start_time).total_seconds()

            self.loaded_models[model_id] = {
                "loaded_at": datetime.now().isoformat(),
                "status": "loaded",
                "source": "ollama",
                "model_info": model_info.get("info"),
            }
            self.model_stats[model_id] = {
                "load_time": load_time,
                "total_inference": 0,
                "total_tokens": 0,
                "last_used": datetime.now().isoformat(),
            }
            logger.info(f"Loaded model: {model_id} (took {load_time:.2f}s)")
            return True
        except Exception as e:
            logger.error(f"Failed to load {model_id}: {e}")
            return False

    async def unload_model(self, model_id: str) -> bool:
        """Unload a model."""
        if model_id not in self.loaded_models:
            return True

        try:
            logger.info(f"Unloading model: {model_id}")
            del self.loaded_models[model_id]
            logger.info(f"Unloaded model: {model_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to unload {model_id}: {e}")
            return False

    async def get_model_status(self, model_id: str) -> Dict[str, Any]:
        """Get model status."""
        info = await self.get_model_info(model_id)
        if not info:
            return {}

        return {
            **info,
            "system_memory": await self.get_system_memory(),
            "available_vram": await self.get_available_vram(),
        }

    async def generate(
        self,
        model_id: str,
        prompt: str,
        **kwargs,
    ) -> str:
        """Generate text using a loaded model."""
        if model_id not in self.loaded_models:
            logger.error(f"Model {model_id} is not loaded")
            return ""

        try:
            config = self.KNOWN_MODELS.get(model_id, {})
            default_params = config.get("default_params", {})

            temperature = kwargs.get("temperature", default_params.get("temperature", 0.7))
            top_p = kwargs.get("top_p", default_params.get("top_p", 0.9))
            max_tokens = kwargs.get("max_tokens", default_params.get("max_tokens", 2048))

            logger.debug(f"Generating with {model_id}: temp={temperature}, top_p={top_p}")

            response = await self.ollama_client.generate(
                model=model_id,
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                num_predict=max_tokens,
            )

            if response:
                self.model_stats[model_id]["total_inference"] += 1
                self.model_stats[model_id]["last_used"] = datetime.now().isoformat()

            return response
        except Exception as e:
            logger.error(f"Generation failed for {model_id}: {e}")
            return ""

    async def chat(
        self,
        model_id: str,
        messages: list,
        **kwargs,
    ) -> str:
        """Chat with a loaded model."""
        if model_id not in self.loaded_models:
            logger.error(f"Model {model_id} is not loaded")
            return ""

        try:
            config = self.KNOWN_MODELS.get(model_id, {})
            default_params = config.get("default_params", {})

            temperature = kwargs.get("temperature", default_params.get("temperature", 0.7))
            top_p = kwargs.get("top_p", default_params.get("top_p", 0.9))

            response = await self.ollama_client.chat(
                model=model_id,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
            )

            if response:
                self.model_stats[model_id]["total_inference"] += 1
                self.model_stats[model_id]["last_used"] = datetime.now().isoformat()

            return response
        except Exception as e:
            logger.error(f"Chat failed for {model_id}: {e}")
            return ""

    async def download_and_load_model(self, model_id: str) -> bool:
        """Download a model and load it."""
        try:
            logger.info(f"Downloading model: {model_id}")
            success = await self.model_loader.download_model(model_id, source="ollama")
            if not success:
                logger.error(f"Failed to download {model_id}")
                return False

            logger.info(f"Loading downloaded model: {model_id}")
            return await self.load_model(model_id)
        except Exception as e:
            logger.error(f"Failed to download and load {model_id}: {e}")
            return False

    async def get_ollama_health(self) -> Dict[str, Any]:
        """Get Ollama service health status."""
        return await self.ollama_client.health_check()
