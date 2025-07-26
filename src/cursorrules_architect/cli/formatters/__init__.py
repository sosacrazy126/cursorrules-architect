"""
Configuration formatters for different AI coding tools.

Provides a unified interface for generating tool-specific configurations
from analysis results.
"""

from .base import BaseFormatter
from .cursor import CursorFormatter
from .windsurf import WindsurfFormatter
from .cline import ClineFormatter
from .roo import RooFormatter
from .claude import ClaudeFormatter

# Formatter registry
FORMATTERS = {
    "cursor": CursorFormatter,
    "windsurf": WindsurfFormatter,
    "cline": ClineFormatter,
    "roo": RooFormatter,
    "claude": ClaudeFormatter,
}


def get_formatter(tool: str) -> BaseFormatter:
    """Get the appropriate formatter for a tool."""
    if tool not in FORMATTERS:
        raise ValueError(f"No formatter available for tool: {tool}")
    
    formatter_class = FORMATTERS[tool]
    return formatter_class()


def list_supported_tools() -> list[str]:
    """List all tools with available formatters."""
    return list(FORMATTERS.keys())


__all__ = [
    "BaseFormatter",
    "get_formatter", 
    "list_supported_tools",
    "CursorFormatter",
    "WindsurfFormatter", 
    "ClineFormatter",
    "RooFormatter",
    "ClaudeFormatter",
]