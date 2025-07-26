"""
Analysis configuration module.

This module provides configuration classes for the analysis pipeline,
including model configurations, analysis settings, and configuration loading.
"""

import yaml
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, field

from .agents import ModelConfig, MODEL_CONFIG
from ..core.agents.base import ModelProvider, ReasoningMode


# Alias for backward compatibility with tests
AgentProvider = ModelProvider


@dataclass
class AnalysisConfig:
    """Configuration for the analysis pipeline."""
    
    # File processing limits
    max_file_size: int = 1024 * 1024  # 1MB
    max_files_per_agent: int = 50
    
    # Analysis settings
    enable_context_engineering: bool = False
    parallel_execution: bool = True
    
    # Timeout settings (in seconds)
    phase_timeout: int = 300  # 5 minutes per phase
    total_timeout: int = 1800  # 30 minutes total
    
    # Model configurations for each phase
    phase_models: Dict[str, ModelConfig] = field(default_factory=lambda: MODEL_CONFIG.copy())
    
    def get_phase_model(self, phase: str) -> ModelConfig:
        """Get the model configuration for a specific phase."""
        return self.phase_models.get(phase, self.phase_models.get("phase1"))
    
    def update_phase_model(self, phase: str, model_config: ModelConfig) -> None:
        """Update the model configuration for a specific phase."""
        self.phase_models[phase] = model_config
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "AnalysisConfig":
        """Create AnalysisConfig from dictionary."""
        # Extract known fields
        known_fields = {
            "max_file_size",
            "max_files_per_agent", 
            "enable_context_engineering",
            "parallel_execution",
            "phase_timeout",
            "total_timeout"
        }
        
        kwargs = {k: v for k, v in config_dict.items() if k in known_fields}
        
        # Handle phase_models if present
        if "phase_models" in config_dict:
            kwargs["phase_models"] = config_dict["phase_models"]
        
        return cls(**kwargs)


def load_config(config_path: Optional[Path] = None) -> AnalysisConfig:
    """
    Load analysis configuration from file or return default.
    
    Args:
        config_path: Path to YAML configuration file. If None, returns default config.
        
    Returns:
        AnalysisConfig instance
    """
    if config_path is None or not config_path.exists():
        return AnalysisConfig()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
        
        if config_dict is None:
            return AnalysisConfig()
            
        return AnalysisConfig.from_dict(config_dict)
        
    except Exception:
        # Return default config if loading fails
        return AnalysisConfig()


# Export commonly used items
__all__ = [
    "AnalysisConfig",
    "ModelConfig", 
    "AgentProvider",
    "ModelProvider",
    "ReasoningMode",
    "load_config"
]
