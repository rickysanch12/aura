"""Model loading and initialization."""

from typing import Optional, Dict, Any
import logging
from pathlib import Path
from .ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class ModelLoader:
    """Loads models from various sources."""

    def __init__(
        self,
        models_dir: Optional[Path] = None,
        ollama_base_url: str = "http://localhost:11434",
    ):
        self.models_dir = models_dir or Path.home() / ".alcos" / "models"
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.ollama_client = OllamaClient(base_url=ollama_base_url)
        self.loaded_models = {}

    async def load_from_ollama(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Load model from Ollama."""
        try:
            is_available = await self.ollama_client.is_available()
            if not is_available:
                logger.error("Ollama service is not available")
                return None

            logger.info(f"Loading {model_id} from Ollama")
            model_info = await self.ollama_client.show_model(model_id)

            if model_info:
                self.loaded_models[model_id] = {
                    "model": model_id,
                    "source": "ollama",
                    "info": model_info,
                }
                logger.info(f"Successfully loaded {model_id} from Ollama")
                return self.loaded_models[model_id]
            else:
                logger.warning(f"Model {model_id} not found in Ollama")
                return None
        except Exception as e:
            logger.error(f"Failed to load {model_id} from Ollama: {e}")
            return None

    async def load_from_llama_cpp(
        self,
        model_path: Path,
        n_gpu_layers: int = -1,
    ) -> Optional[Any]:
        """Load model using llama.cpp."""
        try:
            from llama_cpp import Llama
            logger.info(f"Loading {model_path} with llama.cpp")
            model = Llama(
                model_path=str(model_path),
                n_gpu_layers=n_gpu_layers,
                verbose=False,
            )
            return model
        except ImportError:
            logger.error("llama-cpp-python not installed")
            return None

    async def load_from_vllm(
        self,
        model_name: str,
        gpu_memory_utilization: float = 0.8,
    ) -> Optional[Any]:
        """Load model using vLLM."""
        try:
            from vllm import LLM
            logger.info(f"Loading {model_name} with vLLM")
            model = LLM(
                model=model_name,
                gpu_memory_utilization=gpu_memory_utilization,
            )
            return model
        except ImportError:
            logger.error("vLLM not installed")
            return None

    async def download_model(
        self,
        model_id: str,
        source: str = "ollama",
    ) -> bool:
        """Download a model."""
        try:
            if source == "ollama":
                is_available = await self.ollama_client.is_available()
                if not is_available:
                    logger.error("Ollama service is not available")
                    return False

                logger.info(f"Downloading {model_id} from Ollama registry")
                success = await self.ollama_client.pull_model(model_id)
                if success:
                    logger.info(f"Successfully downloaded {model_id}")
                    return True
                else:
                    logger.error(f"Failed to download {model_id}")
                    return False
            else:
                logger.error(f"Unknown model source: {source}")
                return False
        except Exception as e:
            logger.error(f"Failed to download {model_id}: {e}")
            return False

    async def get_model_path(self, model_id: str) -> Optional[Path]:
        """Get local path for a model."""
        model_path = self.models_dir / model_id
        if model_path.exists():
            return model_path
        return None

    async def verify_model(self, model_id: str) -> bool:
        """Verify that a model is properly loaded."""
        # Placeholder for model verification
        logger.info(f"Verifying model: {model_id}")
        return True
