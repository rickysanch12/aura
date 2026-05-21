"""Logging configuration for ALCOS."""

import logging
import sys
from pathlib import Path
from typing import Optional
from loguru import logger as loguru_logger

_loggers = {}


def setup_logging(
    name: str = "alcos",
    level: str = "INFO",
    log_dir: Optional[Path] = None,
) -> logging.Logger:
    """Setup logging for ALCOS."""

    if log_dir is None:
        log_dir = Path.home() / ".alcos" / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)

    # Remove default handler
    loguru_logger.remove()

    # Add console handler
    loguru_logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )

    # Add file handler
    log_file = log_dir / f"{name}.log"
    loguru_logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level=level,
        rotation="10 MB",
        retention="10 days",
    )

    # Get Python logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handler that forwards to loguru
    class LoguruHandler(logging.Handler):
        def emit(self, record):
            level_name = record.levelname
            loguru_logger.opt(depth=1).log(level_name, record.getMessage())

    handler = LoguruHandler()
    logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
    return _loggers[name]


# Setup root logger
setup_logging()
root_logger = logging.getLogger("alcos")
