"""
core/context_engineering/field_dynamics.py

Implementation of neural field dynamics for enhanced pattern recognition and synthesis.
Maps to the neural field orchestration concepts for system-level intelligence emergence.

ENHANCED: Critical memory management and error handling added
"""

import logging
import time
import copy
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

class FieldDynamicsError(Exception):
    """Specific error for field dynamics failures."""
    pass

@dataclass
class AttractorState:
    """Represents an attractor in the neural field."""
    pattern_id: str
    strength: float
    basin_width: float
    activation_level: float = 0.0
    last_accessed: float = field(default_factory=time.time)
    memory_usage_bytes: int = 0
    
    def __post_init__(self):
        """Validate attractor state parameters."""
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("Attractor strength must be between 0.0 and 1.0")
        if not 0.0 <= self.basin_width <= 1.0:
            raise ValueError("Basin width must be between 0.0 and 1.0")
        if not 0.0 <= self.activation_level <= 1.0:
            raise ValueError("Activation level must be between 0.0 and 1.0")

@dataclass 
class ResonancePattern:
    """Represents a resonance pattern between fields."""
    source_field: str
    target_field: str
    resonance_frequency: float
    coupling_strength: float
    phase_offset: float = 0.0
    last_resonance: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """Validate resonance pattern parameters."""
        if not 0.0 <= self.resonance_frequency <= 10.0:
            raise ValueError("Resonance frequency must be between 0.0 and 10.0")
        if not 0.0 <= self.coupling_strength <= 1.0:
            raise ValueError("Coupling strength must be between 0.0 and 1.0")

@dataclass
class NeuralField:
    """Represents a neural field with dynamic properties."""
    field_id: str
    field_type: FieldType
    activation_map: Dict[str, float] = field(default_factory=dict)
    attractors: List[AttractorState] = field(default_factory=list)
    stability_measure: float = 0.0
    coherence_level: float = 0.0
    last_updated: float = field(default_factory=time.time)
    memory_usage_bytes: int = 0
    max_attractors: int = 100  # Prevent unlimited growth
    
    def __post_init__(self):
        """Initialize field with validation."""
        if not 0.0 <= self.stability_measure <= 1.0:
            self.stability_measure = 0.0
        if not 0.0 <= self.coherence_level <= 1.0:
            self.coherence_level = 0.0
        
        # Estimate initial memory usage
        self._update_memory_usage()
    
    def _update_memory_usage(self):
        """Update memory usage estimate."""
        try:
            # Rough estimate of memory usage
            base_size = 200  # Base object overhead
            activation_size = len(str(self.activation_map)) * 4  # Rough bytes per char
            attractors_size = len(self.attractors) * 150  # Rough bytes per attractor
            
            self.memory_usage_bytes = base_size + activation_size + attractors_size
            
            # Update attractor memory usage
            for attractor in self.attractors:
                attractor.memory_usage_bytes = 150  # Rough estimate
        except Exception as e:
            logger.warning(f"Memory usage calculation failed: {e}")
            self.memory_usage_bytes = 1000  # Conservative estimate
    
    def add_attractor(self, attractor: AttractorState) -> bool:
        """Add attractor with memory limits."""
        try:
            # Check if we're at the limit
            if len(self.attractors) >= self.max_attractors:
                # Remove weakest attractor
                weakest_idx = min(range(len(self.attractors)), 
                                key=lambda i: self.attractors[i].strength)
                removed_attractor = self.attractors.pop(weakest_idx)
                logger.debug(f"Removed weak attractor {removed_attractor.pattern_id} to make room")
            
            self.attractors.append(attractor)
            self._update_memory_usage()
            self.last_updated = time.time()
            return True
            
        except Exception as e:
            logger.error(f"Failed to add attractor: {e}")
            return False
    
    def cleanup_inactive_attractors(self, inactivity_threshold: float = 600) -> int:
        """Remove attractors that haven't been accessed recently."""
        try:
            current_time = time.time()
            initial_count = len(self.attractors)
            
            # Keep only recently accessed or strong attractors
            self.attractors = [
                attractor for attractor in self.attractors
                if (current_time - attractor.last_accessed < inactivity_threshold 
                    or attractor.strength > 0.7)
            ]
            
            removed_count = initial_count - len(self.attractors)
            if removed_count > 0:
                self._update_memory_usage()
                logger.debug(f"Cleaned up {removed_count} inactive attractors from field {self.field_id}")
            
            return removed_count
            
        except Exception as e:
            logger.error(f"Attractor cleanup failed: {e}")
            return 0

class FieldDynamics:
    """Neural field dynamics with memory management and error handling."""
    
    def __init__(self, max_fields: int = 50, memory_limit_mb: int = 100):
        """Initialize with resource limits."""
        try:
            self.active_fields: Dict[str, NeuralField] = {}
            self.field_interactions: Dict[str, ResonancePattern] = {}
            self.system_coherence: float = 0.0
            self.orchestration_state: Dict[str, Any] = {}
            
            # Resource management
            self.max_fields = max_fields
            self.memory_limit_bytes = memory_limit_mb * 1024 * 1024
            self.current_memory_usage = 0
            self.last_cleanup_time = time.time()
            self.cleanup_interval = 300  # 5 minutes
            
            # Performance tracking
            self.operation_count = 0
            self.error_count = 0
            self.last_performance_check = time.time()
            
            logger.info(f"FieldDynamics initialized with max_fields={max_fields}, memory_limit={memory_limit_mb}MB")
            
        except Exception as e:
            logger.error(f"FieldDynamics initialization failed: {e}")
            raise FieldDynamicsError(f"Failed to initialize FieldDynamics: {e}")
    
    def create_field(self, field_id: str, field_type: FieldType, context_data: Dict[str, Any]) -> bool:
        """Create a new neural field with error handling and memory management."""
        try:
            # Check resource limits
            if len(self.active_fields) >= self.max_fields:
                if not self._make_room_for_new_field():
                    logger.warning(f"Cannot create field {field_id}: at max capacity and cleanup failed")
                    return False
            
            # Validate inputs
            if not field_id or not isinstance(field_id, str):
                raise ValueError("field_id must be a non-empty string")
            
            if field_id in self.active_fields:
                logger.warning(f"Field {field_id} already exists, updating instead")
                return self.update_field(field_id, context_data)
            
            # Create new field
            new_field = NeuralField(
                field_id=field_id,
                field_type=field_type,
                max_attractors=min(100, self.max_fields * 2)  # Scale with system capacity
            )
            
            # Initialize field with context data
            self._initialize_field_from_context(new_field, context_data)
            
            # Check memory usage
            if self._would_exceed_memory_limit(new_field):
                logger.warning(f"Creating field {field_id} would exceed memory limit")
                if not self._free_memory():
                    logger.error(f"Cannot create field {field_id}: memory limit reached")
                    return False
            
            # Add field to active fields
            self.active_fields[field_id] = new_field
            self._update_memory_tracking()
            
            logger.debug(f"Created field {field_id} of type {field_type.value}")
            return True
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Failed to create field {field_id}: {e}")
            return False
    
    def _make_room_for_new_field(self) -> bool:
        """Make room for a new field by removing the least active one."""
        try:
            if not self.active_fields:
                return True
            
            # Find least recently used field
            oldest_field_id = min(
                self.active_fields.keys(),
                key=lambda fid: self.active_fields[fid].last_updated
            )
            
            logger.debug(f"Removing least active field {oldest_field_id} to make room")
            return self.remove_field(oldest_field_id)
            
        except Exception as e:
            logger.error(f"Failed to make room for new field: {e}")
            return False
    
    def _initialize_field_from_context(self, field: NeuralField, context_data: Dict[str, Any]):
        """Initialize field from context data with error handling."""
        try:
            # Safely extract activation patterns
            if isinstance(context_data, dict):
                # Create activation map from context keys
                for key, value in context_data.items():
                    if isinstance(key, str) and len(key) < 100:  # Reasonable key length
                        if isinstance(value, (int, float)):
                            field.activation_map[key] = float(value) / 100.0  # Normalize
                        elif isinstance(value, str) and len(value) < 1000:  # Reasonable string length
                            field.activation_map[key] = len(value) / 1000.0  # Length-based activation
                
                # Limit activation map size
                if len(field.activation_map) > 50:
                    # Keep only top 50 activations
                    sorted_activations = sorted(
                        field.activation_map.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                    field.activation_map = dict(sorted_activations[:50])
            
            # Initialize basic coherence
            field.coherence_level = min(0.5, len(field.activation_map) / 20.0)
            field.stability_measure = 0.3  # Initial stability
            
        except Exception as e:
            logger.warning(f"Field initialization from context failed: {e}")
            # Provide minimal initialization
            field.activation_map = {"default": 0.1}
            field.coherence_level = 0.1
            field.stability_measure = 0.1
    
    def _would_exceed_memory_limit(self, new_field: NeuralField) -> bool:
        """Check if adding a field would exceed memory limits."""
        try:
            estimated_usage = self.current_memory_usage + new_field.memory_usage_bytes
            return estimated_usage > self.memory_limit_bytes
        except Exception:
            return False  # If we can't calculate, allow the operation
    
    def _free_memory(self) -> bool:
        """Free memory by cleaning up fields and attractors."""
        try:
            initial_usage = self.current_memory_usage
            
            # Clean up all fields
            for field in self.active_fields.values():
                field.cleanup_inactive_attractors()
            
            # Remove empty or very weak fields
            weak_fields = [
                field_id for field_id, field in self.active_fields.items()
                if field.stability_measure < 0.1 and len(field.attractors) == 0
            ]
            
            for field_id in weak_fields:
                self.remove_field(field_id)
            
            self._update_memory_tracking()
            
            freed_memory = initial_usage - self.current_memory_usage
            logger.debug(f"Freed {freed_memory} bytes of memory")
            
            return freed_memory > 0
            
        except Exception as e:
            logger.error(f"Memory cleanup failed: {e}")
            return False
    
    def _update_memory_tracking(self):
        """Update current memory usage tracking."""
        try:
            total_usage = 0
            for field in self.active_fields.values():
                field._update_memory_usage()
                total_usage += field.memory_usage_bytes
            
            # Add overhead for interactions and orchestration state
            total_usage += len(str(self.field_interactions)) * 4
            total_usage += len(str(self.orchestration_state)) * 4
            
            self.current_memory_usage = total_usage
            
        except Exception as e:
            logger.warning(f"Memory tracking update failed: {e}")
    
    def update_field(self, field_id: str, new_data: Dict[str, Any]) -> bool:
        """Update field with new data and error handling."""
        try:
            if field_id not in self.active_fields:
                logger.warning(f"Field '{field_id}' not found for update")
                return False
            
            field = self.active_fields[field_id]
            field.last_updated = time.time()
            
            # Update activation map safely
            if isinstance(new_data, dict):
                for key, value in new_data.items():
                    if isinstance(key, str) and len(key) < 100:
                        if isinstance(value, (int, float)) and -1000 <= value <= 1000:
                            field.activation_map[key] = max(0.0, min(1.0, float(value)))
            
            # Update field properties
            field.stability_measure = min(1.0, field.stability_measure + 0.1)
            field.coherence_level = min(1.0, len(field.activation_map) / 50.0)
            
            field._update_memory_usage()
            self.operation_count += 1
            
            return True
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Failed to update field {field_id}: {e}")
            return False
    
    def remove_field(self, field_id: str) -> bool:
        """Remove a field and clean up references."""
        try:
            if field_id not in self.active_fields:
                logger.warning(f"Field '{field_id}' not found for removal")
                return False
            
            # Remove field
            removed_field = self.active_fields.pop(field_id)
            
            # Clean up field interactions
            interactions_to_remove = [
                interaction_id for interaction_id, pattern in self.field_interactions.items()
                if pattern.source_field == field_id or pattern.target_field == field_id
            ]
            
            for interaction_id in interactions_to_remove:
                del self.field_interactions[interaction_id]
            
            # Update memory tracking
            self._update_memory_tracking()
            
            logger.debug(f"Removed field {field_id} and {len(interactions_to_remove)} interactions")
            return True
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Failed to remove field {field_id}: {e}")
            return False
    
    def cleanup_inactive_fields(self, inactivity_threshold: float = 600) -> int:
        """Clean up inactive fields and attractors."""
        try:
            current_time = time.time()
            initial_field_count = len(self.active_fields)
            
            # Clean up attractors in all fields
            total_attractors_removed = 0
            for field in self.active_fields.values():
                total_attractors_removed += field.cleanup_inactive_attractors(inactivity_threshold)
            
            # Remove completely inactive fields
            inactive_fields = [
                field_id for field_id, field in self.active_fields.items()
                if (current_time - field.last_updated > inactivity_threshold 
                    and field.stability_measure < 0.2)
            ]
            
            for field_id in inactive_fields:
                self.remove_field(field_id)
            
            # Clean up old interactions
            old_interactions = [
                interaction_id for interaction_id, pattern in self.field_interactions.items()
                if current_time - pattern.last_resonance > inactivity_threshold
            ]
            
            for interaction_id in old_interactions:
                del self.field_interactions[interaction_id]
            
            removed_fields = initial_field_count - len(self.active_fields)
            
            if removed_fields > 0 or total_attractors_removed > 0 or len(old_interactions) > 0:
                logger.info(f"Cleanup completed: {removed_fields} fields, {total_attractors_removed} attractors, {len(old_interactions)} interactions removed")
            
            self._update_memory_tracking()
            self.last_cleanup_time = current_time
            
            return removed_fields
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Field cleanup failed: {e}")
            return 0
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics."""
        try:
            current_time = time.time()
            uptime = current_time - (current_time - 3600)  # Rough uptime estimate
            
            health_metrics = {
                "active_fields": len(self.active_fields),
                "max_fields": self.max_fields,
                "field_utilization": len(self.active_fields) / self.max_fields,
                "memory_usage_mb": self.current_memory_usage / (1024 * 1024),
                "memory_limit_mb": self.memory_limit_bytes / (1024 * 1024),
                "memory_utilization": self.current_memory_usage / self.memory_limit_bytes,
                "operation_count": self.operation_count,
                "error_count": self.error_count,
                "error_rate": self.error_count / max(1, self.operation_count),
                "last_cleanup": current_time - self.last_cleanup_time,
                "system_coherence": self.system_coherence,
                "health_status": "healthy"
            }
            
            # Determine health status
            if health_metrics["error_rate"] > 0.1:
                health_metrics["health_status"] = "unhealthy"
            elif health_metrics["memory_utilization"] > 0.9:
                health_metrics["health_status"] = "critical"
            elif health_metrics["field_utilization"] > 0.9:
                health_metrics["health_status"] = "warning"
            
            return health_metrics
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "health_status": "error",
                "error_message": str(e),
                "active_fields": len(self.active_fields) if hasattr(self, 'active_fields') else 0
            }