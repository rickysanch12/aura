"""Ollama API client for local model execution."""

import httpx
import json
import logging
from typing import Any, Dict, AsyncGenerator, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for Ollama local LLM service."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=300.0)
        self.loaded_models = {}

    async def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama service unavailable: {e}")
            return False

    async def list_models(self) -> list[Dict[str, Any]]:
        """List all available models in Ollama."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return data.get("models", [])
            return []
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    async def pull_model(self, model_name: str) -> bool:
        """Download/pull a model from Ollama registry."""
        try:
            logger.info(f"Pulling model: {model_name}")
            response = await self.client.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
            )
            if response.status_code == 200:
                logger.info(f"Successfully pulled model: {model_name}")
                return True
            else:
                logger.error(f"Failed to pull model {model_name}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False

    async def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_predict: int = 256,
        stop: Optional[list[str]] = None,
    ) -> str | AsyncGenerator[str, None]:
        """Generate text using a model."""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "num_predict": num_predict,
                },
            }
            if stop:
                payload["options"]["stop"] = stop

            if stream:
                return self._stream_generate(payload)
            else:
                response = await self.client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                else:
                    logger.error(f"Generation failed: {response.text}")
                    return ""
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return ""

    async def _stream_generate(
        self,
        payload: Dict[str, Any],
    ) -> AsyncGenerator[str, None]:
        """Stream text generation."""
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json=payload,
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        yield data.get("response", "")
        except Exception as e:
            logger.error(f"Error in stream generation: {e}")

    async def chat(
        self,
        model: str,
        messages: list[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str | AsyncGenerator[str, None]:
        """Chat with a model using message history."""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                },
            }

            if stream:
                return self._stream_chat(payload)
            else:
                response = await self.client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("message", {}).get("content", "")
                else:
                    logger.error(f"Chat failed: {response.text}")
                    return ""
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return ""

    async def _stream_chat(
        self,
        payload: Dict[str, Any],
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses."""
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json=payload,
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        if content:
                            yield content
        except Exception as e:
            logger.error(f"Error in stream chat: {e}")

    async def embed(self, model: str, text: str) -> Optional[list[float]]:
        """Generate embeddings for text."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/embed",
                json={"model": model, "input": text},
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("embedding", None)
            else:
                logger.error(f"Embedding failed: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None

    async def show_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a model."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/show",
                json={"name": model_name},
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Could not show model {model_name}: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error showing model info: {e}")
            return None

    async def delete_model(self, model_name: str) -> bool:
        """Delete a model from Ollama."""
        try:
            logger.info(f"Deleting model: {model_name}")
            response = await self.client.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name},
            )
            if response.status_code == 200:
                logger.info(f"Successfully deleted model: {model_name}")
                return True
            else:
                logger.error(f"Failed to delete model {model_name}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error deleting model {model_name}: {e}")
            return False

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def health_check(self) -> Dict[str, Any]:
        """Check Ollama service health."""
        try:
            is_available = await self.is_available()
            models = await self.list_models()
            return {
                "status": "healthy" if is_available else "unhealthy",
                "available": is_available,
                "models_count": len(models),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "error",
                "available": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
