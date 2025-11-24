"""
Logging configuration for Radic backend.
Uses Loguru for structured logging with file rotation.
"""

import sys
from pathlib import Path
from loguru import logger

# Remove default handler
logger.remove()

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Add console handler with colored output
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True,
)

# Add file handler for all logs
logger.add(
    "logs/radic.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)

# Add file handler for errors only
logger.add(
    "logs/error.log",
    rotation="10 MB",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
)


def get_logger(name: str):
    """
    Get a logger instance bound to a specific module name.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Logger instance
        
    Example:
        logger = get_logger(__name__)
        logger.info("Processing request")
    """
    return logger.bind(name=name)


# Export the main logger
__all__ = ["logger", "get_logger"]

