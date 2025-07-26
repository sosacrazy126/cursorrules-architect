"""
config package

This package contains configuration settings for the project analyzer.
"""

from .analysis_config import (
    AnalysisConfig,
    ModelConfig,
    AgentProvider,
    ModelProvider,
    ReasoningMode,
    load_config
)

from .agents import MODEL_CONFIG, get_architect_for_phase

__all__ = [
    "AnalysisConfig",
    "ModelConfig",
    "AgentProvider",
    "ModelProvider",
    "ReasoningMode",
    "load_config",
    "MODEL_CONFIG",
    "get_architect_for_phase"
]