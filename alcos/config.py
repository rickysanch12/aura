"""Configuration management for ALCOS."""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import logging

logger = logging.getLogger(__name__)


class AlcosSettings(BaseSettings):
    """Main ALCOS settings."""

    # System
    home_dir: Path = Field(default_factory=lambda: Path.home() / ".alcos")
    env: str = Field(default="production")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # API
    api_host: str = Field(default="127.0.0.1")
    api_port: int = Field(default=8000)
    api_workers: int = Field(default=4)

    # Models
    models_dir: Path = Field(default_factory=lambda: Path.home() / ".alcos" / "models")
    default_model: str = Field(default="openclaw")
    model_timeout: int = Field(default=300)
    enable_gpu: bool = Field(default=True)
    cuda_visible_devices: Optional[str] = Field(default=None)
    ollama_base_url: str = Field(default="http://localhost:11434")

    # Memory
    memory_dir: Path = Field(default_factory=lambda: Path.home() / ".alcos" / "memory")
    memory_backend: str = Field(default="chromadb")
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    memory_max_size: int = Field(default=1000000)

    # Agents
    max_agents: int = Field(default=8)
    agent_timeout: int = Field(default=600)
    enable_agent_memory: bool = Field(default=True)

    # Code Execution
    enable_code_execution: bool = Field(default=True)
    sandbox_isolation: str = Field(default="docker")
    execution_timeout: int = Field(default=60)
    max_concurrent_executions: int = Field(default=4)

    # Persistence
    db_url: str = Field(default="sqlite:///{home}/.alcos/alcos.db")
    enable_persistence: bool = Field(default=True)

    # WebSocket
    ws_timeout: int = Field(default=300)
    max_connections: int = Field(default=10)

    # Performance
    cache_size: int = Field(default=512)
    cache_ttl: int = Field(default=3600)
    enable_compression: bool = Field(default=True)

    # Self-improvement
    enable_self_improvement: bool = Field(default=True)
    optimization_interval: int = Field(default=3600)
    enable_self_modification: bool = Field(default=False)

    class Config:
        env_file = ".env"
        case_sensitive = False
        validate_assignment = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Resolve home dir references
        self.db_url = self.db_url.format(home=str(self.home_dir))


class ConfigManager:
    """Manages ALCOS configuration."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".alcos" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings = AlcosSettings()
        self._load_config_files()

    def _load_config_files(self):
        """Load configuration files."""
        config_files = [
            "models.yaml",
            "agents.yaml",
            "memory.yaml",
            "execution.yaml",
            "api.yaml",
        ]
        self.configs = {}
        for config_file in config_files:
            config_path = self.config_dir / config_file
            if config_path.exists():
                with open(config_path, "r") as f:
                    self.configs[config_file.split(".")[0]] = yaml.safe_load(f)
            else:
                logger.debug(f"Config file not found: {config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        parts = key.split(".")
        if len(parts) == 1:
            return getattr(self.settings, key, default)
        section = parts[0]
        if section in self.configs and self.configs[section]:
            result = self.configs[section]
            for part in parts[1:]:
                if isinstance(result, dict):
                    result = result.get(part)
                else:
                    return default
            return result if result is not None else default
        return default

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        parts = key.split(".")
        if len(parts) == 1:
            setattr(self.settings, key, value)
        else:
            section = parts[0]
            if section not in self.configs:
                self.configs[section] = {}
            current = self.configs[section]
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value

    def save(self) -> None:
        """Save configuration to files."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        for section, config in self.configs.items():
            config_path = self.config_dir / f"{section}.yaml"
            with open(config_path, "w") as f:
                yaml.dump(config, f, default_flow_style=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            **self.settings.model_dump(),
            **self.configs,
        }


_config_manager: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get or create the config manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
