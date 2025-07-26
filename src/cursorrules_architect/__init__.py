"""
CursorRules Architect - AI-powered project analysis and configuration generator.

A sophisticated tool that analyzes codebases and generates optimized configurations
for AI development tools like Cursor, Claude, and other AI assistants.

Key Features:
- Multi-phase project analysis using various AI models
- Context engineering for enhanced AI interactions  
- Automated generation of .cursorrules and .cursorignore files
- Support for multiple AI providers (Anthropic, OpenAI, Google, DeepSeek)
- Interactive CLI with rich terminal UI
- Comprehensive testing and validation

Main Components:
- core: Analysis engine with 6-phase pipeline
- cli: Command-line interface and interactive components
- config: Configuration management and AI model settings
"""

__version__ = "2.0.0"
__author__ = "CursorRules Architect Team"
__email__ = "team@cursorrules-architect.dev"

# Import main components for easy access
from .core.analysis import (
    Phase1Analysis,
    Phase2Analysis, 
    Phase3Analysis,
    Phase4Analysis,
    Phase5Analysis,
    FinalAnalysis
)

from .config.agents import MODEL_CONFIG, ModelProvider, get_architect_for_phase

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "Phase1Analysis",
    "Phase2Analysis",
    "Phase3Analysis", 
    "Phase4Analysis",
    "Phase5Analysis",
    "FinalAnalysis",
    "MODEL_CONFIG",
    "ModelProvider",
    "get_architect_for_phase"
]
