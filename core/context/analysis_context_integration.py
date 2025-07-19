"""
Integration layer for Context Field Engine with CursorRules Architect analysis system.

Provides seamless integration of advanced context field dynamics into the
existing analysis pipeline with attractor formation, field resonance, and
emergent pattern detection.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .context_field_engine import (
    ContextFieldEngine, AttractorType, ProtocolState, FieldType
)


class AnalysisContextIntegration:
    """
    Integration layer for Context Field Engine with analysis system.
    
    Enhances analysis with:
    - Dynamic attractor formation for key concepts
    - Field resonance for pattern amplification
    - Emergent pattern detection across analysis phases
    - Symbolic residue tracking for context memory
    - Meta-recursive improvement of analysis quality
    """

    def __init__(self, field_storage_path: str = "analysis_context_field.json"):
        """Initialize with context field engine."""
        self.field_engine = ContextFieldEngine()
        self.storage_path = field_storage_path
        self.current_analysis_session = None
        self.phase_attractors: Dict[str, List[str]] = {}
        self.cross_phase_resonances: List[str] = []
        
        # Initialize analysis-specific field
        self._initialize_analysis_field()

    def start_field_analysis(self, project_context: Dict[str, Any]) -> str:
        """
        Start a new field-enhanced analysis session.
        
        Args:
            project_context: Context about the project being analyzed
            
        Returns:
            Session ID
        """
        session_id = f"field_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_analysis_session = {
            "session_id": session_id,
            "project_context": project_context,
            "start_time": datetime.now(),
            "field_snapshot": self._capture_field_snapshot(),
            "enhancement_protocols": []
        }

        # Create foundational attractors for this analysis
        project_name = project_context.get("name", "project")
        technologies = project_context.get("technologies", [])
        
        # Create project attractor
        project_attractor = self.field_engine.create_attractor(
            f"project_{project_name}",
            AttractorType.CONCEPT,
            (50, 50, 90),  # High in field space for prominence
            strength=0.9
        )
        
        # Create technology attractors
        tech_attractors = []
        for i, tech in enumerate(technologies[:5]):  # Limit to 5 main technologies
            tech_attractor = self.field_engine.create_attractor(
                f"tech_{tech}",
                AttractorType.CONCEPT,
                (20 + i*15, 20 + i*10, 70),
                strength=0.7
            )
            tech_attractors.append(tech_attractor)
        
        # Create resonance between project and technologies
        if tech_attractors:
            tech_resonance = self.field_engine.create_resonance(
                [project_attractor] + tech_attractors,
                frequency=1.2,
                amplitude=0.8,
                resonance_type="project_tech_alignment"
            )
            self.cross_phase_resonances.append(tech_resonance)

        return session_id

    def enhance_phase_with_field(self, phase_name: str, phase_data: Dict[str, Any],
                                phase_number: int) -> Dict[str, Any]:
        """
        Enhance analysis phase with field dynamics.
        
        Args:
            phase_name: Name of the analysis phase
            phase_data: Data from the phase
            phase_number: Phase number (1-6)
            
        Returns:
            Enhanced phase data with field insights
        """
        if not self.current_analysis_session:
            raise ValueError("No active field analysis session")

        # Create phase-specific attractors
        phase_attractors = self._create_phase_attractors(phase_name, phase_data, phase_number)
        self.phase_attractors[phase_name] = phase_attractors

        # Execute relevant protocols for this phase
        protocols_executed = self._execute_phase_protocols(phase_name, phase_data, phase_number)

        # Detect emergent patterns specific to this phase
        emergent_patterns = self.field_engine.detect_emergence()
        phase_patterns = [p for p in emergent_patterns if self._is_phase_relevant(p, phase_name)]

        # Generate field insights
        field_insights = self._generate_field_insights(phase_name, phase_patterns)

        # Create symbolic residues for important findings
        residues_created = self._create_phase_residues(phase_name, phase_data)

        # Enhanced phase data with field dynamics
        enhanced_data = {
            **phase_data,
            "field_enhancement": {
                "attractors_created": phase_attractors,
                "protocols_executed": protocols_executed,
                "emergent_patterns": [
                    {
                        "pattern_id": p.id,
                        "pattern_type": p.pattern_type,
                        "emergence_strength": p.emergence_strength,
                        "elements": p.elements
                    }
                    for p in phase_patterns
                ],
                "field_insights": field_insights,
                "symbolic_residues": residues_created,
                "field_coherence": self.field_engine.get_field_coherence(),
                "field_energy": self.field_engine.get_field_energy()
            }
        }

        # Evolve field forward
        self.field_engine.evolve_field(time_delta=1.0)

        return enhanced_data

    def get_cross_phase_patterns(self) -> Dict[str, Any]:
        """
        Get patterns that emerge across multiple phases.
        
        Returns:
            Cross-phase pattern analysis
        """
        # Detect patterns that span multiple phases
        all_patterns = self.field_engine.emergent_patterns
        cross_phase_patterns = []

        for pattern in all_patterns.values():
            # Check if pattern involves attractors from multiple phases
            involved_phases = set()
            for element_id in pattern.elements:
                for phase_name, phase_attractors in self.phase_attractors.items():
                    if element_id in phase_attractors:
                        involved_phases.add(phase_name)
            
            if len(involved_phases) > 1:
                cross_phase_patterns.append({
                    "pattern_id": pattern.id,
                    "pattern_type": pattern.pattern_type,
                    "involved_phases": list(involved_phases),
                    "emergence_strength": pattern.emergence_strength,
                    "stability": pattern.stability
                })

        # Analyze field resonance across phases
        resonance_analysis = self._analyze_cross_phase_resonance()

        # Generate meta-insights
        meta_insights = self._generate_meta_insights(cross_phase_patterns, resonance_analysis)

        return {
            "cross_phase_patterns": cross_phase_patterns,
            "resonance_analysis": resonance_analysis,
            "meta_insights": meta_insights,
            "field_evolution": self._analyze_field_evolution()
        }

    def perform_meta_recursive_enhancement(self) -> Dict[str, Any]:
        """
        Perform meta-recursive enhancement of the analysis field.
        
        Returns:
            Enhancement results and recommendations
        """
        # Execute meta-recursive framework protocol
        meta_execution = self.field_engine.execute_protocol(
            "meta_recursive_framework",
            {"analysis_session": self.current_analysis_session}
        )

        # Perform field self-reflection
        reflection = self.field_engine.self_reflect()

        # Generate analysis-specific improvements
        analysis_improvements = self._identify_analysis_improvements(reflection)

        # Apply field improvements
        for improvement in analysis_improvements:
            self.field_engine.apply_improvement(
                improvement["type"],
                improvement["parameters"]
            )

        return {
            "meta_execution_id": meta_execution,
            "self_reflection": reflection,
            "improvements_applied": analysis_improvements,
            "enhanced_field_state": self._capture_field_snapshot(),
            "recommendations": self._generate_enhancement_recommendations(reflection)
        }

    def get_field_interpretability_map(self) -> Dict[str, Any]:
        """
        Get interpretability map of the analysis field.
        
        Returns:
            Comprehensive interpretability map
        """
        base_map = self.field_engine.get_interpretability_map()
        
        # Add analysis-specific interpretability layers
        analysis_map = {
            **base_map,
            "analysis_context": {
                "session_info": {
                    "session_id": self.current_analysis_session["session_id"] if self.current_analysis_session else None,
                    "phases_processed": len(self.phase_attractors),
                    "cross_phase_resonances": len(self.cross_phase_resonances)
                },
                "phase_attribution": self._map_phase_attributions(),
                "concept_evolution": self._trace_concept_evolution(),
                "insight_formation": self._trace_insight_formation()
            },
            "analysis_recommendations": self._generate_interpretability_recommendations()
        }

        return analysis_map

    def export_field_state(self) -> Dict[str, Any]:
        """
        Export current field state for persistence or sharing.
        
        Returns:
            Serializable field state
        """
        return {
            "field_dimensions": self.field_engine.field_dimensions,
            "attractors": {
                aid: {
                    "concept": attr.concept,
                    "type": attr.attractor_type.value,
                    "position": attr.position,
                    "strength": attr.strength,
                    "activation_count": attr.activation_count
                }
                for aid, attr in self.field_engine.attractors.items()
            },
            "resonances": {
                rid: {
                    "source_ids": res.source_ids,
                    "frequency": res.frequency,
                    "amplitude": res.amplitude,
                    "coherence_score": res.coherence_score,
                    "resonance_type": res.resonance_type
                }
                for rid, res in self.field_engine.resonance_patterns.items()
            },
            "emergent_patterns": {
                pid: {
                    "pattern_type": pattern.pattern_type,
                    "elements": pattern.elements,
                    "emergence_strength": pattern.emergence_strength,
                    "stability": pattern.stability,
                    "lifecycle_stage": pattern.lifecycle_stage
                }
                for pid, pattern in self.field_engine.emergent_patterns.items()
            },
            "session_info": self.current_analysis_session,
            "phase_attractors": self.phase_attractors
        }

    def end_field_analysis(self) -> Dict[str, Any]:
        """
        End the current field analysis session.
        
        Returns:
            Session summary with field insights
        """
        if not self.current_analysis_session:
            return {"status": "no_active_session"}

        # Perform final field analysis
        final_patterns = self.get_cross_phase_patterns()
        final_coherence = self.field_engine.get_field_coherence()
        final_energy = self.field_engine.get_field_energy()

        # Generate summary insights
        summary_insights = self._generate_session_summary()

        session_summary = {
            "session_id": self.current_analysis_session["session_id"],
            "duration": (datetime.now() - self.current_analysis_session["start_time"]).total_seconds(),
            "phases_enhanced": len(self.phase_attractors),
            "total_attractors_created": sum(len(attrs) for attrs in self.phase_attractors.values()),
            "emergent_patterns_detected": len(self.field_engine.emergent_patterns),
            "final_field_coherence": final_coherence,
            "final_field_energy": final_energy,
            "cross_phase_patterns": final_patterns,
            "summary_insights": summary_insights,
            "field_evolution_metrics": self._calculate_field_evolution_metrics()
        }

        # Reset session
        self.current_analysis_session = None
        self.phase_attractors = {}
        self.cross_phase_resonances = []

        return session_summary

    # Private helper methods

    def _initialize_analysis_field(self):
        """Initialize field with analysis-specific attractors."""
        # Core analysis concepts
        analysis_concepts = [
            ("discovery", AttractorType.CONCEPT, (20, 20, 20)),
            ("understanding", AttractorType.CONCEPT, (40, 20, 20)),
            ("synthesis", AttractorType.CONCEPT, (60, 20, 20)),
            ("insight", AttractorType.INSIGHT, (80, 20, 20)),
            ("quality", AttractorType.PATTERN, (20, 80, 20)),
            ("structure", AttractorType.PATTERN, (40, 80, 20)),
            ("relationships", AttractorType.RELATIONSHIP, (60, 80, 20)),
            ("evolution", AttractorType.PATTERN, (80, 80, 20))
        ]

        for concept, attr_type, position in analysis_concepts:
            self.field_engine.create_attractor(concept, attr_type, position, strength=0.6)

    def _capture_field_snapshot(self) -> Dict[str, Any]:
        """Capture current field state snapshot."""
        return {
            "timestamp": datetime.now().isoformat(),
            "attractor_count": len(self.field_engine.attractors),
            "resonance_count": len(self.field_engine.resonance_patterns),
            "pattern_count": len(self.field_engine.emergent_patterns),
            "field_coherence": self.field_engine.get_field_coherence(),
            "field_energy": self.field_engine.get_field_energy()
        }

    def _create_phase_attractors(self, phase_name: str, phase_data: Dict[str, Any], 
                               phase_number: int) -> List[str]:
        """Create attractors specific to an analysis phase."""
        created_attractors = []

        # Base position for this phase
        base_x = 10 + phase_number * 15
        base_y = 40
        base_z = 30 + phase_number * 10

        # Extract key concepts from phase data
        concepts = self._extract_phase_concepts(phase_data)
        
        for i, concept in enumerate(concepts[:5]):  # Limit to 5 per phase
            position = (base_x + i*5, base_y + i*3, base_z)
            
            # Determine attractor type based on concept nature
            if "pattern" in concept.lower() or "structure" in concept.lower():
                attr_type = AttractorType.PATTERN
            elif "insight" in concept.lower() or "finding" in concept.lower():
                attr_type = AttractorType.INSIGHT
            elif "relation" in concept.lower() or "connection" in concept.lower():
                attr_type = AttractorType.RELATIONSHIP
            else:
                attr_type = AttractorType.CONCEPT

            attractor_id = self.field_engine.create_attractor(
                f"{phase_name}_{concept}",
                attr_type,
                position,
                strength=0.6 + phase_number * 0.05  # Stronger for later phases
            )
            created_attractors.append(attractor_id)

        return created_attractors

    def _extract_phase_concepts(self, phase_data: Dict[str, Any]) -> List[str]:
        """Extract key concepts from phase data."""
        concepts = []
        
        # Extract from different data fields
        for key, value in phase_data.items():
            if isinstance(value, list):
                concepts.extend([str(item)[:20] for item in value[:3]])  # First 3 items, truncated
            elif isinstance(value, str) and len(value) < 50:
                concepts.append(value)
            elif key in ["technologies", "frameworks", "patterns", "issues", "recommendations"]:
                if isinstance(value, (list, tuple)):
                    concepts.extend([str(item)[:15] for item in value])

        # Clean and deduplicate concepts
        cleaned_concepts = []
        for concept in concepts:
            clean_concept = concept.replace(" ", "_").replace("-", "_").lower()
            if clean_concept not in cleaned_concepts and len(clean_concept) > 2:
                cleaned_concepts.append(clean_concept)

        return cleaned_concepts[:8]  # Return top 8 concepts

    def _execute_phase_protocols(self, phase_name: str, phase_data: Dict[str, Any], 
                                phase_number: int) -> List[str]:
        """Execute relevant protocols for a phase."""
        executed_protocols = []

        # Phase 1: Discovery - use attractor co-emergence
        if phase_number == 1:
            protocol_id = self.field_engine.execute_protocol(
                "attractor_co_emerge",
                {"concepts": self._extract_phase_concepts(phase_data)[:3]}
            )
            executed_protocols.append(protocol_id)

        # Phase 2: Planning - use field resonance scaffold
        elif phase_number == 2:
            protocol_id = self.field_engine.execute_protocol(
                "field_resonance_scaffold",
                {"phase": phase_name, "data": phase_data}
            )
            executed_protocols.append(protocol_id)

        # Phase 3: Deep Analysis - use recursive emergence
        elif phase_number == 3:
            protocol_id = self.field_engine.execute_protocol(
                "recursive_emergence",
                {"concept": "deep_analysis", "phase_data": phase_data}
            )
            executed_protocols.append(protocol_id)

        # Phase 4: Synthesis - use symbolic mechanism
        elif phase_number == 4:
            protocol_id = self.field_engine.execute_protocol(
                "symbolic_mechanism",
                {"symbols": ["⊕", "⊗", "⊙"], "meanings": ["combine", "transform", "synthesize"]}
            )
            executed_protocols.append(protocol_id)

        # Phase 5-6: Final phases - use meta-recursive framework
        elif phase_number >= 5:
            protocol_id = self.field_engine.execute_protocol(
                "meta_recursive_framework",
                {"phase": phase_name, "analysis_depth": "comprehensive"}
            )
            executed_protocols.append(protocol_id)

        return executed_protocols

    def _is_phase_relevant(self, pattern: Any, phase_name: str) -> bool:
        """Check if an emergent pattern is relevant to a specific phase."""
        # Check if pattern elements include phase attractors
        phase_attractors = self.phase_attractors.get(phase_name, [])
        
        pattern_elements = set(pattern.elements)
        phase_elements = set(phase_attractors)
        
        # Pattern is relevant if it shares elements with phase attractors
        return bool(pattern_elements & phase_elements)

    def _generate_field_insights(self, phase_name: str, patterns: List[Any]) -> List[str]:
        """Generate insights from field patterns for a phase."""
        insights = []

        # Insight from pattern emergence
        if patterns:
            pattern_types = [p.pattern_type for p in patterns]
            most_common_type = max(set(pattern_types), key=pattern_types.count)
            insights.append(f"Phase {phase_name} shows strong {most_common_type} emergence")

        # Insight from field coherence
        coherence = self.field_engine.get_field_coherence()
        if coherence > 0.8:
            insights.append(f"High field coherence ({coherence:.2f}) indicates strong conceptual alignment")
        elif coherence < 0.4:
            insights.append(f"Low field coherence ({coherence:.2f}) suggests need for better integration")

        # Insight from attractor strength distribution
        phase_attractors = self.phase_attractors.get(phase_name, [])
        if phase_attractors:
            strengths = [self.field_engine.attractors[aid].strength for aid in phase_attractors]
            avg_strength = sum(strengths) / len(strengths)
            if avg_strength > 0.7:
                insights.append(f"Strong concept formation in {phase_name} (avg strength: {avg_strength:.2f})")

        return insights

    def _create_phase_residues(self, phase_name: str, phase_data: Dict[str, Any]) -> List[str]:
        """Create symbolic residues for phase findings."""
        residues_created = []

        # Create residues for important findings
        if "key_findings" in phase_data:
            findings = phase_data["key_findings"]
            for i, finding in enumerate(findings[:3]):  # Top 3 findings
                residue_id = self.field_engine.add_symbolic_residue(
                    symbol=f"F{i+1}",
                    meaning=str(finding)[:50],  # Truncate long findings
                    context=f"{phase_name}_finding",
                    position=(70 + i*5, 60, 40),
                    decay_rate=0.005  # Slow decay for important findings
                )
                residues_created.append(residue_id)

        # Create residues for technologies
        if "technologies" in phase_data:
            for i, tech in enumerate(phase_data["technologies"][:2]):
                residue_id = self.field_engine.add_symbolic_residue(
                    symbol=f"T{tech[0].upper()}",
                    meaning=f"technology_{tech}",
                    context=f"{phase_name}_technology",
                    position=(30 + i*10, 70, 50),
                    decay_rate=0.01
                )
                residues_created.append(residue_id)

        return residues_created

    def _analyze_cross_phase_resonance(self) -> Dict[str, Any]:
        """Analyze resonance patterns across phases."""
        # Get all resonances
        all_resonances = self.field_engine.resonance_patterns

        cross_phase_resonances = []
        for resonance in all_resonances.values():
            # Check if resonance involves attractors from multiple phases
            involved_phases = set()
            for source_id in resonance.source_ids:
                for phase_name, phase_attractors in self.phase_attractors.items():
                    if source_id in phase_attractors:
                        involved_phases.add(phase_name)
            
            if len(involved_phases) > 1:
                cross_phase_resonances.append({
                    "resonance_id": resonance.id,
                    "involved_phases": list(involved_phases),
                    "frequency": resonance.frequency,
                    "amplitude": resonance.amplitude,
                    "coherence": resonance.coherence_score
                })

        return {
            "cross_phase_resonances": cross_phase_resonances,
            "total_resonance_strength": sum(r["amplitude"] for r in cross_phase_resonances),
            "average_coherence": sum(r["coherence"] for r in cross_phase_resonances) / len(cross_phase_resonances) if cross_phase_resonances else 0
        }

    def _generate_meta_insights(self, cross_phase_patterns: List[Dict], 
                               resonance_analysis: Dict[str, Any]) -> List[str]:
        """Generate meta-level insights from cross-phase analysis."""
        insights = []

        # Insights from cross-phase patterns
        if len(cross_phase_patterns) > 3:
            insights.append("Strong cross-phase pattern emergence indicates deep structural coherence")
        elif len(cross_phase_patterns) == 0:
            insights.append("Lack of cross-phase patterns suggests isolated phase analysis")

        # Insights from resonance analysis
        avg_coherence = resonance_analysis.get("average_coherence", 0)
        if avg_coherence > 0.8:
            insights.append("High cross-phase resonance coherence indicates excellent analysis flow")
        elif avg_coherence < 0.4:
            insights.append("Low cross-phase coherence suggests need for better phase integration")

        # Insights from field evolution
        field_energy = self.field_engine.get_field_energy()
        if field_energy > 10:
            insights.append("High field energy indicates rich conceptual development")
        elif field_energy < 3:
            insights.append("Low field energy suggests need for deeper concept exploration")

        return insights

    def _analyze_field_evolution(self) -> Dict[str, Any]:
        """Analyze how the field has evolved during analysis."""
        if not self.current_analysis_session:
            return {}

        initial_snapshot = self.current_analysis_session.get("field_snapshot", {})
        current_snapshot = self._capture_field_snapshot()

        evolution_metrics = {}
        for key in ["attractor_count", "resonance_count", "pattern_count", "field_coherence", "field_energy"]:
            initial_value = initial_snapshot.get(key, 0)
            current_value = current_snapshot.get(key, 0)
            if initial_value > 0:
                evolution_metrics[f"{key}_growth"] = (current_value - initial_value) / initial_value
            else:
                evolution_metrics[f"{key}_growth"] = float('inf') if current_value > 0 else 0

        return {
            "initial_state": initial_snapshot,
            "current_state": current_snapshot,
            "evolution_metrics": evolution_metrics,
            "growth_trajectory": self._classify_growth_trajectory(evolution_metrics)
        }

    def _classify_growth_trajectory(self, evolution_metrics: Dict[str, float]) -> str:
        """Classify the overall growth trajectory of the field."""
        avg_growth = sum(evolution_metrics.values()) / len(evolution_metrics) if evolution_metrics else 0
        
        if avg_growth > 1.0:
            return "explosive_growth"
        elif avg_growth > 0.5:
            return "strong_growth"
        elif avg_growth > 0.1:
            return "steady_growth"
        elif avg_growth > 0:
            return "slow_growth"
        else:
            return "stagnant_or_declining"

    def _identify_analysis_improvements(self, reflection: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify analysis-specific improvements from field reflection."""
        improvements = []
        
        field_metrics = reflection.get("field_metrics", {})
        improvement_opportunities = reflection.get("improvement_opportunities", [])

        # Analysis-specific improvements
        if field_metrics.get("field_coherence", 0) < 0.6:
            improvements.append({
                "type": "enhance_resonance",
                "parameters": {"frequency_adjustment": 1.15},
                "rationale": "Low field coherence needs resonance enhancement"
            })

        if "strengthen_weak_attractors" in improvement_opportunities:
            improvements.append({
                "type": "strengthen_weak_attractors",
                "parameters": {"threshold": 0.4},
                "rationale": "Weak concept attractors need strengthening for better analysis"
            })

        # Analysis phase-specific improvements
        if len(self.phase_attractors) > 3 and field_metrics.get("emergent_patterns", 0) < 2:
            improvements.append({
                "type": "consolidate_patterns",
                "parameters": {"similarity_threshold": 0.7},
                "rationale": "Multiple phases processed but few emergent patterns"
            })

        return improvements

    def _generate_enhancement_recommendations(self, reflection: Dict[str, Any]) -> List[str]:
        """Generate recommendations for enhancing analysis quality."""
        recommendations = []
        
        field_metrics = reflection.get("field_metrics", {})
        
        # Coherence recommendations
        coherence = field_metrics.get("field_coherence", 0)
        if coherence < 0.5:
            recommendations.append("Consider reviewing phase connections for better conceptual flow")
        elif coherence > 0.9:
            recommendations.append("Excellent conceptual coherence - maintain current analysis approach")

        # Energy recommendations
        energy = field_metrics.get("field_energy", 0)
        if energy < 5:
            recommendations.append("Explore concepts more deeply to increase analytical richness")
        elif energy > 15:
            recommendations.append("Consider focusing analysis to avoid conceptual overload")

        # Pattern recommendations
        pattern_count = field_metrics.get("emergent_patterns", 0)
        if pattern_count == 0:
            recommendations.append("Look for emerging patterns and connections between concepts")
        elif pattern_count > 10:
            recommendations.append("Consolidate similar patterns for clearer insights")

        return recommendations

    def _map_phase_attributions(self) -> Dict[str, List[str]]:
        """Map which phases contributed to which attractors and patterns."""
        attributions = {}
        
        for phase_name, phase_attractors in self.phase_attractors.items():
            attributions[phase_name] = {
                "attractors": phase_attractors,
                "influenced_patterns": []
            }
            
            # Find patterns influenced by this phase
            for pattern in self.field_engine.emergent_patterns.values():
                if any(attr_id in pattern.elements for attr_id in phase_attractors):
                    attributions[phase_name]["influenced_patterns"].append(pattern.id)

        return attributions

    def _trace_concept_evolution(self) -> Dict[str, Any]:
        """Trace how concepts evolved through the analysis."""
        concept_evolution = {}
        
        # Track attractor activation patterns
        for attractor in self.field_engine.attractors.values():
            concept_name = attractor.concept
            if concept_name not in concept_evolution:
                concept_evolution[concept_name] = {
                    "initial_strength": attractor.strength,
                    "activation_count": attractor.activation_count,
                    "evolution_stage": "stable" if attractor.activation_count > 3 else "emerging"
                }

        return concept_evolution

    def _trace_insight_formation(self) -> List[Dict[str, Any]]:
        """Trace how insights formed through field interactions."""
        insight_traces = []
        
        # Find insight-type attractors and their formation context
        for attractor in self.field_engine.attractors.values():
            if attractor.attractor_type == AttractorType.INSIGHT:
                insight_traces.append({
                    "insight_concept": attractor.concept,
                    "formation_time": attractor.created.isoformat(),
                    "strength": attractor.strength,
                    "resonance_connections": len(attractor.resonance_connections),
                    "context": "field_emergence"
                })

        return insight_traces

    def _generate_interpretability_recommendations(self) -> List[str]:
        """Generate recommendations for better interpretability."""
        recommendations = []
        
        # Check field complexity
        total_elements = (len(self.field_engine.attractors) + 
                         len(self.field_engine.resonance_patterns) + 
                         len(self.field_engine.emergent_patterns))
        
        if total_elements > 50:
            recommendations.append("Consider field simplification for better interpretability")
        
        # Check pattern clarity
        unclear_patterns = [p for p in self.field_engine.emergent_patterns.values() 
                           if p.stability < 0.3]
        if len(unclear_patterns) > 3:
            recommendations.append("Stabilize unclear patterns for better understanding")

        # Check symbolic residue clarity
        active_residues = [r for r in self.field_engine.symbolic_residues.values() 
                          if r.strength > 0.1]
        if len(active_residues) > 20:
            recommendations.append("Consolidate symbolic residues for clarity")

        return recommendations

    def _generate_session_summary(self) -> List[str]:
        """Generate high-level summary insights for the session."""
        insights = []
        
        # Overall session insights
        total_attractors = sum(len(attrs) for attrs in self.phase_attractors.values())
        insights.append(f"Created {total_attractors} concept attractors across {len(self.phase_attractors)} phases")
        
        # Pattern emergence insights
        pattern_count = len(self.field_engine.emergent_patterns)
        if pattern_count > 5:
            insights.append(f"Strong pattern emergence with {pattern_count} distinct patterns identified")
        
        # Coherence insights
        final_coherence = self.field_engine.get_field_coherence()
        if final_coherence > 0.8:
            insights.append("Achieved high conceptual coherence throughout analysis")
        
        # Energy insights
        final_energy = self.field_engine.get_field_energy()
        if final_energy > 12:
            insights.append("Rich conceptual development with high field energy")

        return insights

    def _calculate_field_evolution_metrics(self) -> Dict[str, float]:
        """Calculate metrics for field evolution during the session."""
        if not self.current_analysis_session:
            return {}

        initial_snapshot = self.current_analysis_session.get("field_snapshot", {})
        current_snapshot = self._capture_field_snapshot()

        metrics = {}
        
        # Calculate growth rates
        for metric in ["attractor_count", "resonance_count", "pattern_count"]:
            initial = initial_snapshot.get(metric, 0)
            current = current_snapshot.get(metric, 0)
            metrics[f"{metric}_growth_rate"] = (current - initial) / (initial + 1)  # Avoid division by zero

        # Calculate quality improvements
        initial_coherence = initial_snapshot.get("field_coherence", 0)
        current_coherence = current_snapshot.get("field_coherence", 0)
        metrics["coherence_improvement"] = current_coherence - initial_coherence

        # Calculate complexity growth
        initial_complexity = (initial_snapshot.get("attractor_count", 0) + 
                             initial_snapshot.get("resonance_count", 0))
        current_complexity = (current_snapshot.get("attractor_count", 0) + 
                             current_snapshot.get("resonance_count", 0))
        metrics["complexity_growth"] = (current_complexity - initial_complexity) / (initial_complexity + 1)

        return metrics