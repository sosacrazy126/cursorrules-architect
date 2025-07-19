"""
core/context_engineering/foundations.py

Implementation of context engineering foundation patterns.
Maps directly to the atomic prompting methodology for optimized token usage.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class PromptStructure(Enum):
    """Atomic prompt structure types based on context engineering foundations."""
    ATOMIC = "atomic"          # Task + constraints + output format
    MOLECULAR = "molecular"     # Connected prompt chains
    CELLULAR = "cellular"       # Memory-integrated prompts
    ORGANIC = "organic"         # Application-synthesized prompts

@dataclass
class AtomicPrompt:
    """
    Core atomic prompt structure implementing the power law optimization.
    Based on 01_atoms_prompting.md patterns.
    """
    task: str
    constraints: List[str]
    output_format: str
    context: Optional[str] = None
    
    def to_prompt(self) -> str:
        """Generate optimized prompt following atomic structure."""
        prompt_parts = [f"TASK: {self.task}"]
        
        if self.constraints:
            constraints_text = "\n".join([f"- {c}" for c in self.constraints])
            prompt_parts.append(f"CONSTRAINTS:\n{constraints_text}")
            
        if self.context:
            prompt_parts.append(f"CONTEXT:\n{self.context}")
            
        prompt_parts.append(f"OUTPUT FORMAT: {self.output_format}")
        
        return "\n\n".join(prompt_parts)

class ContextFoundations:
    """
    Core foundation class implementing context engineering patterns.
    Provides atomic prompting capabilities for enhanced analysis phases.
    """
    
    def __init__(self):
        """Initialize context foundations with pattern templates."""
        self.atomic_templates = {
            "analysis": AtomicPrompt(
                task="Analyze the provided codebase component",
                constraints=[
                    "Focus on structural patterns and dependencies",
                    "Identify key architectural decisions",
                    "Limit analysis to primary patterns only"
                ],
                output_format="JSON with 'structure', 'dependencies', 'patterns' fields"
            ),
            "synthesis": AtomicPrompt(
                task="Synthesize analysis results into coherent insights",
                constraints=[
                    "Preserve critical information from all inputs",
                    "Identify emergent patterns across components",
                    "Maintain analytical depth while ensuring clarity"
                ],
                output_format="Structured report with executive summary and detailed findings"
            ),
            "discovery": AtomicPrompt(
                task="Discover and map project components",
                constraints=[
                    "Catalog all significant files and directories",
                    "Identify technology stack and dependencies",
                    "Map relationships between components"
                ],
                output_format="Hierarchical structure with component relationships"
            )
        }
        
        self.quality_metrics = {
            "token_efficiency": 0.0,
            "completeness_score": 0.0,
            "precision_rating": 0.0
        }
    
    def create_atomic_prompt(
        self, 
        template_name: str,
        context: str,
        custom_constraints: Optional[List[str]] = None
    ) -> str:
        """
        Create an optimized atomic prompt for specific analysis needs.
        
        Args:
            template_name: Name of the template to use
            context: Context information for the analysis
            custom_constraints: Optional additional constraints
            
        Returns:
            Optimized prompt string following atomic structure
        """
        if template_name not in self.atomic_templates:
            raise ValueError(f"Unknown template: {template_name}")
            
        template = self.atomic_templates[template_name]
        
        # Merge custom constraints if provided
        constraints = template.constraints.copy()
        if custom_constraints:
            constraints.extend(custom_constraints)
            
        atomic_prompt = AtomicPrompt(
            task=template.task,
            constraints=constraints,
            output_format=template.output_format,
            context=context
        )
        
        return atomic_prompt.to_prompt()
    
    def measure_token_efficiency(self, prompt: str, response: str) -> float:
        """
        Measure token efficiency based on power law relationship.
        Implements the ROI zone calculation from atomic prompting theory.
        """
        # Simplified token counting (in production, use actual tokenizer)
        prompt_tokens = len(prompt.split())
        response_tokens = len(response.split())
        
        # Calculate efficiency ratio (quality per token)
        if prompt_tokens == 0:
            return 0.0
            
        efficiency = response_tokens / prompt_tokens
        
        # Apply power law curve optimization
        # Peak efficiency typically occurs in the 150-300 token range
        optimal_range = (150, 300)
        if optimal_range[0] <= prompt_tokens <= optimal_range[1]:
            efficiency *= 1.2  # Boost for optimal range
        elif prompt_tokens > optimal_range[1]:
            efficiency *= 0.8  # Penalty for excessive length
            
        self.quality_metrics["token_efficiency"] = efficiency
        return efficiency
    
    def assess_response_quality(self, response: str, expected_format: str) -> Dict[str, float]:
        """
        Assess response quality across multiple dimensions.
        """
        quality_assessment = {
            "completeness": self._assess_completeness(response, expected_format),
            "structure_adherence": self._assess_structure(response, expected_format),
            "precision": self._assess_precision(response)
        }
        
        # Update internal metrics
        self.quality_metrics.update(quality_assessment)
        
        return quality_assessment
    
    def _assess_completeness(self, response: str, expected_format: str) -> float:
        """Assess how complete the response is relative to expectations."""
        # Simplified completeness check
        expected_elements = ["structure", "dependencies", "patterns"] if "JSON" in expected_format else ["summary", "findings"]
        found_elements = sum(1 for element in expected_elements if element.lower() in response.lower())
        return found_elements / len(expected_elements) if expected_elements else 0.0
    
    def _assess_structure(self, response: str, expected_format: str) -> float:
        """Assess how well the response follows the expected structure."""
        # Check for JSON structure if expected
        if "JSON" in expected_format:
            try:
                import json
                json.loads(response)
                return 1.0
            except:
                return 0.5 if "{" in response and "}" in response else 0.0
        else:
            # Check for basic structure elements
            structure_indicators = ["##", "###", "-", "*", "1.", "2."]
            found_indicators = sum(1 for indicator in structure_indicators if indicator in response)
            return min(found_indicators / 3, 1.0)  # Normalize to max 1.0
    
    def _assess_precision(self, response: str) -> float:
        """Assess the precision and specificity of the response."""
        # Simple heuristic: longer responses with specific terms tend to be more precise
        words = response.split()
        specific_terms = ["function", "class", "module", "import", "dependency", "architecture"]
        specificity_ratio = sum(1 for word in words if word.lower() in specific_terms) / len(words)
        
        # Balance length and specificity
        length_factor = min(len(words) / 200, 1.0)  # Optimal around 200 words
        precision = (specificity_ratio * 0.7) + (length_factor * 0.3)
        
        return min(precision, 1.0)
    
    def get_optimization_recommendations(self) -> List[str]:
        """
        Provide recommendations for optimizing prompt performance.
        """
        recommendations = []
        
        if self.quality_metrics["token_efficiency"] < 0.8:
            recommendations.append("Consider shortening prompts to improve token efficiency")
            
        if self.quality_metrics["completeness_score"] < 0.7:
            recommendations.append("Add more specific constraints to improve response completeness")
            
        if self.quality_metrics["precision_rating"] < 0.6:
            recommendations.append("Include more domain-specific context to improve precision")
            
        return recommendations if recommendations else ["Current prompt performance is optimal"]