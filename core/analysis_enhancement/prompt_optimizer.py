"""
core/analysis_enhancement/prompt_optimizer.py

REALISTIC Prompt Optimization for Enhanced CursorRules Analysis
This module provides actual LLM prompt improvements, not pseudoscience.
"""

import logging
import tiktoken
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class PromptStrategy(Enum):
    """Proven prompt engineering strategies."""
    STRUCTURED = "structured"      # Clear structure with sections
    CHAIN_OF_THOUGHT = "cot"       # Step-by-step reasoning
    FEW_SHOT = "few_shot"          # Examples provided
    CONSTRAINT_GUIDED = "constraint"  # Specific constraints
    ROLE_BASED = "role"            # Expert persona

@dataclass
class PromptMetrics:
    """Real metrics for prompt performance."""
    token_count: int
    estimated_cost: float
    readability_score: float
    specificity_score: float
    
class RealPromptOptimizer:
    """
    Actual prompt optimization that improves LLM interactions.
    Based on proven prompt engineering techniques, not pseudoscience.
    """
    
    def __init__(self, model_name: str = "gpt-4"):
        """Initialize with actual tokenizer."""
        self.model_name = model_name
        try:
            self.tokenizer = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Fallback for unknown models
            self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        
        # Real pricing (approximate, update as needed)
        self.token_costs = {
            "gpt-4": {"input": 0.03/1000, "output": 0.06/1000},
            "gpt-3.5-turbo": {"input": 0.0015/1000, "output": 0.002/1000},
            "claude-3": {"input": 0.015/1000, "output": 0.075/1000}
        }
        
        self.optimization_templates = self._load_optimization_templates()
    
    def _load_optimization_templates(self) -> Dict[str, Dict[str, str]]:
        """Load proven prompt templates for different analysis types."""
        return {
            "code_analysis": {
                "structured": """You are an expert software architect analyzing a codebase.

## Analysis Task
{task_description}

## Codebase Context
{code_context}

## Analysis Requirements
{requirements}

## Expected Output Format
```json
{
  "summary": "Brief overview",
  "architecture": {...},
  "dependencies": {...},
  "recommendations": [...]
}
```

Please provide a thorough but concise analysis.""",

                "chain_of_thought": """You are analyzing a codebase. Let's work through this step by step.

**Step 1**: First, examine the overall structure
{code_context}

**Step 2**: Identify the main architectural patterns

**Step 3**: Analyze dependencies and relationships

**Step 4**: Evaluate code quality and potential issues

**Step 5**: Provide actionable recommendations

Please work through each step systematically.""",

                "constraint_guided": """Analyze the following codebase with these specific constraints:

CONSTRAINTS:
- Focus only on {focus_areas}
- Limit response to {max_length} words
- Prioritize {priority_aspects}
- Include specific examples

CODEBASE:
{code_context}

ANALYSIS:"""
            },
            
            "dependency_analysis": {
                "structured": """## Dependency Analysis Task

**Target**: {target_component}
**Context**: {context}

**Analysis Scope**:
1. Direct dependencies
2. Transitive dependencies  
3. Circular dependencies
4. Security vulnerabilities
5. Update recommendations

**Output Format**: JSON with clear categorization

**Analysis**:""",
                
                "few_shot": """Here are examples of good dependency analysis:

EXAMPLE 1:
Input: React project with outdated lodash
Output: {"critical": ["lodash@4.17.15 has known vulnerabilities"], "recommendations": ["Update to lodash@4.17.21"]}

EXAMPLE 2:
Input: Python project with conflicting versions
Output: {"conflicts": ["requests 2.25.1 vs 2.28.0"], "resolution": "Update to unified version"}

Now analyze this codebase:
{code_context}

Analysis:"""
            }
        }
    
    def optimize_prompt(
        self,
        task_type: str,
        context: str,
        strategy: PromptStrategy = PromptStrategy.STRUCTURED,
        max_tokens: Optional[int] = None,
        focus_areas: Optional[List[str]] = None
    ) -> Tuple[str, PromptMetrics]:
        """
        Create an optimized prompt for the given task.
        
        Args:
            task_type: Type of analysis (code_analysis, dependency_analysis, etc.)
            context: The actual context/code to analyze
            strategy: Prompt engineering strategy to use
            max_tokens: Maximum tokens for the prompt
            focus_areas: Specific areas to focus on
            
        Returns:
            Tuple of (optimized_prompt, metrics)
        """
        
        # Get base template
        if task_type not in self.optimization_templates:
            task_type = "code_analysis"  # fallback
            
        template_group = self.optimization_templates[task_type]
        template = template_group.get(strategy.value, template_group["structured"])
        
        # Fill in template variables
        prompt_vars = {
            "task_description": f"Analyze this {task_type.replace('_', ' ')}",
            "code_context": self._truncate_context(context, max_tokens),
            "requirements": self._generate_requirements(focus_areas),
            "focus_areas": ", ".join(focus_areas) if focus_areas else "architecture and quality",
            "max_length": "500" if max_tokens and max_tokens < 2000 else "1000",
            "priority_aspects": "security, maintainability, performance",
            "target_component": "project dependencies",
            "context": context[:500] + "..." if len(context) > 500 else context
        }
        
        # Generate optimized prompt
        optimized_prompt = template.format(**prompt_vars)
        
        # Calculate real metrics
        metrics = self._calculate_prompt_metrics(optimized_prompt)
        
        return optimized_prompt, metrics
    
    def _truncate_context(self, context: str, max_tokens: Optional[int]) -> str:
        """Intelligently truncate context to fit token limits."""
        if not max_tokens:
            return context
            
        # Reserve 30% of tokens for the template structure
        available_tokens = int(max_tokens * 0.7)
        
        # Tokenize and truncate
        tokens = self.tokenizer.encode(context)
        if len(tokens) <= available_tokens:
            return context
            
        # Truncate and add indication
        truncated_tokens = tokens[:available_tokens-10]  # Reserve for "..."
        truncated_text = self.tokenizer.decode(truncated_tokens)
        return truncated_text + "\n\n[... content truncated for token limit ...]"
    
    def _generate_requirements(self, focus_areas: Optional[List[str]]) -> str:
        """Generate analysis requirements based on focus areas."""
        if not focus_areas:
            return """- Identify architectural patterns
- Analyze code quality
- Assess maintainability
- Highlight potential issues"""
        
        requirements = []
        for area in focus_areas:
            if area == "security":
                requirements.append("- Identify security vulnerabilities and risks")
            elif area == "performance":
                requirements.append("- Analyze performance bottlenecks and optimization opportunities")
            elif area == "maintainability":
                requirements.append("- Evaluate code maintainability and technical debt")
            elif area == "dependencies":
                requirements.append("- Examine dependency structure and update requirements")
            else:
                requirements.append(f"- Focus on {area} aspects")
        
        return "\n".join(requirements)
    
    def _calculate_prompt_metrics(self, prompt: str) -> PromptMetrics:
        """Calculate real metrics for the prompt."""
        # Real token count
        token_count = len(self.tokenizer.encode(prompt))
        
        # Estimated cost (input tokens only)
        model_key = "gpt-4" if "gpt-4" in self.model_name else "gpt-3.5-turbo"
        cost_per_token = self.token_costs.get(model_key, self.token_costs["gpt-3.5-turbo"])["input"]
        estimated_cost = token_count * cost_per_token
        
        # Readability score (simple heuristic)
        sentences = prompt.count('.') + prompt.count('!') + prompt.count('?')
        words = len(prompt.split())
        avg_sentence_length = words / max(sentences, 1)
        readability_score = max(0.0, min(1.0, 1.0 - (avg_sentence_length - 15) / 30))
        
        # Specificity score (based on specific keywords)
        specific_words = ['analyze', 'identify', 'evaluate', 'assess', 'examine', 'specific', 'detailed']
        specificity_count = sum(1 for word in specific_words if word in prompt.lower())
        specificity_score = min(1.0, specificity_count / 5)
        
        return PromptMetrics(
            token_count=token_count,
            estimated_cost=estimated_cost,
            readability_score=readability_score,
            specificity_score=specificity_score
        )
    
    def batch_optimize_prompts(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Tuple[str, PromptMetrics]]:
        """Optimize multiple prompts efficiently."""
        results = []
        
        for task in tasks:
            prompt, metrics = self.optimize_prompt(
                task_type=task.get("type", "code_analysis"),
                context=task.get("context", ""),
                strategy=PromptStrategy(task.get("strategy", "structured")),
                max_tokens=task.get("max_tokens"),
                focus_areas=task.get("focus_areas")
            )
            results.append((prompt, metrics))
        
        return results
    
    def analyze_prompt_performance(
        self,
        prompt: str,
        response: str,
        expected_elements: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Analyze the performance of a prompt based on the response.
        This provides real feedback for prompt optimization.
        """
        
        response_tokens = len(self.tokenizer.encode(response))
        prompt_tokens = len(self.tokenizer.encode(prompt))
        
        # Efficiency: response length vs prompt length
        efficiency = response_tokens / max(prompt_tokens, 1)
        
        # Completeness: check if expected elements are present
        completeness = 1.0
        if expected_elements:
            found_elements = sum(1 for elem in expected_elements if elem.lower() in response.lower())
            completeness = found_elements / len(expected_elements)
        
        # Response quality indicators
        has_structure = any(marker in response for marker in ['##', '```', '1.', '2.', '{', '}'])
        structure_score = 1.0 if has_structure else 0.5
        
        # Length appropriateness (not too short, not too verbose)
        words = len(response.split())
        length_score = 1.0
        if words < 50:
            length_score = 0.5  # Too short
        elif words > 2000:
            length_score = 0.7  # Too verbose
        
        return {
            "efficiency": min(efficiency, 2.0),  # Cap at 2.0
            "completeness": completeness,
            "structure_score": structure_score,
            "length_score": length_score,
            "overall_score": (efficiency + completeness + structure_score + length_score) / 4
        }

class PromptCache:
    """Simple caching for optimized prompts to avoid regeneration."""
    
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.access_count = {}
        self.max_size = max_size
    
    def get_cache_key(self, task_type: str, strategy: str, context_hash: str) -> str:
        """Generate cache key for prompt."""
        return f"{task_type}:{strategy}:{context_hash}"
    
    def get(self, key: str) -> Optional[str]:
        """Get cached prompt."""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None
    
    def put(self, key: str, prompt: str):
        """Cache optimized prompt."""
        if len(self.cache) >= self.max_size:
            # Remove least used item
            least_used = min(self.access_count.items(), key=lambda x: x[1])[0]
            del self.cache[least_used]
            del self.access_count[least_used]
        
        self.cache[key] = prompt
        self.access_count[key] = 1