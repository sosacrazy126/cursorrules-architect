"""
Neural Field Manager - Real Context Engineering Implementation

This module implements a true neural field-based context management system
following the Context Engineering paradigm. It treats context as a continuous
semantic field with attractors, resonance, and field dynamics rather than
discrete token management.

Key Concepts:
- Neural Fields: Continuous semantic medium with field dynamics
- Attractors: Stable patterns that organize the semantic space  
- Resonance: Amplification of coherent patterns
- Symbolic Residue: Persistent information fragments across interactions
- Protocol Shells: Structured execution using Pareto-lang format
- Field Evolution: Self-improving recursive capabilities

Based on Context Engineering principles from:
https://github.com/dosco/llm-context-engineering
"""

import numpy as np
import json
import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import copy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FieldState(Enum):
    """States of field patterns and residues."""
    SURFACED = "surfaced"
    INTEGRATED = "integrated" 
    ECHO = "echo"
    ATTRACTOR = "attractor"
    TRANSIENT = "transient"

@dataclass
class Attractor:
    """Represents a stable pattern in the neural field."""
    id: str
    pattern: str
    strength: float
    basin_width: float
    location: Tuple[float, float] = field(default_factory=lambda: (0.5, 0.5))
    field_state: FieldState = FieldState.ATTRACTOR
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def __post_init__(self):
        # Ensure strength is bounded
        self.strength = max(0.0, min(1.0, self.strength))
        self.basin_width = max(0.0, min(1.0, self.basin_width))

@dataclass
class SymbolicResidue:
    """Represents persistent information fragments in the field."""
    id: str
    content: str
    strength: float
    field_state: FieldState
    origin_attractor_id: Optional[str] = None
    location: Tuple[float, float] = field(default_factory=lambda: (0.5, 0.5))
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    last_accessed: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def __post_init__(self):
        self.strength = max(0.0, min(1.0, self.strength))

@dataclass
class FieldMetrics:
    """Metrics for evaluating neural field properties."""
    coherence: float = 0.0
    stability: float = 0.0
    resonance: float = 0.0
    entropy: float = 0.0
    attractor_count: int = 0
    residue_count: int = 0
    field_capacity: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'coherence': self.coherence,
            'stability': self.stability, 
            'resonance': self.resonance,
            'entropy': self.entropy,
            'attractor_count': self.attractor_count,
            'residue_count': self.residue_count,
            'field_capacity': self.field_capacity
        }

class NeuralField:
    """
    Represents a continuous semantic field with neural field dynamics.
    
    This is the core implementation of neural field theory for context engineering,
    treating information as patterns in a continuous medium rather than discrete tokens.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the neural field with configuration parameters."""
        self.config = config
        
        # Field parameters from config
        field_config = config.get('field', {})
        self.decay_rate = field_config.get('decay_rate', 0.05)
        self.boundary_permeability = field_config.get('boundary_permeability', 0.8)
        self.resonance_bandwidth = field_config.get('resonance_bandwidth', 0.6)
        self.attractor_formation_threshold = field_config.get('attractor_formation_threshold', 0.7)
        self.max_capacity = field_config.get('max_capacity', 8000)
        self.reserved_tokens = field_config.get('reserved_tokens', 2000)
        
        # Initialize field components
        self.attractors: Dict[str, Attractor] = {}
        self.residues: Dict[str, SymbolicResidue] = {}
        self.field_matrix = np.zeros((100, 100))  # 2D field representation
        self.pattern_activations: Dict[str, float] = {}
        
        # Field state tracking
        self.cycle_count = 0
        self.last_metrics = FieldMetrics()
        
        # Initialize attractors from config
        self._initialize_attractors()
        
        logger.info(f"Neural field initialized with {len(self.attractors)} attractors")
    
    def _initialize_attractors(self):
        """Initialize attractors from configuration."""
        initial_attractors = self.config.get('attractors', [])
        
        for i, attractor_config in enumerate(initial_attractors):
            attractor = Attractor(
                id=f"init_attractor_{i}",
                pattern=attractor_config.get('pattern', ''),
                strength=attractor_config.get('strength', 0.8),
                basin_width=attractor_config.get('basin_width', 0.7)
            )
            self.attractors[attractor.id] = attractor
            
            # Update field matrix with attractor influence
            self._update_field_matrix_for_attractor(attractor)
    
    def inject_pattern(self, pattern: str, strength: float = 1.0, 
                      location: Optional[Tuple[float, float]] = None) -> str:
        """
        Inject a new information pattern into the field.
        
        Args:
            pattern: The information pattern to inject
            strength: Initial strength of the pattern
            location: Optional location in the field
            
        Returns:
            ID of the injected pattern
        """
        # Apply boundary permeability
        effective_strength = strength * self.boundary_permeability
        
        # Determine location
        if location is None:
            location = self._find_optimal_injection_location(pattern)
        
        # Check for similar existing patterns (blending)
        blend_config = self.config.get('operations', {}).get('injection', {})
        if blend_config.get('blend_similar', True):
            similar_attractor = self._find_similar_attractor(pattern, 
                                                           blend_config.get('blend_threshold', 0.7))
            if similar_attractor:
                return self._blend_with_attractor(similar_attractor, pattern, effective_strength)
        
        # Create new pattern/attractor if strength is high enough
        pattern_id = f"pattern_{len(self.pattern_activations)}"
        
        if effective_strength >= self.attractor_formation_threshold:
            # Create new attractor
            attractor = Attractor(
                id=pattern_id,
                pattern=pattern,
                strength=effective_strength,
                basin_width=self.resonance_bandwidth,
                location=location
            )
            self.attractors[attractor.id] = attractor
            self._update_field_matrix_for_attractor(attractor)
            logger.debug(f"Created new attractor: {pattern_id}")
        else:
            # Create transient pattern activation
            self.pattern_activations[pattern_id] = effective_strength
            logger.debug(f"Created transient pattern: {pattern_id}")
        
        # Process resonance effects
        self._process_resonance_effects(pattern, location, effective_strength)
        
        return pattern_id
    
    def measure_resonance(self, query_pattern: str) -> Dict[str, float]:
        """
        Measure how strongly the field resonates with a query pattern.
        
        Args:
            query_pattern: Pattern to measure resonance with
            
        Returns:
            Dictionary mapping attractor IDs to resonance scores
        """
        resonance_scores = {}
        
        for attractor_id, attractor in self.attractors.items():
            # Calculate semantic similarity (simplified implementation)
            similarity = self._calculate_semantic_similarity(query_pattern, attractor.pattern)
            
            # Apply resonance configuration
            resonance_config = self.config.get('resonance', {})
            threshold = resonance_config.get('threshold', 0.2)
            amplification = resonance_config.get('amplification', 1.2)
            
            if similarity >= threshold:
                # Apply distance decay
                distance = self._calculate_semantic_distance(query_pattern, attractor.pattern)
                distance_factor = resonance_config.get('distance_factor', 0.5)
                distance_decay = np.exp(-distance * distance_factor)
                
                # Calculate final resonance score
                resonance = similarity * amplification * distance_decay * attractor.strength
                resonance_scores[attractor_id] = min(1.0, resonance)
        
        return resonance_scores
    
    def create_resonance_scaffold(self, target_patterns: List[str]) -> Dict[str, Any]:
        """
        Create a resonance scaffold to amplify coherent patterns and dampen noise.
        
        This implements the field.resonance.scaffold protocol from Context Engineering.
        
        Args:
            target_patterns: Patterns to scaffold around
            
        Returns:
            Scaffold structure and metrics
        """
        scaffold = {
            'type': 'resonance_framework',
            'nodes': [],
            'connections': [],
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # Detect resonant patterns for each target
        for pattern in target_patterns:
            resonance_scores = self.measure_resonance(pattern)
            
            # Create scaffold nodes for strong resonances
            for attractor_id, score in resonance_scores.items():
                if score > 0.6:  # Strong resonance threshold
                    attractor = self.attractors[attractor_id]
                    node = {
                        'id': f"scaffold_node_{len(scaffold['nodes'])}",
                        'attractor_id': attractor_id,
                        'pattern': pattern,
                        'resonance_score': score,
                        'location': attractor.location,
                        'anchored': True
                    }
                    scaffold['nodes'].append(node)
        
        # Create connections between resonant nodes
        scaffold['connections'] = self._create_scaffold_connections(scaffold['nodes'])
        
        # Apply scaffolding effects to field
        self._apply_resonance_scaffold(scaffold)
        
        logger.info(f"Created resonance scaffold with {len(scaffold['nodes'])} nodes")
        return scaffold
    
    def surface_symbolic_residue(self, mode: str = 'recursive') -> List[SymbolicResidue]:
        """
        Surface symbolic residue in the field.
        
        Args:
            mode: Method for surfacing ('recursive', 'echo', 'integration')
            
        Returns:
            List of surfaced residues
        """
        surfaced_residues = []
        
        # Detect residue based on field state
        potential_residues = self._detect_potential_residue()
        
        for residue_data in potential_residues:
            if residue_data['strength'] >= 0.3:  # Minimum surfacing threshold
                residue = SymbolicResidue(
                    id=f"residue_{len(self.residues)}",
                    content=residue_data['content'],
                    strength=residue_data['strength'],
                    field_state=FieldState.SURFACED,
                    origin_attractor_id=residue_data.get('origin_attractor'),
                    location=residue_data.get('location', (0.5, 0.5))
                )
                
                self.residues[residue.id] = residue
                surfaced_residues.append(residue)
        
        logger.info(f"Surfaced {len(surfaced_residues)} symbolic residues")
        return surfaced_residues
    
    def calculate_field_metrics(self) -> FieldMetrics:
        """Calculate comprehensive field metrics."""
        metrics = FieldMetrics()
        
        # Coherence: how well-organized the field is
        metrics.coherence = self._calculate_coherence()
        
        # Stability: resistance to change
        metrics.stability = self._calculate_stability()
        
        # Resonance: average resonance strength
        metrics.resonance = self._calculate_average_resonance()
        
        # Entropy: measure of disorder
        metrics.entropy = self._calculate_field_entropy()
        
        # Counts
        metrics.attractor_count = len(self.attractors)
        metrics.residue_count = len(self.residues)
        
        # Capacity utilization
        current_tokens = self._estimate_token_usage()
        metrics.field_capacity = current_tokens / self.max_capacity
        
        self.last_metrics = metrics
        return metrics
    
    def apply_field_decay(self):
        """Apply natural decay to all field patterns."""
        # Decay attractors
        for attractor_id in list(self.attractors.keys()):
            attractor = self.attractors[attractor_id]
            
            # Apply protection for strong attractors
            persistence_config = self.config.get('persistence', {})
            protection = persistence_config.get('attractor_protection', 0.8)
            
            if attractor.strength > 0.8:  # Strong attractor
                decay_factor = 1 - (self.decay_rate * (1 - protection))
            else:
                decay_factor = 1 - self.decay_rate
            
            attractor.strength *= decay_factor
            
            # Remove very weak attractors
            if attractor.strength < 0.01:
                del self.attractors[attractor_id]
                logger.debug(f"Removed weak attractor: {attractor_id}")
        
        # Decay pattern activations
        for pattern_id in list(self.pattern_activations.keys()):
            self.pattern_activations[pattern_id] *= (1 - self.decay_rate)
            if self.pattern_activations[pattern_id] < 0.01:
                del self.pattern_activations[pattern_id]
        
        # Decay residues
        for residue_id in list(self.residues.keys()):
            residue = self.residues[residue_id]
            residue.strength *= (1 - self.decay_rate * 0.5)  # Slower decay for residues
            
            if residue.strength < 0.1:
                del self.residues[residue_id]
    
    def strengthen_on_access(self, pattern_id: str):
        """Strengthen patterns when accessed (if enabled)."""
        persistence_config = self.config.get('persistence', {})
        if not persistence_config.get('strengthen_on_access', True):
            return
        
        boost = persistence_config.get('access_boost', 0.3)
        
        if pattern_id in self.attractors:
            attractor = self.attractors[pattern_id]
            attractor.strength = min(1.0, attractor.strength + boost)
            logger.debug(f"Strengthened attractor {pattern_id} to {attractor.strength}")
        
        if pattern_id in self.residues:
            residue = self.residues[pattern_id]
            residue.strength = min(1.0, residue.strength + boost)
            residue.last_accessed = datetime.datetime.now().isoformat()
    
    def get_field_representation(self, format: str = 'markdown') -> str:
        """
        Generate a representation of the current field state.
        
        Args:
            format: Output format ('markdown', 'text', 'json')
            
        Returns:
            String representation of the field
        """
        output_config = self.config.get('output', {})
        max_attractors = output_config.get('max_attractors', 5)
        max_residues = output_config.get('max_residues', 5)
        include_metrics = output_config.get('include_metrics', True)
        
        if format == 'markdown':
            return self._generate_markdown_representation(max_attractors, max_residues, include_metrics)
        elif format == 'json':
            return self._generate_json_representation(max_attractors, max_residues, include_metrics)
        else:
            return self._generate_text_representation(max_attractors, max_residues, include_metrics)
    
    # Private helper methods
    
    def _find_optimal_injection_location(self, pattern: str) -> Tuple[float, float]:
        """Find optimal location for pattern injection."""
        # Simplified implementation - could use more sophisticated placement
        return (np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9))
    
    def _find_similar_attractor(self, pattern: str, threshold: float) -> Optional[Attractor]:
        """Find an existing attractor similar to the pattern."""
        for attractor in self.attractors.values():
            similarity = self._calculate_semantic_similarity(pattern, attractor.pattern)
            if similarity >= threshold:
                return attractor
        return None
    
    def _blend_with_attractor(self, attractor: Attractor, pattern: str, strength: float) -> str:
        """Blend a pattern with an existing attractor."""
        blend_config = self.config.get('operations', {}).get('injection', {})
        blend_ratio = blend_config.get('blend_ratio', 0.3)
        
        # Update attractor pattern (simplified blending)
        blended_pattern = f"{attractor.pattern} | {pattern}"
        attractor.pattern = blended_pattern
        
        # Update strength
        attractor.strength = attractor.strength * (1 - blend_ratio) + strength * blend_ratio
        
        logger.debug(f"Blended pattern with attractor {attractor.id}")
        return attractor.id
    
    def _calculate_semantic_similarity(self, pattern1: str, pattern2: str) -> float:
        """Calculate semantic similarity between patterns."""
        # Simplified implementation using word overlap
        words1 = set(pattern1.lower().split())
        words2 = set(pattern2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_semantic_distance(self, pattern1: str, pattern2: str) -> float:
        """Calculate semantic distance between patterns."""
        similarity = self._calculate_semantic_similarity(pattern1, pattern2)
        return 1.0 - similarity
    
    def _update_field_matrix_for_attractor(self, attractor: Attractor):
        """Update the field matrix to reflect attractor influence."""
        x, y = attractor.location
        matrix_x = int(x * self.field_matrix.shape[0])
        matrix_y = int(y * self.field_matrix.shape[1])
        
        # Create influence region
        influence_radius = int(attractor.basin_width * 10)
        for i in range(max(0, matrix_x - influence_radius), 
                      min(self.field_matrix.shape[0], matrix_x + influence_radius)):
            for j in range(max(0, matrix_y - influence_radius),
                          min(self.field_matrix.shape[1], matrix_y + influence_radius)):
                distance = np.sqrt((i - matrix_x)**2 + (j - matrix_y)**2)
                if distance <= influence_radius:
                    influence = attractor.strength * np.exp(-distance / influence_radius)
                    self.field_matrix[i, j] += influence
    
    def _process_resonance_effects(self, pattern: str, location: Tuple[float, float], strength: float):
        """Process resonance effects from a new pattern."""
        resonance_config = self.config.get('resonance', {})
        
        if not resonance_config.get('allow_circular', True):
            return
        
        # Find resonating attractors
        resonance_scores = self.measure_resonance(pattern)
        
        # Amplify resonating attractors
        amplification = resonance_config.get('amplification', 1.2)
        
        for attractor_id, score in resonance_scores.items():
            if score > resonance_config.get('threshold', 0.2):
                attractor = self.attractors[attractor_id]
                amplification_factor = 1 + (score * (amplification - 1))
                attractor.strength = min(1.0, attractor.strength * amplification_factor)
    
    def _create_scaffold_connections(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create connections between scaffold nodes."""
        connections = []
        
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                # Calculate connection strength based on resonance
                strength = (node1['resonance_score'] + node2['resonance_score']) / 2
                
                if strength > 0.5:  # Connection threshold
                    connection = {
                        'id': f"connection_{len(connections)}",
                        'source': node1['id'],
                        'target': node2['id'],
                        'type': 'resonance_bridge',
                        'strength': strength
                    }
                    connections.append(connection)
        
        return connections
    
    def _apply_resonance_scaffold(self, scaffold: Dict[str, Any]):
        """Apply scaffolding effects to the field."""
        # Amplify patterns connected by scaffold
        for connection in scaffold['connections']:
            strength = connection['strength']
            # Find source and target nodes
            source_node = next((n for n in scaffold['nodes'] if n['id'] == connection['source']), None)
            target_node = next((n for n in scaffold['nodes'] if n['id'] == connection['target']), None)
            
            if source_node and target_node:
                # Strengthen both attractors
                source_attractor = self.attractors.get(source_node['attractor_id'])
                target_attractor = self.attractors.get(target_node['attractor_id'])
                
                if source_attractor:
                    source_attractor.strength = min(1.0, source_attractor.strength * (1 + strength * 0.2))
                if target_attractor:
                    target_attractor.strength = min(1.0, target_attractor.strength * (1 + strength * 0.2))
    
    def _detect_potential_residue(self) -> List[Dict[str, Any]]:
        """Detect potential symbolic residue in the field."""
        potential_residues = []
        
        # Check weak attractors that might become residue
        for attractor in self.attractors.values():
            if 0.2 <= attractor.strength < 0.5:  # Residue strength range
                potential_residues.append({
                    'content': attractor.pattern,
                    'strength': attractor.strength,
                    'origin_attractor': attractor.id,
                    'location': attractor.location
                })
        
        # Check decaying pattern activations
        for pattern_id, strength in self.pattern_activations.items():
            if 0.1 <= strength < 0.3:
                potential_residues.append({
                    'content': f"pattern_{pattern_id}",
                    'strength': strength,
                    'location': (0.5, 0.5)  # Default location
                })
        
        return potential_residues
    
    def _calculate_coherence(self) -> float:
        """Calculate field coherence."""
        if len(self.attractors) < 2:
            return 1.0
        
        # Measure how well attractors are organized
        total_resonance = 0
        comparisons = 0
        
        attractors_list = list(self.attractors.values())
        for i, attractor1 in enumerate(attractors_list):
            for attractor2 in attractors_list[i+1:]:
                similarity = self._calculate_semantic_similarity(attractor1.pattern, attractor2.pattern)
                total_resonance += similarity
                comparisons += 1
        
        return total_resonance / comparisons if comparisons > 0 else 0.0
    
    def _calculate_stability(self) -> float:
        """Calculate field stability."""
        # Measure based on attractor strengths and distribution
        if not self.attractors:
            return 0.0
        
        strengths = [a.strength for a in self.attractors.values()]
        stability = np.mean(strengths) * (1 - np.std(strengths))
        return max(0.0, min(1.0, stability))
    
    def _calculate_average_resonance(self) -> float:
        """Calculate average resonance in the field."""
        if len(self.attractors) < 2:
            return 0.0
        
        total_resonance = 0
        count = 0
        
        for attractor in self.attractors.values():
            resonance_scores = self.measure_resonance(attractor.pattern)
            total_resonance += sum(resonance_scores.values())
            count += len(resonance_scores)
        
        return total_resonance / count if count > 0 else 0.0
    
    def _calculate_field_entropy(self) -> float:
        """Calculate field entropy (measure of disorder)."""
        if not self.attractors:
            return 1.0
        
        # Calculate entropy based on attractor strength distribution
        strengths = np.array([a.strength for a in self.attractors.values()])
        strengths = strengths / np.sum(strengths)  # Normalize
        
        # Calculate Shannon entropy
        entropy = -np.sum(strengths * np.log2(strengths + 1e-10))
        max_entropy = np.log2(len(strengths))
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _estimate_token_usage(self) -> int:
        """Estimate current token usage of the field."""
        total_tokens = 0
        
        # Count attractor tokens
        for attractor in self.attractors.values():
            total_tokens += len(attractor.pattern.split()) * 2  # Rough estimate
        
        # Count residue tokens
        for residue in self.residues.values():
            total_tokens += len(residue.content.split())
        
        return total_tokens
    
    def _generate_markdown_representation(self, max_attractors: int, max_residues: int, 
                                        include_metrics: bool) -> str:
        """Generate markdown representation of the field."""
        output = ["# Neural Field State\n"]
        
        # Field metrics
        if include_metrics:
            metrics = self.calculate_field_metrics()
            output.append("## Field Metrics")
            output.append(f"- **Coherence**: {metrics.coherence:.3f}")
            output.append(f"- **Stability**: {metrics.stability:.3f}")
            output.append(f"- **Resonance**: {metrics.resonance:.3f}")
            output.append(f"- **Entropy**: {metrics.entropy:.3f}")
            output.append(f"- **Capacity**: {metrics.field_capacity:.1%}")
            output.append("")
        
        # Active attractors
        output.append("## Active Attractors")
        sorted_attractors = sorted(self.attractors.values(), 
                                 key=lambda a: a.strength, reverse=True)
        
        for attractor in sorted_attractors[:max_attractors]:
            output.append(f"### {attractor.id}")
            output.append(f"- **Strength**: {attractor.strength:.3f}")
            output.append(f"- **Pattern**: {attractor.pattern}")
            output.append("")
        
        # Symbolic residue
        if self.residues:
            output.append("## Symbolic Residue")
            sorted_residues = sorted(self.residues.values(),
                                   key=lambda r: r.strength, reverse=True)
            
            for residue in sorted_residues[:max_residues]:
                output.append(f"- **{residue.id}** ({residue.strength:.3f}): {residue.content}")
            output.append("")
        
        return "\n".join(output)
    
    def _generate_json_representation(self, max_attractors: int, max_residues: int,
                                    include_metrics: bool) -> str:
        """Generate JSON representation of the field."""
        data = {
            'cycle_count': self.cycle_count,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        if include_metrics:
            metrics = self.calculate_field_metrics()
            data['metrics'] = metrics.to_dict()
        
        # Attractors
        sorted_attractors = sorted(self.attractors.values(),
                                 key=lambda a: a.strength, reverse=True)
        data['attractors'] = []
        for attractor in sorted_attractors[:max_attractors]:
            data['attractors'].append({
                'id': attractor.id,
                'pattern': attractor.pattern,
                'strength': attractor.strength,
                'basin_width': attractor.basin_width,
                'location': attractor.location
            })
        
        # Residues
        if self.residues:
            sorted_residues = sorted(self.residues.values(),
                                   key=lambda r: r.strength, reverse=True)
            data['residues'] = []
            for residue in sorted_residues[:max_residues]:
                data['residues'].append({
                    'id': residue.id,
                    'content': residue.content,
                    'strength': residue.strength,
                    'state': residue.field_state.value
                })
        
        return json.dumps(data, indent=2)
    
    def _generate_text_representation(self, max_attractors: int, max_residues: int,
                                    include_metrics: bool) -> str:
        """Generate text representation of the field."""
        output = ["Neural Field State"]
        output.append("=" * 20)
        
        if include_metrics:
            metrics = self.calculate_field_metrics()
            output.append(f"Coherence: {metrics.coherence:.3f} | Stability: {metrics.stability:.3f}")
            output.append(f"Resonance: {metrics.resonance:.3f} | Entropy: {metrics.entropy:.3f}")
            output.append("")
        
        output.append("Active Attractors:")
        sorted_attractors = sorted(self.attractors.values(),
                                 key=lambda a: a.strength, reverse=True)
        
        for attractor in sorted_attractors[:max_attractors]:
            output.append(f"  {attractor.id} ({attractor.strength:.3f}): {attractor.pattern}")
        
        if self.residues:
            output.append("\nSymbolic Residue:")
            sorted_residues = sorted(self.residues.values(),
                                   key=lambda r: r.strength, reverse=True)
            
            for residue in sorted_residues[:max_residues]:
                output.append(f"  {residue.id} ({residue.strength:.3f}): {residue.content}")
        
        return "\n".join(output)


class NeuralFieldManager:
    """
    Manager for neural field-based context engineering.
    
    This class orchestrates multiple neural fields and provides high-level
    operations for context management following Context Engineering principles.
    """
    
    def __init__(self, config_path: str):
        """Initialize the neural field manager with configuration."""
        with open(config_path, 'r') as f:
            import yaml
            self.config = yaml.safe_load(f)
        
        # Initialize primary field
        self.primary_field = NeuralField(self.config)
        
        # Initialize specialized fields if configured
        self.specialized_fields = {}
        multi_field_config = self.config.get('advanced', {}).get('multi_field', {})
        if multi_field_config.get('enabled', False):
            self._initialize_specialized_fields(multi_field_config)
        
        # Protocol execution state
        self.protocol_history = []
        
        logger.info("Neural Field Manager initialized")
    
    def process_context(self, context: str, query: Optional[str] = None) -> Dict[str, Any]:
        """
        Process context through the neural field system.
        
        Args:
            context: Context information to process
            query: Optional query to guide processing
            
        Returns:
            Processing results including field state and recommendations
        """
        # Inject context into primary field
        pattern_id = self.primary_field.inject_pattern(context)
        
        # Process query if provided
        resonance_scores = {}
        if query:
            resonance_scores = self.primary_field.measure_resonance(query)
        
        # Create resonance scaffold for coherent patterns
        scaffold = None
        if query:
            scaffold = self.primary_field.create_resonance_scaffold([query])
        
        # Surface symbolic residue
        residues = self.primary_field.surface_symbolic_residue()
        
        # Calculate field metrics
        metrics = self.primary_field.calculate_field_metrics()
        
        # Apply natural decay
        self.primary_field.apply_field_decay()
        
        # Generate field representation
        field_repr = self.primary_field.get_field_representation('markdown')
        
        return {
            'pattern_id': pattern_id,
            'resonance_scores': resonance_scores,
            'scaffold': scaffold,
            'surfaced_residues': [r.content for r in residues],
            'field_metrics': metrics.to_dict(),
            'field_representation': field_repr,
            'recommendations': self._generate_recommendations(metrics, resonance_scores)
        }
    
    def execute_protocol_shell(self, protocol_content: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a protocol shell using the neural field.
        
        Args:
            protocol_content: Protocol shell in Pareto-lang format
            input_data: Input data for the protocol
            
        Returns:
            Protocol execution results
        """
        # This would parse and execute Pareto-lang protocol shells
        # For now, return a placeholder implementation
        
        execution_result = {
            'protocol_name': 'neural_field_protocol',
            'status': 'executed',
            'field_updates': [],
            'output': input_data,  # Placeholder
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.protocol_history.append(execution_result)
        return execution_result
    
    def _initialize_specialized_fields(self, multi_field_config: Dict[str, Any]):
        """Initialize specialized neural fields."""
        fields_config = multi_field_config.get('fields', [])
        
        for field_config in fields_config:
            field_name = field_config['name']
            
            # Create specialized field configuration
            specialized_config = self.config.copy()
            specialized_config['field']['decay_rate'] = field_config.get('decay_rate', 0.05)
            
            # Initialize specialized field
            self.specialized_fields[field_name] = NeuralField(specialized_config)
            logger.info(f"Initialized specialized field: {field_name}")
    
    def _generate_recommendations(self, metrics: FieldMetrics, 
                                resonance_scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on field state."""
        recommendations = []
        
        # Coherence recommendations
        if metrics.coherence < 0.5:
            recommendations.append("Consider creating resonance scaffolding to improve field coherence")
        
        # Stability recommendations
        if metrics.stability < 0.6:
            recommendations.append("Field stability is low - strengthen key attractors")
        
        # Capacity recommendations
        if metrics.field_capacity > 0.8:
            recommendations.append("Field approaching capacity - consider residue compression")
        
        # Resonance recommendations
        if resonance_scores and max(resonance_scores.values()) < 0.3:
            recommendations.append("Low resonance detected - inject more relevant patterns")
        
        return recommendations
    
    def get_field_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of all fields."""
        summary = {
            'primary_field': {
                'metrics': self.primary_field.calculate_field_metrics().to_dict(),
                'attractor_count': len(self.primary_field.attractors),
                'residue_count': len(self.primary_field.residues)
            },
            'specialized_fields': {},
            'protocol_history_count': len(self.protocol_history)
        }
        
        for name, field in self.specialized_fields.items():
            summary['specialized_fields'][name] = {
                'metrics': field.calculate_field_metrics().to_dict(),
                'attractor_count': len(field.attractors),
                'residue_count': len(field.residues)
            }
        
        return summary