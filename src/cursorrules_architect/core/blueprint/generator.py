"""
core/blueprint/generator.py

This module provides the Blueprint Generator for creating detailed phase specifications
that describe tasks, agent roles, and evaluation criteria before any model invocation.
"""

# ====================================================
# Importing Required Libraries
# ====================================================

import json
import yaml
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import logging

# ====================================================
# Blueprint Generator Class
# ====================================================

class BlueprintGenerator:
    """
    Generates detailed blueprints for phase execution in Plan Mode workflow.
    
    The blueprint serves as a pre-phase specification that defines:
    - Tasks to be executed
    - Agent roles and responsibilities
    - Evaluation criteria for success
    - Execution constraints and requirements
    """
    
    def __init__(self, output_dir: str = "phases_output"):
        """
        Initialize the Blueprint Generator.
        
        Args:
            output_dir: Directory where blueprints will be stored
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def generate_blueprint(
        self,
        phase_name: str,
        project_context: Dict[str, Any],
        custom_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive blueprint for a specific phase.
        
        Args:
            phase_name: Name of the phase (e.g., "phase1", "phase2")
            project_context: Context information about the project
            custom_requirements: Optional custom requirements for the phase
            
        Returns:
            Dictionary containing the complete blueprint specification
        """
        blueprint = {
            "metadata": self._generate_metadata(phase_name),
            "context": self._process_context(project_context),
            "tasks": self._generate_tasks(phase_name, project_context),
            "agents": self._define_agents(phase_name),
            "evaluation_criteria": self._define_evaluation_criteria(phase_name),
            "execution_plan": self._create_execution_plan(phase_name),
            "constraints": self._define_constraints(phase_name, custom_requirements)
        }
        
        # Save the blueprint
        self._save_blueprint(blueprint, phase_name)
        
        return blueprint
    
    def _generate_metadata(self, phase_name: str) -> Dict[str, Any]:
        """Generate metadata for the blueprint."""
        return {
            "phase": phase_name,
            "generated_at": datetime.now().isoformat(),
            "version": "1.0",
            "generator": "BlueprintGenerator",
            "mode": "plan_mode"
        }
    
    def _process_context(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure the project context."""
        return {
            "project_info": project_context.get("project_info", {}),
            "environment": project_context.get("environment", {}),
            "dependencies": project_context.get("dependencies", {}),
            "existing_analysis": project_context.get("existing_analysis", {})
        }
    
    def _generate_tasks(self, phase_name: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific tasks based on phase and context."""
        phase_tasks = {
            "phase1": [
                {
                    "id": "T1.1",
                    "name": "Directory Structure Analysis",
                    "description": "Analyze and map the complete directory structure",
                    "priority": "high",
                    "dependencies": [],
                    "expected_output": "Structured directory tree with annotations"
                },
                {
                    "id": "T1.2",
                    "name": "Dependency Investigation",
                    "description": "Identify all project dependencies and their versions",
                    "priority": "high",
                    "dependencies": [],
                    "expected_output": "Dependency graph with version compatibility analysis"
                },
                {
                    "id": "T1.3",
                    "name": "Technology Stack Identification",
                    "description": "Identify all frameworks, libraries, and technologies used",
                    "priority": "high",
                    "dependencies": ["T1.1", "T1.2"],
                    "expected_output": "Comprehensive tech stack documentation"
                }
            ],
            "phase2": [
                {
                    "id": "T2.1",
                    "name": "Analysis Plan Creation",
                    "description": "Create detailed analysis plan based on Phase 1 findings",
                    "priority": "high",
                    "dependencies": ["phase1"],
                    "expected_output": "Structured analysis plan with agent assignments"
                },
                {
                    "id": "T2.2",
                    "name": "Resource Allocation",
                    "description": "Allocate computational and agent resources",
                    "priority": "medium",
                    "dependencies": ["T2.1"],
                    "expected_output": "Resource allocation matrix"
                }
            ],
            "phase3": [
                {
                    "id": "T3.1",
                    "name": "Component Deep Dive",
                    "description": "Perform deep analysis of identified components",
                    "priority": "high",
                    "dependencies": ["phase2"],
                    "expected_output": "Detailed component analysis reports"
                },
                {
                    "id": "T3.2",
                    "name": "Pattern Recognition",
                    "description": "Identify architectural patterns and anti-patterns",
                    "priority": "medium",
                    "dependencies": ["T3.1"],
                    "expected_output": "Pattern catalog with recommendations"
                }
            ],
            "phase4": [
                {
                    "id": "T4.1",
                    "name": "Finding Synthesis",
                    "description": "Synthesize findings from all previous analyses",
                    "priority": "high",
                    "dependencies": ["phase3"],
                    "expected_output": "Integrated findings report"
                },
                {
                    "id": "T4.2",
                    "name": "Recommendation Generation",
                    "description": "Generate actionable recommendations",
                    "priority": "high",
                    "dependencies": ["T4.1"],
                    "expected_output": "Prioritized recommendation list"
                }
            ],
            "phase5": [
                {
                    "id": "T5.1",
                    "name": "Report Consolidation",
                    "description": "Consolidate all phase reports into final deliverable",
                    "priority": "high",
                    "dependencies": ["phase4"],
                    "expected_output": "Comprehensive final report"
                },
                {
                    "id": "T5.2",
                    "name": "Documentation Generation",
                    "description": "Generate project documentation and guidelines",
                    "priority": "medium",
                    "dependencies": ["T5.1"],
                    "expected_output": "Complete documentation package"
                }
            ]
        }
        
        return phase_tasks.get(phase_name, [])
    
    def _define_agents(self, phase_name: str) -> List[Dict[str, Any]]:
        """Define agent roles and configurations for the phase."""
        phase_agents = {
            "phase1": [
                {
                    "id": "A1.1",
                    "name": "Structure Agent",
                    "role": "Directory and file organization analyst",
                    "capabilities": [
                        "Directory traversal and mapping",
                        "File relationship analysis",
                        "Architectural component identification"
                    ],
                    "assigned_tasks": ["T1.1"]
                },
                {
                    "id": "A1.2",
                    "name": "Dependency Agent",
                    "role": "Package and library investigator",
                    "capabilities": [
                        "Dependency resolution",
                        "Version compatibility checking",
                        "Security vulnerability assessment"
                    ],
                    "assigned_tasks": ["T1.2"]
                },
                {
                    "id": "A1.3",
                    "name": "Tech Stack Agent",
                    "role": "Technology and framework identifier",
                    "capabilities": [
                        "Framework detection",
                        "Best practices research",
                        "Documentation gathering"
                    ],
                    "assigned_tasks": ["T1.3"]
                }
            ],
            "phase2": [
                {
                    "id": "A2.1",
                    "name": "Planning Orchestrator",
                    "role": "Master planner and coordinator",
                    "capabilities": [
                        "Strategic planning",
                        "Resource optimization",
                        "Task dependency resolution"
                    ],
                    "assigned_tasks": ["T2.1", "T2.2"]
                }
            ],
            "phase3": [
                {
                    "id": "A3.1",
                    "name": "Analysis Agent",
                    "role": "Deep component analyzer",
                    "capabilities": [
                        "Code quality assessment",
                        "Performance analysis",
                        "Security audit"
                    ],
                    "assigned_tasks": ["T3.1", "T3.2"]
                }
            ],
            "phase4": [
                {
                    "id": "A4.1",
                    "name": "Synthesis Agent",
                    "role": "Finding integrator and synthesizer",
                    "capabilities": [
                        "Cross-phase correlation",
                        "Insight generation",
                        "Recommendation formulation"
                    ],
                    "assigned_tasks": ["T4.1", "T4.2"]
                }
            ],
            "phase5": [
                {
                    "id": "A5.1",
                    "name": "Consolidation Agent",
                    "role": "Report consolidator and finalizer",
                    "capabilities": [
                        "Report generation",
                        "Documentation creation",
                        "Quality assurance"
                    ],
                    "assigned_tasks": ["T5.1", "T5.2"]
                }
            ]
        }
        
        return phase_agents.get(phase_name, [])
    
    def _define_evaluation_criteria(self, phase_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """Define evaluation criteria for the phase."""
        return {
            "task_criteria": [
                {
                    "criterion": "Completeness",
                    "description": "All required outputs are generated",
                    "weight": 0.3,
                    "measurement": "Percentage of completed deliverables"
                },
                {
                    "criterion": "Quality",
                    "description": "Outputs meet quality standards",
                    "weight": 0.3,
                    "measurement": "Quality score based on defined metrics"
                },
                {
                    "criterion": "Timeliness",
                    "description": "Tasks completed within allocated time",
                    "weight": 0.2,
                    "measurement": "Time taken vs. estimated time"
                },
                {
                    "criterion": "Accuracy",
                    "description": "Information is correct and verified",
                    "weight": 0.2,
                    "measurement": "Error rate and validation results"
                }
            ],
            "phase_criteria": [
                {
                    "criterion": "Goal Achievement",
                    "description": "Phase objectives are met",
                    "measurement": "Objective completion percentage"
                },
                {
                    "criterion": "Integration Success",
                    "description": "Outputs integrate well with other phases",
                    "measurement": "Integration test results"
                }
            ]
        }
    
    def _create_execution_plan(self, phase_name: str) -> Dict[str, Any]:
        """Create the execution plan for the phase."""
        return {
            "sequence": self._get_execution_sequence(phase_name),
            "parallelization": self._get_parallelization_strategy(phase_name),
            "checkpoints": self._define_checkpoints(phase_name),
            "rollback_strategy": self._define_rollback_strategy(phase_name)
        }
    
    def _get_execution_sequence(self, phase_name: str) -> List[str]:
        """Get the execution sequence for tasks."""
        sequences = {
            "phase1": ["T1.1", "T1.2", "T1.3"],
            "phase2": ["T2.1", "T2.2"],
            "phase3": ["T3.1", "T3.2"],
            "phase4": ["T4.1", "T4.2"],
            "phase5": ["T5.1", "T5.2"]
        }
        return sequences.get(phase_name, [])
    
    def _get_parallelization_strategy(self, phase_name: str) -> Dict[str, Any]:
        """Define parallelization strategy."""
        if phase_name == "phase1":
            return {
                "parallel_groups": [["T1.1", "T1.2"]],
                "sequential": ["T1.3"]
            }
        return {"parallel_groups": [], "sequential": self._get_execution_sequence(phase_name)}
    
    def _define_checkpoints(self, phase_name: str) -> List[Dict[str, Any]]:
        """Define checkpoints for the phase."""
        return [
            {
                "id": f"CP_{phase_name}_1",
                "after_task": self._get_execution_sequence(phase_name)[0] if self._get_execution_sequence(phase_name) else None,
                "validation": "Initial task completion check",
                "action_on_failure": "retry_with_adjusted_parameters"
            },
            {
                "id": f"CP_{phase_name}_final",
                "after_task": "phase_completion",
                "validation": "Full phase validation",
                "action_on_failure": "escalate_to_supervisor"
            }
        ]
    
    def _define_rollback_strategy(self, phase_name: str) -> Dict[str, Any]:
        """Define rollback strategy for failures."""
        return {
            "trigger_conditions": ["critical_failure", "validation_failure"],
            "rollback_points": self._define_checkpoints(phase_name),
            "recovery_actions": ["restore_previous_state", "adjust_parameters", "retry_with_fallback"]
        }
    
    def _define_constraints(self, phase_name: str, custom_requirements: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Define constraints and requirements for the phase."""
        base_constraints = {
            "time_limit": "2 hours",
            "resource_limits": {
                "max_agents": 5,
                "max_parallel_tasks": 3,
                "memory_limit": "4GB"
            },
            "quality_thresholds": {
                "min_accuracy": 0.85,
                "min_completeness": 0.90
            }
        }
        
        if custom_requirements:
            base_constraints.update(custom_requirements)
        
        return base_constraints
    
    def _save_blueprint(self, blueprint: Dict[str, Any], phase_name: str):
        """Save the blueprint to file."""
        # Save as JSON
        json_path = self.output_dir / f"{phase_name}_blueprint.json"
        with open(json_path, 'w') as f:
            json.dump(blueprint, f, indent=2)
        
        # Save as YAML for readability
        yaml_path = self.output_dir / f"{phase_name}_blueprint.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(blueprint, f, default_flow_style=False)
        
        # Save as Markdown for documentation
        md_path = self.output_dir / f"{phase_name}_blueprint.md"
        self._save_as_markdown(blueprint, md_path)
        
        self.logger.info(f"Blueprint saved to {json_path}, {yaml_path}, and {md_path}")
    
    def _save_as_markdown(self, blueprint: Dict[str, Any], path: Path):
        """Save blueprint as a formatted Markdown document."""
        with open(path, 'w') as f:
            f.write(f"# {blueprint['metadata']['phase'].upper()} Blueprint\n\n")
            f.write(f"Generated: {blueprint['metadata']['generated_at']}\n\n")
            
            # Tasks section
            f.write("## Tasks\n\n")
            for task in blueprint['tasks']:
                f.write(f"### {task['id']}: {task['name']}\n")
                f.write(f"- **Description**: {task['description']}\n")
                f.write(f"- **Priority**: {task['priority']}\n")
                f.write(f"- **Dependencies**: {', '.join(task['dependencies']) if task['dependencies'] else 'None'}\n")
                f.write(f"- **Expected Output**: {task['expected_output']}\n\n")
            
            # Agents section
            f.write("## Agents\n\n")
            for agent in blueprint['agents']:
                f.write(f"### {agent['id']}: {agent['name']}\n")
                f.write(f"- **Role**: {agent['role']}\n")
                f.write(f"- **Capabilities**:\n")
                for cap in agent['capabilities']:
                    f.write(f"  - {cap}\n")
                f.write(f"- **Assigned Tasks**: {', '.join(agent['assigned_tasks'])}\n\n")
            
            # Evaluation Criteria section
            f.write("## Evaluation Criteria\n\n")
            f.write("### Task Criteria\n")
            for criterion in blueprint['evaluation_criteria']['task_criteria']:
                f.write(f"- **{criterion['criterion']}** ({criterion['weight']*100}%): {criterion['description']}\n")
            
            f.write("\n### Phase Criteria\n")
            for criterion in blueprint['evaluation_criteria']['phase_criteria']:
                f.write(f"- **{criterion['criterion']}**: {criterion['description']}\n")
            
            # Execution Plan section
            f.write("\n## Execution Plan\n\n")
            f.write(f"- **Sequence**: {' → '.join(blueprint['execution_plan']['sequence'])}\n")
            f.write(f"- **Parallelization**: {blueprint['execution_plan']['parallelization']}\n")
            
            # Constraints section
            f.write("\n## Constraints\n\n")
            f.write(f"- **Time Limit**: {blueprint['constraints']['time_limit']}\n")
            f.write(f"- **Resource Limits**: {blueprint['constraints']['resource_limits']}\n")
            f.write(f"- **Quality Thresholds**: {blueprint['constraints']['quality_thresholds']}\n")
    
    def inject_into_prompt(self, base_prompt: str, blueprint: Dict[str, Any]) -> str:
        """
        Inject blueprint into a prompt template to enforce Plan Mode workflow.
        
        Args:
            base_prompt: The base prompt template
            blueprint: The blueprint to inject
            
        Returns:
            Enhanced prompt with blueprint context
        """
        blueprint_context = f"""
# BLUEPRINT CONTEXT (Plan Mode Active)

## Phase: {blueprint['metadata']['phase']}
Generated: {blueprint['metadata']['generated_at']}

## Your Tasks:
{self._format_tasks_for_prompt(blueprint['tasks'])}

## Your Role:
{self._format_agents_for_prompt(blueprint['agents'])}

## Success Criteria:
{self._format_criteria_for_prompt(blueprint['evaluation_criteria'])}

## Execution Constraints:
- Time Limit: {blueprint['constraints']['time_limit']}
- Quality Thresholds: Minimum {blueprint['constraints']['quality_thresholds']['min_accuracy']*100}% accuracy

---
"""
        return blueprint_context + base_prompt
    
    def _format_tasks_for_prompt(self, tasks: List[Dict[str, Any]]) -> str:
        """Format tasks for prompt injection."""
        formatted = []
        for task in tasks:
            formatted.append(f"- [{task['id']}] {task['name']}: {task['description']}")
        return "\n".join(formatted)
    
    def _format_agents_for_prompt(self, agents: List[Dict[str, Any]]) -> str:
        """Format agent roles for prompt injection."""
        if not agents:
            return "No specific agent role defined."
        
        formatted = []
        for agent in agents:
            formatted.append(f"You are the {agent['name']} - {agent['role']}")
            formatted.append(f"Your capabilities: {', '.join(agent['capabilities'])}")
        return "\n".join(formatted)
    
    def _format_criteria_for_prompt(self, criteria: Dict[str, List[Dict[str, Any]]]) -> str:
        """Format evaluation criteria for prompt injection."""
        formatted = []
        for criterion in criteria['task_criteria']:
            formatted.append(f"- {criterion['criterion']}: {criterion['description']}")
        return "\n".join(formatted)
