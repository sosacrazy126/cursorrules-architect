"""
core/utils/tools/model_config_helper.py

This module provides utility functions for working with model configurations,
including functions to identify and display model configuration names.
"""

import inspect
from typing import Dict, Any, Union
from config.agents import MODEL_CONFIG

def get_model_config_name(config_entry):
    """
    Find the variable name for a model configuration in agents.py
    
    Args:
        config_entry: A ModelConfig object or dict with model configuration info
        
    Returns:
        str: The configuration name (like "GPT4O_CREATIVE" or "CLAUDE_WITH_REASONING")
    """
    # First check if it's one of the predefined phase configs
    for phase, config in MODEL_CONFIG.items():
        if isinstance(config_entry, dict):
            if (config.provider == config_entry.get("provider") and 
                config.model_name == config_entry.get("model_name") and
                config.reasoning == config_entry.get("reasoning") and
                config.temperature == config_entry.get("temperature")):
                # Instead of returning the phase name, continue looking for the actual config name
                pass
        elif config is config_entry:
            # Direct object identity match (for when passing MODEL_CONFIG['phase1'] directly)
            # Import here to avoid circular import
            import config.agents as agents_module
            for name, value in inspect.getmembers(agents_module):
                if name.isupper() and value is config:
                    return name
    
    # Check all variables in the agents module
    import config.agents as agents_module
    for name, value in inspect.getmembers(agents_module):
        if name.isupper() and isinstance(value, agents_module.ModelConfig):
            if isinstance(config_entry, dict):
                if (value.provider == config_entry.get("provider") and 
                    value.model_name == config_entry.get("model_name") and
                    value.reasoning == config_entry.get("reasoning") and
                    value.temperature == config_entry.get("temperature")):
                    return name
            elif (value.provider == getattr(config_entry, "provider", None) and 
                  value.model_name == getattr(config_entry, "model_name", None) and
                  value.reasoning == getattr(config_entry, "reasoning", None) and
                  value.temperature == getattr(config_entry, "temperature", None)):
                return name
                
    # Return the model name if no match is found
    if isinstance(config_entry, dict):
        provider = config_entry.get("provider", "unknown")
        model_name = config_entry.get("model_name", "unknown")
        provider_name = provider.name if hasattr(provider, "name") else provider
        return f"{provider_name}_{model_name}"
    else:
        provider_name = config_entry.provider.name if hasattr(config_entry, "provider") else "unknown"
        model_name = getattr(config_entry, "model_name", "unknown")
        return f"{provider_name}_{model_name}" 