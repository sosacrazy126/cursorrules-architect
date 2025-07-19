"""
core/analysis/enhanced_phase_1.py

Enhanced Phase 1 analysis with context engineering integration.
Incorporates atomic prompting patterns for optimized initial discovery.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from ..analysis.phase_1 import Phase1Analysis
from ..context_engineering.foundations import ContextFoundations, AtomicPrompt
from ..context_engineering.field_dynamics import FieldDynamics, FieldType
from ..context_engineering.cognitive_tools import CognitiveToolkit

logger = logging.getLogger(__name__)

class ContextAwarePhase1Analysis(Phase1Analysis):
    """
    Enhanced Phase 1 analysis with context engineering capabilities.
    Integrates atomic prompting patterns and field dynamics for superior initial discovery.
    """
    
    def __init__(self):
        """Initialize enhanced Phase 1 with context engineering components."""
        super().__init__()
        
        # Initialize context engineering components
        self.context_foundations = ContextFoundations()
        self.field_dynamics = FieldDynamics()
        self.cognitive_toolkit = CognitiveToolkit()
        
        # Track enhancement metrics
        self.enhancement_metrics = {
            "atomic_prompt_efficiency": 0.0,
            "field_coherence": 0.0,
            "cognitive_depth": 0.0
        }
        
        logger.info("Initialized enhanced Phase 1 with context engineering capabilities")
    
    async def run(self, tree: List[str], package_info: Dict) -> Dict[str, Any]:
        """
        Enhanced Phase 1 execution with atomic prompting and field dynamics.
        
        Args:
            tree: Project file tree structure
            package_info: Package dependency information
            
        Returns:
            Enhanced analysis results with context engineering insights
        """
        logger.info("Starting enhanced Phase 1 analysis with context engineering")
        
        # Phase 1.1: Initialize neural field for discovery
        discovery_context = self._create_discovery_context(tree, package_info)
        discovery_field = self.field_dynamics.initialize_field(
            field_id="phase1_discovery",
            field_type=FieldType.DISCOVERY,
            context=discovery_context
        )
        
        # Phase 1.2: Create atomic prompts for each analysis type
        atomic_prompts = self._create_atomic_prompts(discovery_context)
        
        # Phase 1.3: Apply cognitive understanding to context
        cognitive_insights = self.cognitive_toolkit.apply_cognitive_operations(discovery_context)
        
        # Phase 1.4: Run enhanced standard analysis
        enhanced_results = await self._run_enhanced_standard_analysis(
            tree, package_info, atomic_prompts, cognitive_insights
        )
        
        # Phase 1.5: Process results through neural field
        field_processed_results = self.field_dynamics.process_through_field(
            field_id="phase1_discovery",
            input_data=enhanced_results
        )
        
        # Phase 1.6: Synthesize all insights
        synthesized_results = self._synthesize_enhanced_results(
            enhanced_results,
            field_processed_results,
            cognitive_insights,
            atomic_prompts
        )
        
        # Update enhancement metrics
        self._update_enhancement_metrics(synthesized_results)
        
        logger.info(f"Enhanced Phase 1 completed with coherence: {self.enhancement_metrics['field_coherence']:.2f}")
        
        return synthesized_results
    
    def _create_discovery_context(self, tree: List[str], package_info: Dict) -> Dict[str, Any]:
        """Create optimized discovery context for atomic prompting."""
        return {
            "codebase_tree": tree,
            "dependencies": package_info,
            "analysis_scope": "initial_discovery",
            "optimization_target": "comprehensive_understanding",
            "context_metadata": {
                "file_count": len(tree),
                "dependency_count": len(package_info.get("dependencies", {})),
                "complexity_estimate": self._estimate_complexity(tree, package_info)
            }
        }
    
    def _create_atomic_prompts(self, discovery_context: Dict[str, Any]) -> Dict[str, str]:
        """Create atomic prompts for each analysis component."""
        atomic_prompts = {}
        
        # Structure analysis atomic prompt
        atomic_prompts["structure"] = self.context_foundations.create_atomic_prompt(
            template_name="discovery",
            context=f"Project structure: {discovery_context['codebase_tree'][:10]}...",
            custom_constraints=[
                "Focus on directory organization patterns",
                "Identify modular structure indicators",
                "Limit to top-level architectural insights"
            ]
        )
        
        # Dependency analysis atomic prompt
        atomic_prompts["dependencies"] = self.context_foundations.create_atomic_prompt(
            template_name="analysis",
            context=f"Dependencies: {discovery_context['dependencies']}",
            custom_constraints=[
                "Map critical dependency relationships",
                "Identify potential version conflicts",
                "Assess dependency complexity level"
            ]
        )
        
        # Technology stack atomic prompt
        atomic_prompts["tech_stack"] = self.context_foundations.create_atomic_prompt(
            template_name="discovery",
            context=f"Technology indicators from files and dependencies",
            custom_constraints=[
                "Categorize technology stack components",
                "Identify primary frameworks and libraries",
                "Assess technology maturity and compatibility"
            ]
        )
        
        return atomic_prompts
    
    async def _run_enhanced_standard_analysis(
        self,
        tree: List[str],
        package_info: Dict,
        atomic_prompts: Dict[str, str],
        cognitive_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run standard analysis enhanced with atomic prompts and cognitive insights."""
        
        # Create enhanced context for each architect
        enhanced_context = {
            "original_tree": tree,
            "original_package_info": package_info,
            "atomic_prompts": atomic_prompts,
            "cognitive_context": cognitive_insights.get("understanding", {}),
            "reasoning_insights": cognitive_insights.get("reasoning", {}),
            "field_guidance": "Focus on pattern emergence and attractor identification"
        }
        
        # Run parallel analysis with enhanced context
        tasks = []
        for architect in self.architects:
            # Enhance architect prompt with atomic structure
            architect_type = architect.instructions.get("role", "unknown")
            if architect_type in atomic_prompts:
                enhanced_prompt = atomic_prompts[architect_type]
                
                # Create enhanced architect context
                architect_context = {
                    **enhanced_context,
                    "atomic_prompt": enhanced_prompt,
                    "cognitive_guidance": cognitive_insights.get("meta_analysis", {}),
                    "optimization_mode": "atomic_efficiency"
                }
                
                task = architect.analyze(architect_context)
                tasks.append(task)
        
        # Execute enhanced analysis
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results with error handling
        processed_results = {}
        for i, result in enumerate(results):
            architect_role = self.architects[i].instructions.get("role", f"architect_{i}")
            
            if isinstance(result, Exception):
                logger.error(f"Enhanced analysis failed for {architect_role}: {result}")
                processed_results[architect_role] = {"error": str(result), "status": "failed"}
            else:
                processed_results[architect_role] = result
                
                # Measure atomic prompt efficiency
                if "atomic_prompt" in enhanced_context:
                    efficiency = self.context_foundations.measure_token_efficiency(
                        atomic_prompts.get(architect_role, ""),
                        str(result)
                    )
                    processed_results[architect_role]["atomic_efficiency"] = efficiency
        
        return processed_results
    
    def _synthesize_enhanced_results(
        self,
        enhanced_results: Dict[str, Any],
        field_results: Dict[str, Any],
        cognitive_insights: Dict[str, Any],
        atomic_prompts: Dict[str, str]
    ) -> Dict[str, Any]:
        """Synthesize all enhancement results into comprehensive analysis."""
        
        synthesized_results = {
            # Core analysis results
            "standard_analysis": enhanced_results,
            
            # Context engineering enhancements
            "context_engineering": {
                "atomic_prompting": {
                    "prompts_used": atomic_prompts,
                    "efficiency_metrics": self._calculate_atomic_efficiency(enhanced_results),
                    "optimization_recommendations": self.context_foundations.get_optimization_recommendations()
                },
                "field_dynamics": {
                    "field_state": field_results.get("field_state"),
                    "activated_attractors": field_results.get("activated_attractors", []),
                    "emergent_properties": field_results.get("emergent_properties", []),
                    "field_coherence": self._calculate_field_coherence(field_results)
                },
                "cognitive_processing": {
                    "understanding_insights": cognitive_insights.get("understanding", {}),
                    "reasoning_patterns": cognitive_insights.get("reasoning", {}),
                    "cognitive_quality": cognitive_insights.get("meta_analysis", {}),
                    "synthesis_recommendations": cognitive_insights.get("composition", {}).get("final_recommendations", [])
                }
            },
            
            # Integrated insights
            "integrated_insights": self._generate_integrated_insights(
                enhanced_results, field_results, cognitive_insights
            ),
            
            # Enhancement metrics
            "enhancement_metrics": self.enhancement_metrics,
            
            # Phase progression context
            "phase_context": {
                "atomic_context_prepared": True,
                "field_initialized": True,
                "cognitive_foundation_established": True,
                "next_phase_guidance": self._generate_next_phase_guidance(enhanced_results, field_results)
            }
        }
        
        return synthesized_results
    
    def _estimate_complexity(self, tree: List[str], package_info: Dict) -> str:
        """Estimate project complexity for optimization."""
        file_count = len(tree)
        dependency_count = len(package_info.get("dependencies", {}))
        
        complexity_score = (file_count / 100) + (dependency_count / 20)
        
        if complexity_score < 1.0:
            return "low"
        elif complexity_score < 3.0:
            return "medium"
        else:
            return "high"
    
    def _calculate_atomic_efficiency(self, enhanced_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate atomic prompting efficiency metrics."""
        efficiency_metrics = {}
        
        for architect_role, result in enhanced_results.items():
            if isinstance(result, dict) and "atomic_efficiency" in result:
                efficiency_metrics[architect_role] = result["atomic_efficiency"]
        
        if efficiency_metrics:
            efficiency_metrics["average"] = sum(efficiency_metrics.values()) / len(efficiency_metrics)
        
        return efficiency_metrics
    
    def _calculate_field_coherence(self, field_results: Dict[str, Any]) -> float:
        """Calculate field coherence score."""
        field_state = field_results.get("field_state")
        if not field_state:
            return 0.0
        
        # Use field stability as coherence measure
        coherence = getattr(field_state, 'stability_measure', 0.0)
        
        # Boost coherence based on activated attractors
        activated_attractors = field_results.get("activated_attractors", [])
        if activated_attractors:
            attractor_bonus = min(len(activated_attractors) / 5.0, 0.2)
            coherence += attractor_bonus
        
        return min(coherence, 1.0)
    
    def _generate_integrated_insights(
        self,
        enhanced_results: Dict[str, Any],
        field_results: Dict[str, Any],
        cognitive_insights: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate integrated insights from all enhancement sources."""
        integrated_insights = []
        
        # Insight 1: Structural patterns from field dynamics
        emergent_properties = field_results.get("emergent_properties", [])
        if emergent_properties:
            integrated_insights.append({
                "type": "structural_emergence",
                "source": "field_dynamics",
                "insight": "Emergent structural patterns detected",
                "details": emergent_properties,
                "confidence": 0.8
            })
        
        # Insight 2: Cognitive understanding patterns
        understanding_context = cognitive_insights.get("understanding", {}).get("output_data", {}).get("synthesized_context", {})
        if understanding_context:
            integrated_insights.append({
                "type": "cognitive_understanding",
                "source": "cognitive_toolkit",
                "insight": "Deep semantic understanding achieved",
                "details": understanding_context,
                "confidence": cognitive_insights.get("understanding", {}).get("confidence_score", 0.0)
            })
        
        # Insight 3: Cross-analysis pattern convergence
        pattern_convergence = self._identify_pattern_convergence(enhanced_results, field_results, cognitive_insights)
        if pattern_convergence:
            integrated_insights.append({
                "type": "pattern_convergence",
                "source": "multi_source_synthesis",
                "insight": "Consistent patterns identified across analysis methods",
                "details": pattern_convergence,
                "confidence": 0.9
            })
        
        return integrated_insights
    
    def _identify_pattern_convergence(
        self,
        enhanced_results: Dict[str, Any],
        field_results: Dict[str, Any],
        cognitive_insights: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Identify patterns that converge across different analysis methods."""
        convergence_patterns = {}
        
        # Extract patterns from different sources
        field_patterns = [prop.get("patterns", []) for prop in field_results.get("emergent_properties", [])]
        cognitive_patterns = cognitive_insights.get("understanding", {}).get("output_data", {}).get("concepts", [])
        
        # Look for common themes
        common_themes = set()
        
        # Flatten field patterns
        for pattern_list in field_patterns:
            if isinstance(pattern_list, list):
                common_themes.update(pattern_list)
        
        # Extract cognitive pattern themes
        for concept in cognitive_patterns:
            if isinstance(concept, dict):
                instances = concept.get("instances", [])
                if isinstance(instances, list):
                    common_themes.update(instances)
        
        if len(common_themes) > 2:
            convergence_patterns = {
                "converged_themes": list(common_themes),
                "convergence_strength": len(common_themes) / 10.0,
                "analysis_consensus": "High agreement across analysis methods"
            }
        
        return convergence_patterns if convergence_patterns else None
    
    def _generate_next_phase_guidance(
        self,
        enhanced_results: Dict[str, Any],
        field_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate guidance for Phase 2 based on Phase 1 enhancements."""
        guidance = {
            "molecular_context_seeds": [],
            "field_state_transfer": field_results.get("field_state"),
            "optimization_recommendations": [],
            "complexity_adjustments": []
        }
        
        # Extract context seeds for molecular prompting in Phase 2
        activated_attractors = field_results.get("activated_attractors", [])
        for attractor in activated_attractors:
            guidance["molecular_context_seeds"].append({
                "pattern_id": getattr(attractor, 'pattern_id', 'unknown'),
                "activation_level": getattr(attractor, 'activation_level', 0.0),
                "resonance_frequency": getattr(attractor, 'resonance_frequency', 1.0)
            })
        
        # Optimization recommendations based on enhancement metrics
        if self.enhancement_metrics["atomic_prompt_efficiency"] < 0.7:
            guidance["optimization_recommendations"].append("Refine atomic prompts for better efficiency")
        
        if self.enhancement_metrics["field_coherence"] < 0.6:
            guidance["optimization_recommendations"].append("Strengthen field coherence in next phase")
        
        return guidance
    
    def _update_enhancement_metrics(self, synthesized_results: Dict[str, Any]):
        """Update enhancement metrics based on synthesized results."""
        # Update atomic prompt efficiency
        atomic_metrics = synthesized_results.get("context_engineering", {}).get("atomic_prompting", {}).get("efficiency_metrics", {})
        if "average" in atomic_metrics:
            self.enhancement_metrics["atomic_prompt_efficiency"] = atomic_metrics["average"]
        
        # Update field coherence
        field_coherence = synthesized_results.get("context_engineering", {}).get("field_dynamics", {}).get("field_coherence", 0.0)
        self.enhancement_metrics["field_coherence"] = field_coherence
        
        # Update cognitive depth
        cognitive_quality = synthesized_results.get("context_engineering", {}).get("cognitive_processing", {}).get("cognitive_quality", {})
        depth_score = cognitive_quality.get("cognitive_depth", 0.0)
        self.enhancement_metrics["cognitive_depth"] = depth_score
    
    def get_enhancement_summary(self) -> Dict[str, Any]:
        """Get summary of context engineering enhancements applied."""
        return {
            "enhancement_type": "Context Engineering Integration",
            "components_used": [
                "Atomic Prompting (ContextFoundations)",
                "Neural Field Dynamics (FieldDynamics)",
                "Cognitive Toolkit (CognitiveToolkit)"
            ],
            "enhancement_metrics": self.enhancement_metrics,
            "optimization_status": {
                "atomic_efficiency": "excellent" if self.enhancement_metrics["atomic_prompt_efficiency"] > 0.8 else "good" if self.enhancement_metrics["atomic_prompt_efficiency"] > 0.6 else "needs_improvement",
                "field_coherence": "excellent" if self.enhancement_metrics["field_coherence"] > 0.8 else "good" if self.enhancement_metrics["field_coherence"] > 0.6 else "needs_improvement",
                "cognitive_depth": "excellent" if self.enhancement_metrics["cognitive_depth"] > 0.8 else "good" if self.enhancement_metrics["cognitive_depth"] > 0.6 else "needs_improvement"
            }
        }