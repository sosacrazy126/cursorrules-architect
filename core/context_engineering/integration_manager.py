"""
core/context_engineering/integration_manager.py

Central integration manager for context engineering components.
Orchestrates atomic prompting, field dynamics, cognitive tools, and pattern synthesis
across all CursorRules architect phases.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

from .foundations import ContextFoundations
from .patterns import PromptPatterns  
from .field_dynamics import FieldDynamics, FieldType
from .cognitive_tools import CognitiveToolkit

logger = logging.getLogger(__name__)

class IntegrationPhase(Enum):
    """Context engineering integration phases."""
    ATOMIC = "atomic"                # Phase 1 - Atomic prompting
    MOLECULAR = "molecular"          # Phase 2 - Context building
    CELLULAR = "cellular"           # Phase 3 - Memory integration
    ORGANIC = "organic"             # Phase 4 - Application synthesis
    COGNITIVE = "cognitive"         # Phase 5 - Tool integration
    ORCHESTRATION = "orchestration" # Final - System synthesis

@dataclass
class IntegrationConfig:
    """Configuration for context engineering integration."""
    enable_atomic_prompting: bool = True
    enable_field_dynamics: bool = True
    enable_cognitive_tools: bool = True
    enable_pattern_synthesis: bool = True
    optimization_mode: str = "balanced"  # "efficiency", "depth", "balanced"
    field_capacity: int = 8000
    token_efficiency_threshold: float = 0.7
    coherence_threshold: float = 0.6

class ContextEngineeringIntegrationManager:
    """
    Central manager for integrating context engineering capabilities
    with CursorRules architect analysis phases.
    """
    
    def __init__(self, config: Optional[IntegrationConfig] = None):
        """Initialize integration manager with configuration."""
        self.config = config or IntegrationConfig()
        
        # Initialize core components
        self.foundations = ContextFoundations()
        self.patterns = PromptPatterns()
        self.field_dynamics = FieldDynamics()
        self.cognitive_toolkit = CognitiveToolkit()
        
        # Integration state
        self.phase_contexts = {}
        self.field_states = {}
        self.integration_metrics = {
            "phases_enhanced": 0,
            "total_coherence": 0.0,
            "optimization_efficiency": 0.0,
            "emergent_patterns_detected": 0
        }
        
        logger.info("Initialized Context Engineering Integration Manager")
    
    def enhance_phase(
        self,
        phase_name: str,
        phase_data: Dict[str, Any],
        previous_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhance a CursorRules architect phase with context engineering.
        
        Args:
            phase_name: Name of the phase being enhanced
            phase_data: Input data for the phase
            previous_context: Context from previous phases
            
        Returns:
            Enhanced phase results with context engineering insights
        """
        logger.info(f"Enhancing {phase_name} with context engineering")
        
        # Determine integration phase
        integration_phase = self._map_to_integration_phase(phase_name)
        
        # Initialize phase-specific enhancement
        enhancement_results = {
            "phase_name": phase_name,
            "integration_phase": integration_phase.value,
            "original_data": phase_data,
            "enhanced_data": {},
            "context_engineering": {},
            "integration_metrics": {}
        }
        
        # Apply phase-specific enhancements
        if integration_phase == IntegrationPhase.ATOMIC:
            enhancement_results = self._enhance_atomic_phase(enhancement_results, phase_data)
        elif integration_phase == IntegrationPhase.MOLECULAR:
            enhancement_results = self._enhance_molecular_phase(enhancement_results, phase_data, previous_context)
        elif integration_phase == IntegrationPhase.CELLULAR:
            enhancement_results = self._enhance_cellular_phase(enhancement_results, phase_data, previous_context)
        elif integration_phase == IntegrationPhase.ORGANIC:
            enhancement_results = self._enhance_organic_phase(enhancement_results, phase_data, previous_context)
        elif integration_phase == IntegrationPhase.COGNITIVE:
            enhancement_results = self._enhance_cognitive_phase(enhancement_results, phase_data, previous_context)
        else:
            # Default enhancement for unknown phases
            enhancement_results = self._enhance_default_phase(enhancement_results, phase_data)
        
        # Store phase context for future phases
        self.phase_contexts[phase_name] = enhancement_results
        
        # Update integration metrics
        self._update_integration_metrics(enhancement_results)
        
        logger.info(f"Enhanced {phase_name} with coherence: {enhancement_results['integration_metrics'].get('coherence', 0.0):.2f}")
        
        return enhancement_results
    
    def orchestrate_multi_phase_analysis(
        self,
        phases_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Orchestrate context engineering across multiple phases.
        
        Args:
            phases_data: Data for all phases to be enhanced
            
        Returns:
            Comprehensive multi-phase orchestration results
        """
        logger.info("Starting multi-phase context engineering orchestration")
        
        orchestration_results = {
            "enhanced_phases": {},
            "cross_phase_synthesis": {},
            "field_orchestration": {},
            "emergent_intelligence": {},
            "system_coherence": 0.0
        }
        
        # Process phases in sequence, building context
        previous_context = None
        phase_order = ["phase_1", "phase_2", "phase_3", "phase_4", "phase_5", "final_analysis"]
        
        for phase_name in phase_order:
            if phase_name in phases_data:
                # Enhance individual phase
                enhanced_phase = self.enhance_phase(phase_name, phases_data[phase_name], previous_context)
                orchestration_results["enhanced_phases"][phase_name] = enhanced_phase
                
                # Update context for next phase
                previous_context = self._extract_context_for_next_phase(enhanced_phase)
        
        # Perform cross-phase synthesis
        orchestration_results["cross_phase_synthesis"] = self._synthesize_across_phases(
            orchestration_results["enhanced_phases"]
        )
        
        # Orchestrate neural fields
        orchestration_results["field_orchestration"] = self._orchestrate_neural_fields(
            orchestration_results["enhanced_phases"]
        )
        
        # Identify emergent intelligence
        orchestration_results["emergent_intelligence"] = self._identify_emergent_intelligence(
            orchestration_results
        )
        
        # Calculate system coherence
        orchestration_results["system_coherence"] = self._calculate_system_coherence(
            orchestration_results
        )
        
        logger.info(f"Multi-phase orchestration completed with system coherence: {orchestration_results['system_coherence']:.2f}")
        
        return orchestration_results
    
    def _map_to_integration_phase(self, phase_name: str) -> IntegrationPhase:
        """Map CursorRules phase to context engineering integration phase."""
        phase_mapping = {
            "phase_1": IntegrationPhase.ATOMIC,
            "phase_2": IntegrationPhase.MOLECULAR,
            "phase_3": IntegrationPhase.CELLULAR,
            "phase_4": IntegrationPhase.ORGANIC,
            "phase_5": IntegrationPhase.COGNITIVE,
            "final_analysis": IntegrationPhase.ORCHESTRATION
        }
        
        return phase_mapping.get(phase_name, IntegrationPhase.ATOMIC)
    
    def _enhance_atomic_phase(
        self,
        enhancement_results: Dict[str, Any],
        phase_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhance phase with atomic prompting patterns."""
        
        # Create atomic prompts
        atomic_prompts = {}
        if "codebase_tree" in phase_data:
            atomic_prompts["structure"] = self.foundations.create_atomic_prompt(
                "discovery",
                str(phase_data["codebase_tree"][:100]) + "...",
                ["Focus on architectural patterns", "Identify modular structure"]
            )
        
        if "dependencies" in phase_data:
            atomic_prompts["dependencies"] = self.foundations.create_atomic_prompt(
                "analysis",
                str(phase_data["dependencies"]),
                ["Map dependency relationships", "Assess complexity"]
            )
        
        # Initialize discovery field
        field_id = "atomic_discovery"
        discovery_field = self.field_dynamics.initialize_field(
            field_id, FieldType.DISCOVERY, phase_data
        )
        self.field_states[field_id] = discovery_field
        
        # Apply cognitive understanding
        cognitive_results = self.cognitive_toolkit.apply_cognitive_operations(phase_data)
        
        # Enhance results
        enhancement_results["enhanced_data"] = {
            **phase_data,
            "atomic_prompts": atomic_prompts,
            "field_guidance": "Focus on initial pattern discovery"
        }
        
        enhancement_results["context_engineering"] = {
            "atomic_prompting": {
                "prompts": atomic_prompts,
                "efficiency_score": self._calculate_prompt_efficiency(atomic_prompts)
            },
            "field_dynamics": {
                "field_state": discovery_field,
                "initialization_success": True
            },
            "cognitive_processing": cognitive_results
        }
        
        enhancement_results["integration_metrics"] = {
            "coherence": discovery_field.stability_measure,
            "efficiency": self._calculate_prompt_efficiency(atomic_prompts),
            "cognitive_depth": cognitive_results.get("meta_analysis", {}).get("cognitive_depth", 0.0)
        }
        
        return enhancement_results
    
    def _enhance_molecular_phase(
        self,
        enhancement_results: Dict[str, Any],
        phase_data: Dict[str, Any],
        previous_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Enhance phase with molecular context building."""
        
        # Create molecular context from previous phase
        molecular_context = {}
        if previous_context:
            molecular_context = self.patterns.chain_phases(
                {"phase_1": str(previous_context)},
                "phase_2"
            )
        
        # Create context molecules for planning
        planning_molecule = self.patterns.create_analysis_molecule(
            "phase_2_planning",
            f"Planning context: {phase_data}",
            [molecular_context] if molecular_context else [],
            "analysis_chain"
        )
        
        # Initialize reasoning field
        field_id = "molecular_reasoning"
        reasoning_field = self.field_dynamics.initialize_field(
            field_id, FieldType.REASONING, phase_data
        )
        self.field_states[field_id] = reasoning_field
        
        # Enhance results
        enhancement_results["enhanced_data"] = {
            **phase_data,
            "molecular_context": molecular_context,
            "context_molecule": planning_molecule.synthesize(),
            "field_guidance": "Build connected analysis patterns"
        }
        
        enhancement_results["context_engineering"] = {
            "molecular_patterns": {
                "context_chain": molecular_context,
                "planning_molecule": planning_molecule.synthesize(),
                "pattern_type": "analysis_chain"
            },
            "field_dynamics": {
                "field_state": reasoning_field,
                "field_type": "reasoning"
            }
        }
        
        enhancement_results["integration_metrics"] = {
            "coherence": reasoning_field.stability_measure,
            "molecular_complexity": len(molecular_context) if isinstance(molecular_context, str) else 0,
            "pattern_richness": 0.8  # Simplified metric
        }
        
        return enhancement_results
    
    def _enhance_cellular_phase(
        self,
        enhancement_results: Dict[str, Any],
        phase_data: Dict[str, Any],
        previous_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Enhance phase with cellular memory integration."""
        
        # Build memory-integrated context
        memory_context = {}
        if previous_context:
            # Track context evolution
            self.patterns.track_context_evolution("phase_3", str(phase_data))
            memory_context = self.patterns.get_evolution_summary()
        
        # Initialize memory field
        field_id = "cellular_memory"
        memory_field = self.field_dynamics.initialize_field(
            field_id, FieldType.MEMORY, phase_data
        )
        self.field_states[field_id] = memory_field
        
        # Process through field for memory integration
        memory_processing = self.field_dynamics.process_through_field(
            field_id, phase_data
        )
        
        # Enhance results
        enhancement_results["enhanced_data"] = {
            **phase_data,
            "memory_context": memory_context,
            "memory_integration": memory_processing,
            "field_guidance": "Integrate persistent patterns and memory"
        }
        
        enhancement_results["context_engineering"] = {
            "cellular_memory": {
                "memory_context": memory_context,
                "memory_processing": memory_processing,
                "evolution_tracking": True
            },
            "field_dynamics": {
                "field_state": memory_field,
                "processing_results": memory_processing
            }
        }
        
        enhancement_results["integration_metrics"] = {
            "coherence": memory_field.stability_measure,
            "memory_depth": len(memory_processing.get("activated_attractors", [])),
            "evolution_complexity": memory_context.get("total_phases", 0)
        }
        
        return enhancement_results
    
    def _enhance_organic_phase(
        self,
        enhancement_results: Dict[str, Any],
        phase_data: Dict[str, Any],
        previous_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Enhance phase with organic application synthesis."""
        
        # Create synthesis context from all previous phases
        synthesis_context = {}
        if previous_context:
            synthesis_context = {
                "accumulated_insights": previous_context,
                "synthesis_target": "application_patterns",
                "organic_integration": True
            }
        
        # Initialize synthesis field
        field_id = "organic_synthesis"
        synthesis_field = self.field_dynamics.initialize_field(
            field_id, FieldType.SYNTHESIS, synthesis_context
        )
        self.field_states[field_id] = synthesis_field
        
        # Orchestrate multi-field analysis
        if len(self.field_states) > 1:
            multi_field_results = self.field_dynamics.orchestrate_multi_field_analysis(
                synthesis_context
            )
        else:
            multi_field_results = {"single_field": True}
        
        # Enhance results
        enhancement_results["enhanced_data"] = {
            **phase_data,
            "synthesis_context": synthesis_context,
            "multi_field_orchestration": multi_field_results,
            "field_guidance": "Synthesize organic application patterns"
        }
        
        enhancement_results["context_engineering"] = {
            "organic_synthesis": {
                "synthesis_context": synthesis_context,
                "multi_field_results": multi_field_results,
                "orchestration_enabled": len(self.field_states) > 1
            },
            "field_dynamics": {
                "synthesis_field": synthesis_field,
                "multi_field_coherence": multi_field_results.get("system_coherence", 0.0)
            }
        }
        
        enhancement_results["integration_metrics"] = {
            "coherence": synthesis_field.stability_measure,
            "synthesis_quality": multi_field_results.get("system_coherence", 0.0),
            "organic_complexity": len(str(synthesis_context)) / 1000.0
        }
        
        return enhancement_results
    
    def _enhance_cognitive_phase(
        self,
        enhancement_results: Dict[str, Any],
        phase_data: Dict[str, Any],
        previous_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Enhance phase with cognitive tools integration."""
        
        # Apply comprehensive cognitive operations
        cognitive_results = self.cognitive_toolkit.apply_cognitive_operations(phase_data)
        
        # Get cognitive operation summary
        operation_summary = self.cognitive_toolkit.get_operation_summary()
        
        # Enhance results
        enhancement_results["enhanced_data"] = {
            **phase_data,
            "cognitive_enhancement": cognitive_results,
            "operation_summary": operation_summary,
            "field_guidance": "Apply comprehensive cognitive tools"
        }
        
        enhancement_results["context_engineering"] = {
            "cognitive_tools": {
                "full_cognitive_results": cognitive_results,
                "operation_summary": operation_summary,
                "cognitive_efficiency": operation_summary.get("processing_efficiency", 0.0)
            }
        }
        
        enhancement_results["integration_metrics"] = {
            "cognitive_depth": cognitive_results.get("meta_analysis", {}).get("cognitive_depth", 0.0),
            "processing_efficiency": operation_summary.get("processing_efficiency", 0.0),
            "synthesis_quality": cognitive_results.get("composition", {}).get("synthesis_quality", {}).get("overall_score", 0.0)
        }
        
        return enhancement_results
    
    def _enhance_default_phase(
        self,
        enhancement_results: Dict[str, Any],
        phase_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Default enhancement for unknown phases."""
        
        # Apply basic cognitive processing
        cognitive_results = self.cognitive_toolkit.apply_cognitive_operations(phase_data)
        
        enhancement_results["enhanced_data"] = {
            **phase_data,
            "basic_cognitive_enhancement": cognitive_results,
            "field_guidance": "Apply basic context engineering patterns"
        }
        
        enhancement_results["context_engineering"] = {
            "basic_enhancement": {
                "cognitive_results": cognitive_results,
                "enhancement_type": "default"
            }
        }
        
        enhancement_results["integration_metrics"] = {
            "coherence": 0.5,  # Default coherence
            "enhancement_level": "basic"
        }
        
        return enhancement_results
    
    def _extract_context_for_next_phase(self, enhanced_phase: Dict[str, Any]) -> Dict[str, Any]:
        """Extract context from enhanced phase for use in next phase."""
        return {
            "previous_phase": enhanced_phase["phase_name"],
            "integration_phase": enhanced_phase["integration_phase"],
            "coherence": enhanced_phase["integration_metrics"].get("coherence", 0.0),
            "context_engineering_insights": enhanced_phase["context_engineering"],
            "enhanced_data_summary": str(enhanced_phase["enhanced_data"])[:500] + "..."
        }
    
    def _synthesize_across_phases(
        self,
        enhanced_phases: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesize insights across all enhanced phases."""
        synthesis = {
            "cross_phase_patterns": [],
            "coherence_progression": [],
            "emergent_insights": [],
            "integration_quality": 0.0
        }
        
        # Track coherence progression
        for phase_name, phase_data in enhanced_phases.items():
            coherence = phase_data["integration_metrics"].get("coherence", 0.0)
            synthesis["coherence_progression"].append({
                "phase": phase_name,
                "coherence": coherence
            })
        
        # Identify cross-phase patterns
        all_insights = []
        for phase_data in enhanced_phases.values():
            context_eng = phase_data.get("context_engineering", {})
            all_insights.extend(str(context_eng).split())
        
        # Simple pattern detection
        word_freq = {}
        for word in all_insights:
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        cross_patterns = [word for word, freq in word_freq.items() if freq > 2]
        synthesis["cross_phase_patterns"] = cross_patterns[:10]
        
        # Calculate integration quality
        coherences = [p["coherence"] for p in synthesis["coherence_progression"]]
        synthesis["integration_quality"] = sum(coherences) / len(coherences) if coherences else 0.0
        
        return synthesis
    
    def _orchestrate_neural_fields(
        self,
        enhanced_phases: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Orchestrate neural fields across phases."""
        field_orchestration = {
            "active_fields": list(self.field_states.keys()),
            "field_interactions": {},
            "collective_coherence": 0.0,
            "emergent_field_properties": []
        }
        
        # Calculate field interactions
        fields = list(self.field_states.values())
        for i, field1 in enumerate(fields):
            for j, field2 in enumerate(fields[i+1:], i+1):
                interaction_key = f"{field1.field_id}_{field2.field_id}"
                # Simplified interaction calculation
                interaction_strength = min(field1.stability_measure * field2.stability_measure, 1.0)
                field_orchestration["field_interactions"][interaction_key] = interaction_strength
        
        # Calculate collective coherence
        if fields:
            collective_coherence = sum(f.stability_measure for f in fields) / len(fields)
            field_orchestration["collective_coherence"] = collective_coherence
        
        return field_orchestration
    
    def _identify_emergent_intelligence(
        self,
        orchestration_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identify emergent intelligence from orchestration."""
        emergent = {
            "system_level_patterns": [],
            "intelligence_indicators": [],
            "adaptation_capabilities": [],
            "emergent_score": 0.0
        }
        
        # Analyze cross-phase synthesis
        cross_synthesis = orchestration_results.get("cross_phase_synthesis", {})
        integration_quality = cross_synthesis.get("integration_quality", 0.0)
        
        if integration_quality > 0.8:
            emergent["intelligence_indicators"].append("High cross-phase integration")
        
        # Analyze field orchestration
        field_orch = orchestration_results.get("field_orchestration", {})
        collective_coherence = field_orch.get("collective_coherence", 0.0)
        
        if collective_coherence > 0.7:
            emergent["intelligence_indicators"].append("Strong field coherence")
        
        # Calculate emergent score
        emergent["emergent_score"] = (integration_quality + collective_coherence) / 2.0
        
        return emergent
    
    def _calculate_system_coherence(
        self,
        orchestration_results: Dict[str, Any]
    ) -> float:
        """Calculate overall system coherence."""
        coherence_factors = []
        
        # Cross-phase coherence
        cross_synthesis = orchestration_results.get("cross_phase_synthesis", {})
        integration_quality = cross_synthesis.get("integration_quality", 0.0)
        coherence_factors.append(integration_quality)
        
        # Field coherence
        field_orch = orchestration_results.get("field_orchestration", {})
        collective_coherence = field_orch.get("collective_coherence", 0.0)
        coherence_factors.append(collective_coherence)
        
        # Emergent intelligence coherence
        emergent = orchestration_results.get("emergent_intelligence", {})
        emergent_score = emergent.get("emergent_score", 0.0)
        coherence_factors.append(emergent_score)
        
        return sum(coherence_factors) / len(coherence_factors) if coherence_factors else 0.0
    
    def _calculate_prompt_efficiency(self, prompts: Dict[str, str]) -> float:
        """Calculate efficiency of atomic prompts."""
        if not prompts:
            return 0.0
        
        # Simple efficiency heuristic based on prompt length optimization
        efficiencies = []
        for prompt in prompts.values():
            # Optimal prompt length is around 200-400 characters
            length = len(prompt)
            if 200 <= length <= 400:
                efficiency = 1.0
            elif length < 200:
                efficiency = length / 200.0
            else:
                efficiency = max(0.5, 400.0 / length)
            efficiencies.append(efficiency)
        
        return sum(efficiencies) / len(efficiencies)
    
    def _update_integration_metrics(self, enhancement_results: Dict[str, Any]):
        """Update global integration metrics."""
        self.integration_metrics["phases_enhanced"] += 1
        
        coherence = enhancement_results["integration_metrics"].get("coherence", 0.0)
        self.integration_metrics["total_coherence"] += coherence
        
        efficiency = enhancement_results["integration_metrics"].get("efficiency", 0.0)
        if efficiency > 0:
            self.integration_metrics["optimization_efficiency"] = (
                self.integration_metrics["optimization_efficiency"] + efficiency
            ) / 2.0
    
    def get_integration_summary(self) -> Dict[str, Any]:
        """Get comprehensive integration summary."""
        return {
            "integration_manager": "Context Engineering Integration Manager",
            "phases_enhanced": self.integration_metrics["phases_enhanced"],
            "average_coherence": (
                self.integration_metrics["total_coherence"] / 
                max(self.integration_metrics["phases_enhanced"], 1)
            ),
            "optimization_efficiency": self.integration_metrics["optimization_efficiency"],
            "active_fields": len(self.field_states),
            "components_integrated": {
                "atomic_prompting": self.config.enable_atomic_prompting,
                "field_dynamics": self.config.enable_field_dynamics,
                "cognitive_tools": self.config.enable_cognitive_tools,
                "pattern_synthesis": self.config.enable_pattern_synthesis
            },
            "system_status": "fully_integrated" if self.integration_metrics["phases_enhanced"] > 3 else "partial_integration"
        }