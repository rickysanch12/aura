"""Agentic Local Core OS - Elite local autonomous AI system."""

__version__ = "1.0.0"
__author__ = "Autonomous Systems Team"

from .core import AgenticCoreOS
from .config import get_config
from .logger import setup_logging

__all__ = [
    "AgenticCoreOS",
    "get_config",
    "setup_logging",
]
