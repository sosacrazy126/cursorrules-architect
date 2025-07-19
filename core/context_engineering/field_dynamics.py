"""
core/context_engineering/field_dynamics.py

Implementation of neural field dynamics for enhanced pattern recognition and synthesis.
Maps to the neural field orchestration concepts for system-level intelligence emergence.
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger(__name__)

class FieldType(Enum):
    """Types of neural fields for different analysis purposes."""
    DISCOVERY = "discovery"       # Initial pattern discovery
    REASONING = "reasoning"       # Logical reasoning and inference
    SYNTHESIS = "synthesis"       # Pattern integration and synthesis
    MEMORY = "memory"            # Persistent context storage
    ORCHESTRATION = "orchestration"  # System-level coordination

@dataclass
class AttractorState:
    """Represents an attractor in the neural field."""
    pattern_id: str
    strength: float
    basin_width: float
    activation_level: float
    decay_rate: float
    resonance_frequency: float
    connected_patterns: List[str] = field(default_factory=list)
    
    def update_activation(self, input_strength: float, time_delta: float = 1.0) -> float:
        """Update attractor activation based on input and decay."""
        # Apply input reinforcement
        reinforcement = input_strength * self.strength
        
        # Apply temporal decay
        decay = self.activation_level * self.decay_rate * time_delta
        
        # Update activation level
        self.activation_level = max(0.0, min(1.0, 
            self.activation_level + reinforcement - decay
        ))
        
        return self.activation_level

@dataclass
class FieldState:
    """Represents the current state of a neural field."""
    field_id: str
    field_type: FieldType
    activation_level: float
    capacity: int
    current_load: int
    attractors: Dict[str, AttractorState] = field(default_factory=dict)
    resonance_patterns: Dict[str, float] = field(default_factory=dict)
    boundary_permeability: float = 0.8
    decay_rate: float = 0.05
    stability_measure: float = 0.0
    
    def add_attractor(self, attractor: AttractorState):
        """Add an attractor to the field."""
        self.attractors[attractor.pattern_id] = attractor
    
    def update_field_state(self, time_delta: float = 1.0):
        """Update the entire field state over time."""
        # Update all attractors
        total_activation = 0.0
        for attractor in self.attractors.values():
            attractor.update_activation(0.0, time_delta)  # Natural decay
            total_activation += attractor.activation_level
        
        # Update field activation level
        self.activation_level = total_activation / len(self.attractors) if self.attractors else 0.0
        
        # Calculate stability
        self.stability_measure = self._calculate_stability()
    
    def _calculate_stability(self) -> float:
        """Calculate field stability based on attractor dynamics."""
        if not self.attractors:
            return 0.0
        
        activation_variance = np.var([a.activation_level for a in self.attractors.values()])
        stability = 1.0 / (1.0 + activation_variance)
        return stability

class FieldDynamics:
    """
    Core field dynamics engine implementing neural field theory for code analysis.
    Provides pattern emergence, attractor dynamics, and multi-field orchestration.
    """
    
    def __init__(self, field_config: Optional[Dict[str, Any]] = None):
        """Initialize field dynamics with configuration."""
        self.field_config = field_config or self._default_field_config()
        self.active_fields = {}
        self.field_interactions = {}
        self.global_state = {
            "system_coherence": 0.0,
            "emergent_patterns": [],
            "resonance_network": {}
        }
        self.time_step = 0
    
    def _default_field_config(self) -> Dict[str, Any]:
        """Provide default field configuration."""
        return {
            "discovery_field": {
                "capacity": 8000,
                "decay_rate": 0.05,
                "boundary_permeability": 0.8,
                "resonance_bandwidth": 0.6,
                "attractor_threshold": 0.7
            },
            "reasoning_field": {
                "capacity": 6000,
                "decay_rate": 0.08,
                "boundary_permeability": 0.7,
                "resonance_bandwidth": 0.8,
                "attractor_threshold": 0.6
            },
            "synthesis_field": {
                "capacity": 10000,
                "decay_rate": 0.02,
                "boundary_permeability": 0.9,
                "resonance_bandwidth": 0.9,
                "attractor_threshold": 0.8
            }
        }
    
    def initialize_field(
        self, 
        field_id: str, 
        field_type: FieldType, 
        context: Dict[str, Any]
    ) -> FieldState:
        """
        Initialize a neural field with given context and configuration.
        
        Args:
            field_id: Unique identifier for the field
            field_type: Type of neural field to create
            context: Initial context data for field initialization
            
        Returns:
            FieldState object representing the initialized field
        """
        config = self.field_config.get(field_id, self.field_config.get("default", {}))
        
        field_state = FieldState(
            field_id=field_id,
            field_type=field_type,
            activation_level=0.0,
            capacity=config.get("capacity", 8000),
            current_load=self._calculate_context_load(context),
            boundary_permeability=config.get("boundary_permeability", 0.8),
            decay_rate=config.get("decay_rate", 0.05)
        )
        
        # Initialize attractors based on context
        initial_attractors = self._identify_initial_attractors(context, config)
        for attractor in initial_attractors:
            field_state.add_attractor(attractor)
        
        self.active_fields[field_id] = field_state
        logger.info(f"Initialized {field_type.value} field '{field_id}' with {len(initial_attractors)} attractors")
        
        return field_state
    
    def process_through_field(
        self, 
        field_id: str, 
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process input data through a specific neural field.
        
        Args:
            field_id: ID of the field to process through
            input_data: Data to process through the field
            
        Returns:
            Processing results including field state, attractors, and resonance
        """
        if field_id not in self.active_fields:
            raise ValueError(f"Field '{field_id}' not initialized")
        
        field_state = self.active_fields[field_id]
        
        # Extract patterns from input data
        input_patterns = self._extract_patterns(input_data)
        
        # Update existing attractors with new input
        self._update_attractors_with_input(field_state, input_patterns)
        
        # Identify new attractors if needed
        new_attractors = self._identify_emergent_attractors(field_state, input_patterns)
        for attractor in new_attractors:
            field_state.add_attractor(attractor)
        
        # Calculate resonance patterns
        resonance = self._calculate_field_resonance(field_state, input_patterns)
        field_state.resonance_patterns.update(resonance)
        
        # Update field state
        field_state.update_field_state()
        
        # Calculate field interactions
        interactions = self._calculate_field_interactions(field_id)
        
        return {
            "field_state": field_state,
            "activated_attractors": [a for a in field_state.attractors.values() if a.activation_level > 0.3],
            "resonance_patterns": resonance,
            "field_interactions": interactions,
            "emergent_properties": self._identify_emergent_properties(field_state)
        }
    
    def orchestrate_multi_field_analysis(self, analysis_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate analysis across multiple neural fields for comprehensive insights.
        
        Args:
            analysis_context: Context data for multi-field analysis
            
        Returns:
            Comprehensive analysis results from all fields
        """
        self.time_step += 1
        field_results = {}
        
        # Phase 1: Discovery Field - Initial pattern identification
        discovery_field = self.initialize_field("discovery", FieldType.DISCOVERY, analysis_context)
        discovery_results = self.process_through_field("discovery", analysis_context)
        field_results["discovery"] = discovery_results
        
        # Phase 2: Reasoning Field - Logical analysis of discovered patterns
        reasoning_context = self._prepare_reasoning_context(analysis_context, discovery_results)
        reasoning_field = self.initialize_field("reasoning", FieldType.REASONING, reasoning_context)
        reasoning_results = self.process_through_field("reasoning", reasoning_context)
        field_results["reasoning"] = reasoning_results
        
        # Phase 3: Synthesis Field - Integration and emergence
        synthesis_context = self._prepare_synthesis_context(field_results)
        synthesis_field = self.initialize_field("synthesis", FieldType.SYNTHESIS, synthesis_context)
        synthesis_results = self.process_through_field("synthesis", synthesis_context)
        field_results["synthesis"] = synthesis_results
        
        # Calculate cross-field interactions
        cross_field_resonance = self._calculate_cross_field_resonance(field_results)
        
        # Identify emergent system properties
        emergent_properties = self._calculate_emergent_properties(field_results)
        
        # Update global state
        self._update_global_state(field_results, emergent_properties)
        
        return {
            "field_results": field_results,
            "cross_field_resonance": cross_field_resonance,
            "emergent_properties": emergent_properties,
            "global_state": self.global_state,
            "system_coherence": self._measure_system_coherence(),
            "time_step": self.time_step
        }
    
    def _calculate_context_load(self, context: Dict[str, Any]) -> int:
        """Calculate the computational load of context data."""
        context_str = json.dumps(context, default=str)
        return len(context_str.split())
    
    def _identify_initial_attractors(
        self, 
        context: Dict[str, Any], 
        config: Dict[str, Any]
    ) -> List[AttractorState]:
        """Identify initial attractors from context."""
        attractors = []
        threshold = config.get("attractor_threshold", 0.7)
        
        # Analyze context for pattern seeds
        if "codebase_tree" in context:
            # File structure patterns
            structure_attractor = AttractorState(
                pattern_id="file_structure",
                strength=0.8,
                basin_width=0.6,
                activation_level=0.5,
                decay_rate=0.03,
                resonance_frequency=1.2
            )
            attractors.append(structure_attractor)
        
        if "dependencies" in context:
            # Dependency patterns
            dependency_attractor = AttractorState(
                pattern_id="dependency_network",
                strength=0.7,
                basin_width=0.5,
                activation_level=0.4,
                decay_rate=0.05,
                resonance_frequency=1.0
            )
            attractors.append(dependency_attractor)
        
        if "code_patterns" in context:
            # Code architectural patterns
            arch_attractor = AttractorState(
                pattern_id="architectural_patterns",
                strength=0.9,
                basin_width=0.8,
                activation_level=0.6,
                decay_rate=0.02,
                resonance_frequency=1.5
            )
            attractors.append(arch_attractor)
        
        return attractors
    
    def _extract_patterns(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract patterns from input data with strength measures."""
        patterns = {}
        
        # Simple pattern extraction heuristics
        for key, value in input_data.items():
            if isinstance(value, str):
                # Text-based pattern strength
                patterns[f"text_pattern_{key}"] = min(len(value.split()) / 100.0, 1.0)
            elif isinstance(value, list):
                # List-based pattern strength
                patterns[f"list_pattern_{key}"] = min(len(value) / 50.0, 1.0)
            elif isinstance(value, dict):
                # Dictionary-based pattern strength
                patterns[f"dict_pattern_{key}"] = min(len(value) / 20.0, 1.0)
        
        return patterns
    
    def _update_attractors_with_input(
        self, 
        field_state: FieldState, 
        input_patterns: Dict[str, float]
    ):
        """Update existing attractors based on input patterns."""
        for attractor in field_state.attractors.values():
            # Find matching patterns
            pattern_strength = 0.0
            for pattern_name, strength in input_patterns.items():
                if self._patterns_resonate(attractor.pattern_id, pattern_name):
                    pattern_strength += strength
            
            # Update attractor activation
            if pattern_strength > 0:
                attractor.update_activation(pattern_strength)
    
    def _patterns_resonate(self, attractor_pattern: str, input_pattern: str) -> bool:
        """Check if two patterns resonate with each other."""
        # Simplified resonance check based on string similarity
        common_words = set(attractor_pattern.split()) & set(input_pattern.split())
        return len(common_words) > 0
    
    def _identify_emergent_attractors(
        self, 
        field_state: FieldState, 
        input_patterns: Dict[str, float]
    ) -> List[AttractorState]:
        """Identify new attractors that emerge from input patterns."""
        emergent_attractors = []
        threshold = 0.6
        
        for pattern_name, strength in input_patterns.items():
            if strength > threshold and pattern_name not in field_state.attractors:
                # Create new emergent attractor
                emergent_attractor = AttractorState(
                    pattern_id=pattern_name,
                    strength=strength,
                    basin_width=strength * 0.8,
                    activation_level=strength * 0.5,
                    decay_rate=0.05,
                    resonance_frequency=strength * 1.2
                )
                emergent_attractors.append(emergent_attractor)
        
        return emergent_attractors
    
    def _calculate_field_resonance(
        self, 
        field_state: FieldState, 
        input_patterns: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate resonance patterns within the field."""
        resonance = {}
        
        for attractor in field_state.attractors.values():
            resonance_strength = 0.0
            
            # Calculate resonance with input patterns
            for pattern_name, strength in input_patterns.items():
                if self._patterns_resonate(attractor.pattern_id, pattern_name):
                    resonance_strength += strength * attractor.activation_level
            
            # Calculate resonance with other attractors
            for other_attractor in field_state.attractors.values():
                if other_attractor.pattern_id != attractor.pattern_id:
                    if self._patterns_resonate(attractor.pattern_id, other_attractor.pattern_id):
                        resonance_strength += other_attractor.activation_level * 0.3
            
            resonance[attractor.pattern_id] = min(resonance_strength, 1.0)
        
        return resonance
    
    def _calculate_field_interactions(self, field_id: str) -> Dict[str, float]:
        """Calculate interactions between current field and other active fields."""
        interactions = {}
        current_field = self.active_fields[field_id]
        
        for other_field_id, other_field in self.active_fields.items():
            if other_field_id != field_id:
                # Calculate interaction strength based on resonance overlap
                interaction_strength = self._calculate_interaction_strength(current_field, other_field)
                interactions[other_field_id] = interaction_strength
        
        return interactions
    
    def _calculate_interaction_strength(self, field1: FieldState, field2: FieldState) -> float:
        """Calculate interaction strength between two fields."""
        # Find resonance pattern overlaps
        field1_patterns = set(field1.resonance_patterns.keys())
        field2_patterns = set(field2.resonance_patterns.keys())
        
        overlap = field1_patterns & field2_patterns
        if not overlap:
            return 0.0
        
        # Calculate weighted overlap
        total_strength = 0.0
        for pattern in overlap:
            strength1 = field1.resonance_patterns.get(pattern, 0.0)
            strength2 = field2.resonance_patterns.get(pattern, 0.0)
            total_strength += (strength1 * strength2) ** 0.5  # Geometric mean
        
        return min(total_strength / len(overlap), 1.0) if overlap else 0.0
    
    def _identify_emergent_properties(self, field_state: FieldState) -> List[Dict[str, Any]]:
        """Identify emergent properties within a field."""
        emergent_properties = []
        
        # High activation clusters
        high_activation_attractors = [
            a for a in field_state.attractors.values() 
            if a.activation_level > 0.7
        ]
        
        if len(high_activation_attractors) > 2:
            emergent_properties.append({
                "type": "activation_cluster",
                "patterns": [a.pattern_id for a in high_activation_attractors],
                "strength": np.mean([a.activation_level for a in high_activation_attractors])
            })
        
        # Resonance networks
        strong_resonance = {
            pattern: strength for pattern, strength in field_state.resonance_patterns.items()
            if strength > 0.6
        }
        
        if len(strong_resonance) > 1:
            emergent_properties.append({
                "type": "resonance_network",
                "patterns": list(strong_resonance.keys()),
                "average_strength": np.mean(list(strong_resonance.values()))
            })
        
        return emergent_properties
    
    def _prepare_reasoning_context(
        self, 
        original_context: Dict[str, Any], 
        discovery_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare context for reasoning field based on discovery results."""
        return {
            "original_context": original_context,
            "discovered_patterns": discovery_results.get("activated_attractors", []),
            "field_resonance": discovery_results.get("resonance_patterns", {}),
            "emergent_properties": discovery_results.get("emergent_properties", [])
        }
    
    def _prepare_synthesis_context(self, field_results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context for synthesis field based on all previous results."""
        return {
            "discovery_insights": field_results.get("discovery", {}),
            "reasoning_insights": field_results.get("reasoning", {}),
            "cross_field_patterns": self._extract_cross_field_patterns(field_results)
        }
    
    def _extract_cross_field_patterns(self, field_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract patterns that appear across multiple fields."""
        cross_patterns = {}
        
        # Find common resonance patterns
        all_resonance = {}
        for field_name, results in field_results.items():
            resonance = results.get("resonance_patterns", {})
            for pattern, strength in resonance.items():
                if pattern not in all_resonance:
                    all_resonance[pattern] = []
                all_resonance[pattern].append((field_name, strength))
        
        # Identify cross-field patterns
        for pattern, field_strengths in all_resonance.items():
            if len(field_strengths) > 1:  # Pattern appears in multiple fields
                cross_patterns[pattern] = {
                    "fields": [field_name for field_name, _ in field_strengths],
                    "average_strength": np.mean([strength for _, strength in field_strengths]),
                    "coherence": np.std([strength for _, strength in field_strengths])
                }
        
        return cross_patterns
    
    def _calculate_cross_field_resonance(self, field_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate resonance patterns across all active fields."""
        cross_resonance = {}
        
        fields = list(field_results.keys())
        for i, field1 in enumerate(fields):
            for field2 in fields[i+1:]:
                resonance_key = f"{field1}_{field2}"
                
                field1_state = self.active_fields.get(field1)
                field2_state = self.active_fields.get(field2)
                
                if field1_state and field2_state:
                    interaction_strength = self._calculate_interaction_strength(field1_state, field2_state)
                    cross_resonance[resonance_key] = interaction_strength
        
        return cross_resonance
    
    def _calculate_emergent_properties(self, field_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate system-level emergent properties."""
        emergent_properties = {
            "system_patterns": [],
            "coherence_measures": {},
            "stability_indicators": {},
            "evolution_trends": []
        }
        
        # System-wide pattern emergence
        all_emergent = []
        for field_name, results in field_results.items():
            field_emergent = results.get("emergent_properties", [])
            all_emergent.extend(field_emergent)
        
        # Group by type
        by_type = {}
        for prop in all_emergent:
            prop_type = prop.get("type", "unknown")
            if prop_type not in by_type:
                by_type[prop_type] = []
            by_type[prop_type].append(prop)
        
        emergent_properties["system_patterns"] = by_type
        
        # Calculate coherence measures
        for field_name in field_results.keys():
            if field_name in self.active_fields:
                field_state = self.active_fields[field_name]
                emergent_properties["coherence_measures"][field_name] = field_state.stability_measure
        
        return emergent_properties
    
    def _update_global_state(self, field_results: Dict[str, Any], emergent_properties: Dict[str, Any]):
        """Update global system state."""
        self.global_state["system_coherence"] = self._measure_system_coherence()
        self.global_state["emergent_patterns"] = emergent_properties
        self.global_state["active_fields"] = list(field_results.keys())
        self.global_state["time_step"] = self.time_step
    
    def _measure_system_coherence(self) -> float:
        """Measure overall system coherence across all fields."""
        if not self.active_fields:
            return 0.0
        
        # Calculate average field stability
        stability_scores = [field.stability_measure for field in self.active_fields.values()]
        average_stability = np.mean(stability_scores)
        
        # Calculate field interaction coherence
        interaction_scores = []
        fields = list(self.active_fields.values())
        for i, field1 in enumerate(fields):
            for field2 in fields[i+1:]:
                interaction = self._calculate_interaction_strength(field1, field2)
                interaction_scores.append(interaction)
        
        average_interaction = np.mean(interaction_scores) if interaction_scores else 0.0
        
        # Combine stability and interaction for overall coherence
        coherence = (average_stability * 0.7) + (average_interaction * 0.3)
        return min(coherence, 1.0)
    
    def get_field_summary(self, field_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of a specific field."""
        if field_id not in self.active_fields:
            return {"error": f"Field '{field_id}' not found"}
        
        field_state = self.active_fields[field_id]
        
        return {
            "field_id": field_id,
            "field_type": field_state.field_type.value,
            "activation_level": field_state.activation_level,
            "stability": field_state.stability_measure,
            "attractor_count": len(field_state.attractors),
            "active_attractors": len([a for a in field_state.attractors.values() if a.activation_level > 0.3]),
            "resonance_patterns": len(field_state.resonance_patterns),
            "capacity_usage": field_state.current_load / field_state.capacity if field_state.capacity > 0 else 0.0
        }