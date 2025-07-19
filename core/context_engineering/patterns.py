"""
core/context_engineering/patterns.py

Implementation of molecular context patterns for enhanced prompt chaining.
Maps to 02_molecules_context.md for building connected analysis workflows.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ContextType(Enum):
    """Types of context for molecular pattern building."""
    SEQUENTIAL = "sequential"     # Linear context flow
    HIERARCHICAL = "hierarchical" # Nested context structures
    NETWORKED = "networked"       # Interconnected context webs
    EMERGENT = "emergent"         # Self-organizing context patterns

@dataclass
class ContextMolecule:
    """
    A context molecule representing connected prompt patterns.
    Based on molecular context engineering principles.
    """
    primary_context: str
    supporting_contexts: List[str]
    context_type: ContextType
    binding_pattern: str
    
    def synthesize(self) -> str:
        """Synthesize contexts into a coherent molecular structure."""
        if self.context_type == ContextType.SEQUENTIAL:
            return self._synthesize_sequential()
        elif self.context_type == ContextType.HIERARCHICAL:
            return self._synthesize_hierarchical()
        elif self.context_type == ContextType.NETWORKED:
            return self._synthesize_networked()
        else:  # EMERGENT
            return self._synthesize_emergent()
    
    def _synthesize_sequential(self) -> str:
        """Create sequential context flow."""
        contexts = [self.primary_context] + self.supporting_contexts
        return f"\n{self.binding_pattern}\n".join(contexts)
    
    def _synthesize_hierarchical(self) -> str:
        """Create hierarchical context structure."""
        result = f"PRIMARY CONTEXT:\n{self.primary_context}\n\n"
        if self.supporting_contexts:
            result += "SUPPORTING CONTEXTS:\n"
            for i, context in enumerate(self.supporting_contexts, 1):
                result += f"{i}. {context}\n"
        return result
    
    def _synthesize_networked(self) -> str:
        """Create networked context web."""
        result = f"CORE: {self.primary_context}\n\n"
        result += "CONNECTED CONTEXTS:\n"
        for context in self.supporting_contexts:
            result += f"↔ {context}\n"
        return result
    
    def _synthesize_emergent(self) -> str:
        """Create emergent context pattern."""
        all_contexts = [self.primary_context] + self.supporting_contexts
        return f"EMERGENT PATTERN:\n{' ⟷ '.join(all_contexts)}"

class PromptPatterns:
    """
    Advanced prompt pattern management for molecular context building.
    Implements context engineering patterns for enhanced analysis workflows.
    """
    
    def __init__(self):
        """Initialize prompt patterns with molecular templates."""
        self.pattern_library = {
            "analysis_chain": {
                "description": "Sequential analysis pattern for deep exploration",
                "template": "Analyze {component} → Consider {context} → Synthesize {output}",
                "binding_pattern": "BUILDING ON PREVIOUS ANALYSIS:"
            },
            "synthesis_web": {
                "description": "Networked synthesis for complex pattern recognition",
                "template": "Core insight: {insight} ↔ Connected patterns: {patterns}",
                "binding_pattern": "PATTERN CONNECTIONS:"
            },
            "discovery_hierarchy": {
                "description": "Hierarchical discovery for structured exploration",
                "template": "Primary discovery: {discovery} → Sub-patterns: {sub_patterns}",
                "binding_pattern": "HIERARCHICAL STRUCTURE:"
            }
        }
        
        self.active_molecules = {}
        self.context_history = []
    
    def create_analysis_molecule(
        self,
        phase_name: str,
        primary_analysis: str,
        supporting_analyses: List[str],
        pattern_type: str = "analysis_chain"
    ) -> ContextMolecule:
        """
        Create a context molecule for analysis workflows.
        
        Args:
            phase_name: Name of the analysis phase
            primary_analysis: Main analysis context
            supporting_analyses: Supporting analysis contexts
            pattern_type: Type of pattern to use
            
        Returns:
            ContextMolecule configured for the analysis
        """
        if pattern_type not in self.pattern_library:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        pattern = self.pattern_library[pattern_type]
        
        # Determine context type based on pattern
        context_type_mapping = {
            "analysis_chain": ContextType.SEQUENTIAL,
            "synthesis_web": ContextType.NETWORKED,
            "discovery_hierarchy": ContextType.HIERARCHICAL
        }
        
        context_type = context_type_mapping.get(pattern_type, ContextType.EMERGENT)
        
        molecule = ContextMolecule(
            primary_context=primary_analysis,
            supporting_contexts=supporting_analyses,
            context_type=context_type,
            binding_pattern=pattern["binding_pattern"]
        )
        
        self.active_molecules[phase_name] = molecule
        return molecule
    
    def chain_phases(
        self,
        phase_results: Dict[str, str],
        target_phase: str
    ) -> str:
        """
        Chain results from previous phases into context for target phase.
        
        Args:
            phase_results: Results from completed phases
            target_phase: Phase that will use the chained context
            
        Returns:
            Chained context string optimized for target phase
        """
        # Create hierarchical context from phase results
        chained_context = f"CONTEXT FOR {target_phase.upper()}:\n\n"
        
        # Add previous phase results in order
        phase_order = ["phase_1", "phase_2", "phase_3", "phase_4", "phase_5"]
        relevant_phases = [p for p in phase_order if p in phase_results and p != target_phase]
        
        for phase in relevant_phases:
            chained_context += f"FROM {phase.upper()}:\n{phase_results[phase]}\n\n"
        
        # Add synthesis directive
        chained_context += f"SYNTHESIZE FOR {target_phase.upper()}:\n"
        chained_context += "Build upon the above insights to generate enhanced analysis."
        
        return chained_context
    
    def create_synthesis_molecule(
        self,
        core_insight: str,
        pattern_connections: List[str],
        synthesis_goal: str
    ) -> ContextMolecule:
        """
        Create a synthesis molecule for pattern integration.
        
        Args:
            core_insight: Central insight to build around
            pattern_connections: Related patterns to connect
            synthesis_goal: Goal of the synthesis process
            
        Returns:
            ContextMolecule configured for synthesis
        """
        # Format core insight with synthesis goal
        primary_context = f"CORE INSIGHT: {core_insight}\nSYNTHESIS GOAL: {synthesis_goal}"
        
        # Format pattern connections
        formatted_connections = [f"PATTERN: {conn}" for conn in pattern_connections]
        
        molecule = ContextMolecule(
            primary_context=primary_context,
            supporting_contexts=formatted_connections,
            context_type=ContextType.NETWORKED,
            binding_pattern="CONNECTING PATTERNS:"
        )
        
        return molecule
    
    def optimize_context_flow(
        self,
        context_sequence: List[str],
        optimization_goal: str = "clarity"
    ) -> List[str]:
        """
        Optimize context flow for better information transfer.
        
        Args:
            context_sequence: Sequence of contexts to optimize
            optimization_goal: Goal for optimization ('clarity', 'efficiency', 'depth')
            
        Returns:
            Optimized context sequence
        """
        if optimization_goal == "clarity":
            return self._optimize_for_clarity(context_sequence)
        elif optimization_goal == "efficiency":
            return self._optimize_for_efficiency(context_sequence)
        elif optimization_goal == "depth":
            return self._optimize_for_depth(context_sequence)
        else:
            return context_sequence
    
    def _optimize_for_clarity(self, contexts: List[str]) -> List[str]:
        """Optimize context sequence for clarity."""
        # Sort by length (shorter first for clarity)
        sorted_contexts = sorted(contexts, key=len)
        
        # Add clarity markers
        optimized = []
        for i, context in enumerate(sorted_contexts, 1):
            marker = f"CLARITY POINT {i}:"
            optimized.append(f"{marker}\n{context}")
        
        return optimized
    
    def _optimize_for_efficiency(self, contexts: List[str]) -> List[str]:
        """Optimize context sequence for efficiency."""
        # Combine related contexts to reduce redundancy
        combined_contexts = []
        current_combined = ""
        
        for context in contexts:
            if len(current_combined) + len(context) < 500:  # Efficiency threshold
                current_combined += f"\n{context}" if current_combined else context
            else:
                if current_combined:
                    combined_contexts.append(current_combined)
                current_combined = context
        
        if current_combined:
            combined_contexts.append(current_combined)
        
        return combined_contexts
    
    def _optimize_for_depth(self, contexts: List[str]) -> List[str]:
        """Optimize context sequence for analytical depth."""
        # Sort by complexity (longer, more detailed first)
        sorted_contexts = sorted(contexts, key=lambda x: len(x.split()), reverse=True)
        
        # Add depth markers
        optimized = []
        for i, context in enumerate(sorted_contexts, 1):
            marker = f"DEPTH LAYER {i}:"
            optimized.append(f"{marker}\n{context}")
        
        return optimized
    
    def track_context_evolution(self, phase: str, context: str):
        """Track how context evolves through phases."""
        self.context_history.append({
            "phase": phase,
            "context": context,
            "timestamp": "current",  # Would use actual timestamp in production
            "complexity": len(context.split())
        })
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get summary of context evolution across phases."""
        if not self.context_history:
            return {"status": "No context history available"}
        
        return {
            "total_phases": len(self.context_history),
            "complexity_trend": [entry["complexity"] for entry in self.context_history],
            "evolution_pattern": "increasing" if len(set(entry["complexity"] for entry in self.context_history)) > 1 else "stable"
        }