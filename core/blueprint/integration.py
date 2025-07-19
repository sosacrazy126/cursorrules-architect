"""
core/blueprint/integration.py

This module integrates the Blueprint Generator with the existing phase execution system,
enabling Plan Mode workflow by injecting blueprints into agent prompts.
"""

# ====================================================
# Importing Required Libraries
# ====================================================

from typing import Dict, Any, Optional
import asyncio
import logging
from pathlib import Path

from core.blueprint.generator import BlueprintGenerator
from core.agents.base import BaseArchitect
from config.prompts.phase_1_prompts import PHASE_1_BASE_PROMPT

# ====================================================
# Blueprint Integration Class
# ====================================================

class BlueprintIntegration:
    """
    Integrates blueprint generation with phase execution.
    
    This class modifies the existing phase workflow to include:
    1. Pre-phase blueprint generation
    2. Prompt enhancement with blueprint context
    3. Post-phase evaluation against blueprint criteria
    """
    
    def __init__(self, blueprint_dir: str = "phases_output"):
        """Initialize the blueprint integration."""
        self.generator = BlueprintGenerator(blueprint_dir)
        self.logger = logging.getLogger(__name__)
    
    async def execute_phase_with_blueprint(
        self,
        phase_name: str,
        phase_executor: Any,  # The phase analysis class (e.g., Phase1Analysis)
        project_context: Dict[str, Any],
        custom_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a phase with blueprint-driven Plan Mode.
        
        Args:
            phase_name: Name of the phase to execute
            phase_executor: The phase analysis instance
            project_context: Context information about the project
            custom_requirements: Optional custom requirements
            
        Returns:
            Enhanced phase results including blueprint evaluation
        """
        # Step 1: Generate blueprint
        self.logger.info(f"Generating blueprint for {phase_name}")
        blueprint = self.generator.generate_blueprint(
            phase_name,
            project_context,
            custom_requirements
        )
        
        # Step 2: Enhance phase architects with blueprint context
        self._enhance_architects_with_blueprint(phase_executor, blueprint)
        
        # Step 3: Execute the phase
        self.logger.info(f"Executing {phase_name} with blueprint context")
        
        # Determine the appropriate method to call based on phase
        if phase_name == "phase1":
            phase_results = await phase_executor.run(
                project_context.get("tree_structure", []),
                project_context.get("package_info", {})
            )
        else:
            # For other phases, adapt the call as needed
            phase_results = await phase_executor.run(project_context)
        
        # Step 4: Evaluate results against blueprint criteria
        evaluation = self._evaluate_against_blueprint(phase_results, blueprint)
        
        # Step 5: Return enhanced results
        return {
            "phase": phase_name,
            "blueprint": blueprint,
            "results": phase_results,
            "evaluation": evaluation,
            "plan_mode": True
        }
    
    def _enhance_architects_with_blueprint(
        self,
        phase_executor: Any,
        blueprint: Dict[str, Any]
    ):
        """
        Enhance phase architects with blueprint context.
        
        This modifies the architects' prompts to include blueprint specifications.
        """
        if hasattr(phase_executor, 'architects'):
            for architect in phase_executor.architects:
                # Store original analyze method
                original_analyze = architect.analyze
                
                # Create blueprint-enhanced analyze method
                async def enhanced_analyze(context, architect=architect, original=original_analyze):
                    # Inject blueprint into the context
                    enhanced_context = {
                        **context,
                        "blueprint": blueprint,
                        "plan_mode": True
                    }
                    
                    # If the architect has a prompt template, enhance it
                    if hasattr(architect, 'prompt_template'):
                        original_template = architect.prompt_template
                        architect.prompt_template = self.generator.inject_into_prompt(
                            original_template,
                            blueprint
                        )
                    
                    # Execute with enhanced context
                    result = await original(enhanced_context)
                    
                    # Restore original template if it was modified
                    if hasattr(architect, 'prompt_template'):
                        architect.prompt_template = original_template
                    
                    return result
                
                # Replace analyze method with enhanced version
                architect.analyze = enhanced_analyze
    
    def _evaluate_against_blueprint(
        self,
        phase_results: Dict[str, Any],
        blueprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate phase results against blueprint criteria.
        
        Args:
            phase_results: The results from phase execution
            blueprint: The blueprint specification
            
        Returns:
            Evaluation results including scores and recommendations
        """
        evaluation = {
            "task_completion": self._evaluate_task_completion(phase_results, blueprint),
            "criteria_scores": self._calculate_criteria_scores(phase_results, blueprint),
            "overall_score": 0.0,
            "recommendations": []
        }
        
        # Calculate overall score
        task_score = evaluation["task_completion"]["completion_rate"]
        criteria_scores = evaluation["criteria_scores"]
        
        # Weighted average of all scores
        total_weight = sum(c["weight"] for c in criteria_scores.values())
        weighted_sum = sum(c["score"] * c["weight"] for c in criteria_scores.values())
        
        evaluation["overall_score"] = (task_score * 0.5) + (weighted_sum / total_weight * 0.5)
        
        # Generate recommendations based on evaluation
        if evaluation["overall_score"] < 0.7:
            evaluation["recommendations"].append(
                "Phase performance below threshold. Consider re-execution with adjusted parameters."
            )
        
        return evaluation
    
    def _evaluate_task_completion(
        self,
        phase_results: Dict[str, Any],
        blueprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate task completion against blueprint tasks."""
        expected_tasks = blueprint["tasks"]
        completed_tasks = []
        
        # Simple heuristic: check if expected outputs are mentioned in results
        if "findings" in phase_results:
            findings_str = str(phase_results["findings"]).lower()
            
            for task in expected_tasks:
                # Check if task output keywords appear in findings
                output_keywords = task["expected_output"].lower().split()
                if any(keyword in findings_str for keyword in output_keywords):
                    completed_tasks.append(task["id"])
        
        completion_rate = len(completed_tasks) / len(expected_tasks) if expected_tasks else 0
        
        return {
            "expected_tasks": len(expected_tasks),
            "completed_tasks": len(completed_tasks),
            "completion_rate": completion_rate,
            "completed_task_ids": completed_tasks
        }
    
    def _calculate_criteria_scores(
        self,
        phase_results: Dict[str, Any],
        blueprint: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Calculate scores for each evaluation criterion."""
        criteria = blueprint["evaluation_criteria"]["task_criteria"]
        scores = {}
        
        for criterion in criteria:
            # Simplified scoring logic - in production, this would be more sophisticated
            if criterion["criterion"] == "Completeness":
                score = 0.8  # Placeholder - would analyze actual completeness
            elif criterion["criterion"] == "Quality":
                score = 0.85  # Placeholder - would assess quality metrics
            elif criterion["criterion"] == "Timeliness":
                score = 0.9  # Placeholder - would check execution time
            elif criterion["criterion"] == "Accuracy":
                score = 0.87  # Placeholder - would validate accuracy
            else:
                score = 0.5
            
            scores[criterion["criterion"]] = {
                "score": score,
                "weight": criterion["weight"],
                "description": criterion["description"]
            }
        
        return scores


# ====================================================
# Helper Functions
# ====================================================

def create_blueprint_enhanced_phase(phase_class: Any) -> Any:
    """
    Decorator to enhance a phase class with blueprint functionality.
    
    Args:
        phase_class: The original phase analysis class
        
    Returns:
        Enhanced phase class with blueprint support
    """
    class BlueprintEnhancedPhase(phase_class):
        """Enhanced phase with automatic blueprint generation."""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.blueprint_integration = BlueprintIntegration()
        
        async def run(self, *args, **kwargs):
            """Run phase with blueprint enhancement."""
            # Extract phase name from class name (e.g., Phase1Analysis -> phase1)
            phase_name = self.__class__.__name__.lower().replace("analysis", "")
            
            # Create project context from arguments
            if len(args) >= 2:  # Phase 1 style arguments
                project_context = {
                    "tree_structure": args[0],
                    "package_info": args[1]
                }
            else:
                project_context = args[0] if args else kwargs
            
            # Execute with blueprint
            return await self.blueprint_integration.execute_phase_with_blueprint(
                phase_name,
                self,
                project_context
            )
    
    return BlueprintEnhancedPhase


# ====================================================
# Example Usage
# ====================================================

async def demonstrate_blueprint_integration():
    """Demonstrate how to use blueprint integration with existing phases."""
    from core.analysis.phase_1 import Phase1Analysis
    
    # Create blueprint-enhanced phase
    EnhancedPhase1 = create_blueprint_enhanced_phase(Phase1Analysis)
    
    # Initialize enhanced phase
    phase1 = EnhancedPhase1()
    
    # Sample project context
    project_context = {
        "tree_structure": ["src/", "src/main.py", "tests/", "README.md"],
        "package_info": {"dependencies": ["fastapi", "pydantic"]}
    }
    
    # Run phase with blueprint
    results = await phase1.run(
        project_context["tree_structure"],
        project_context["package_info"]
    )
    
    print(f"Phase completed with Plan Mode: {results['plan_mode']}")
    print(f"Overall score: {results['evaluation']['overall_score']}")
    
    return results
