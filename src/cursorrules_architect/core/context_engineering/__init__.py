"""
Context Engineering Module

Real Context Engineering implementation based on neural field theory.
This module implements the paradigm shift from discrete token management
to continuous semantic fields with attractors, resonance, and field dynamics.

Key Components:
- NeuralFieldManager: Continuous semantic field management
- ProtocolShellEngine: Pareto-lang protocol execution
- Neural field configuration and templates

Based on Context Engineering principles from:
https://github.com/dosco/llm-context-engineering
"""

from .neural_field_manager import NeuralFieldManager, NeuralField, Attractor, SymbolicResidue, FieldState
from .protocol_shell_engine import ProtocolShellEngine, ProtocolParser, ProtocolShell

__all__ = [
    'NeuralFieldManager',
    'NeuralField', 
    'Attractor',
    'SymbolicResidue',
    'FieldState',
    'ProtocolShellEngine',
    'ProtocolParser',
    'ProtocolShell'
]