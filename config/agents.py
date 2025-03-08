"""
config/agents.py

This module provides configurations for AI models used in different phases of analysis.
It allows users to easily configure which models to use for each phase by updating
the `MODEL_CONFIG` dictionary.

Users can specify a different model for each phase and whether to use reasoning.
"""

from core.agents.base import ModelProvider, ReasoningMode
from typing import Dict, Any, NamedTuple, Optional

# ====================================================
# Model Configuration Types
# This section defines types for model configuration.
# ====================================================

class ModelConfig(NamedTuple):
    """Configuration for a specific AI model."""
    provider: ModelProvider
    model_name: str
    reasoning: ReasoningMode = ReasoningMode.DISABLED
    temperature: Optional[float] = None  # For temperature-based models like GPT-4o

# ====================================================
# Predefined Model Configurations
# These are shorthand configurations that can be referenced in the MODEL_CONFIG.
# ====================================================

CLAUDE_BASIC = ModelConfig(
    provider=ModelProvider.ANTHROPIC,
    model_name="claude-3-7-sonnet-20250219",
    reasoning=ReasoningMode.DISABLED
)

CLAUDE_WITH_REASONING = ModelConfig(
    provider=ModelProvider.ANTHROPIC,
    model_name="claude-3-7-sonnet-20250219",
    reasoning=ReasoningMode.ENABLED
)

# O1 configurations with different reasoning levels
O1_HIGH = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o1",
    reasoning=ReasoningMode.HIGH
)

O1_MEDIUM = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o1",
    reasoning=ReasoningMode.MEDIUM
)

O1_LOW = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o1",
    reasoning=ReasoningMode.LOW
)

# O3-mini configurations with different reasoning levels
O3_MINI_HIGH = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o3-mini",
    reasoning=ReasoningMode.HIGH
)

O3_MINI_MEDIUM = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o3-mini",
    reasoning=ReasoningMode.MEDIUM
)

O3_MINI_LOW = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o3-mini",
    reasoning=ReasoningMode.LOW
)

# GPT-4o configurations with different temperature values
GPT4O_DEFAULT = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="gpt-4o",
    reasoning=ReasoningMode.TEMPERATURE,
    temperature=0.7  # Default temperature
)

GPT4O_CREATIVE = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="gpt-4o",
    reasoning=ReasoningMode.TEMPERATURE,
    temperature=0.9  # Higher temperature for more creative outputs
)

GPT4O_PRECISE = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="gpt-4o",
    reasoning=ReasoningMode.TEMPERATURE,
    temperature=0.2  # Lower temperature for more precise/deterministic outputs
)

# DeepSeek configurations
DEEPSEEK_REASONER = ModelConfig(
    provider=ModelProvider.DEEPSEEK,
    model_name="deepseek-reasoner",
    reasoning=ReasoningMode.ENABLED  # Always enabled for reasoner
)

# ====================================================
# Phase Model Configuration
# Define which model to use for each phase.
# ====================================================

# Default model configuration
MODEL_CONFIG = {
    # Phase 1: Initial Discovery
    "phase1": CLAUDE_BASIC,
    
    # Phase 2: Methodical Planning
    "phase2": O1_HIGH,
    
    # Phase 3: Deep Analysis
    "phase3": CLAUDE_BASIC,
    
    # Phase 4: Synthesis
    "phase4": CLAUDE_WITH_REASONING,
    
    # Phase 5: Consolidation
    "phase5": DEEPSEEK_REASONER,
    
    # Final Analysis
    "final": CLAUDE_WITH_REASONING,
}

# ====================================================
# Model Factory Function
# This function creates the appropriate architect instance based on configuration.
# ====================================================

def get_architect_for_phase(phase: str, **kwargs) -> Any:
    """
    Get the appropriate architect instance for a phase based on configuration.
    
    Args:
        phase: The phase to get an architect for (e.g., "phase1", "phase2")
        **kwargs: Additional keyword arguments to pass to the architect constructor
        
    Returns:
        An instance of the appropriate architect class for the specified phase
    """
    from core.agents.anthropic import AnthropicArchitect
    from core.agents.openai import OpenAIArchitect
    from core.agents.deepseek import DeepSeekArchitect
    
    # Get model configuration for the phase
    config = MODEL_CONFIG.get(phase)
    if not config:
        raise ValueError(f"No model configuration found for phase '{phase}'")
    
    # Create the appropriate architect instance
    if config.provider == ModelProvider.ANTHROPIC:
        return AnthropicArchitect(
            model_name=config.model_name,
            reasoning=config.reasoning,
            **kwargs
        )
    elif config.provider == ModelProvider.OPENAI:
        return OpenAIArchitect(
            model_name=config.model_name,
            reasoning=config.reasoning,
            temperature=config.temperature,
            **kwargs
        )
    elif config.provider == ModelProvider.DEEPSEEK:
        # DeepSeek Reasoner has fixed parameters
        return DeepSeekArchitect(
            **kwargs  # Only pass the kwargs, other params are fixed in DeepSeekArchitect
        )
    else:
        raise ValueError(f"Unknown model provider: {config.provider}")
