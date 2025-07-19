"""
core/context_engineering/__init__.py

Context Engineering Integration Module for CursorRules Architect

This module provides the foundation for integrating context engineering patterns
into the existing analysis phases, enhancing prompt optimization and field dynamics.
"""

from .foundations import ContextFoundations
from .patterns import PromptPatterns
from .field_dynamics import FieldDynamics
from .cognitive_tools import CognitiveToolkit

__all__ = [
    'ContextFoundations',
    'PromptPatterns', 
    'FieldDynamics',
    'CognitiveToolkit'
]