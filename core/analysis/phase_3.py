"""
core/analysis/phase_3.py

This module provides functionality for Phase 3 (Deep Analysis) of the project analysis.
It defines the agents and methods needed for in-depth analysis of the project's code and architecture.
"""

# ====================================================
# Importing Required Libraries
# This section imports all the necessary libraries and modules needed for the script.
# ====================================================

import asyncio
import json
from typing import Dict, List, Any
from pathlib import Path
from core.agents.anthropic import ClaudeAgent
from core.utils.tools.file_retriever import get_filtered_formatted_contents

# ====================================================
# Phase 3 Analysis Class
# This class handles the deep analysis phase (Phase 3) of the project.
# It uses AI agents to analyze the code and architecture.
# ====================================================

class Phase3Analysis:
    """
    Class responsible for Phase 3 (Deep Analysis) of the project analysis.
    
    This phase uses dynamically created Claude agents based on Phase 2's output
    to perform in-depth analysis of the project's code and architecture.
    """
    
    # ====================================================
    # Initialization (__init__)
    # This method sets up the initial state of the Phase3Analysis class.
    # ====================================================
    def __init__(self):
        """Initialize the Phase 3 analysis."""
        # The agents will be created dynamically based on Phase 2's output
        self.agents = []
        
        # Base prompt template for all Phase 3 agents
        self.base_prompt_template = """You are the {agent_name}, responsible for analyzing a codebase.

Your role is focused on {agent_description}

Analyze this project context with special attention to the files assigned to you:

TREE STRUCTURE:
{tree_structure}

ASSIGNED FILES:
{assigned_files}

FILE CONTENTS:
{file_contents}

Analyze the code following these guidelines:
1. Focus on understanding the purpose and functionality of each file
2. Identify key patterns and design decisions
3. Note any potential issues, optimizations, or improvements
4. Pay attention to relationships between different components
5. Summarize your findings in a clear, structured format

Format your response as a structured report with clear sections and findings."""

        # Fallback agents to use if Phase 2 doesn't provide valid agent definitions
        self.fallback_agent_configs = [
            {
                "name": "Code Analysis Agent",
                "description": "examining core logic and patterns, reviewing implementation details, and identifying optimization opportunities.",
                "responsibilities": [
                    "Examine core logic and patterns",
                    "Review implementation details",
                    "Identify optimization opportunities",
                    "Analyze algorithmic efficiency",
                    "Evaluate code quality and readability"
                ]
            },
            {
                "name": "Dependency Mapping Agent",
                "description": "mapping file relationships, documenting import/export patterns, and charting data flow paths.",
                "responsibilities": [
                    "Map all file relationships",
                    "Document import/export patterns",
                    "Chart data flow paths",
                    "Identify coupling between components",
                    "Analyze dependency hierarchies"
                ]
            },
            {
                "name": "Architecture Agent",
                "description": "studying design patterns, reviewing architectural decisions, and evaluating system structure.",
                "responsibilities": [
                    "Study design patterns",
                    "Review architectural decisions",
                    "Evaluate system structure",
                    "Identify architectural principles",
                    "Assess scalability and maintainability"
                ]
            }
        ]
    
    # ====================================================
    # Format Agent Prompt Function
    # This function formats the prompt for a specific agent.
    # ====================================================
    def _format_agent_prompt(self, agent_config: Dict, context: Dict) -> str:
        """
        Format a prompt for a specific agent using the base template.
        
        Args:
            agent_config: Dictionary containing agent name and description
            context: Dictionary containing the context for analysis
            
        Returns:
            Formatted prompt string
        """
        # Extract required context elements with defaults
        tree_structure = "\n".join(context.get("tree_structure", ["No tree structure provided"]))
        
        # Extract file-related information
        assigned_files = context.get("assigned_files", ["No specific files assigned"])
        if isinstance(assigned_files, list):
            assigned_files = "\n".join(f"- {file}" for file in assigned_files)
        
        # Extract file contents
        file_contents = context.get("file_contents", "No file contents provided")
        
        # Return a formatted string that can be used directly
        return self.base_prompt_template.format(
            agent_name=agent_config["name"],
            agent_description=agent_config["description"],
            tree_structure=tree_structure,
            assigned_files=assigned_files,
            file_contents=file_contents
        )
    
    # ====================================================
    # Create Agents from Phase 2 Function
    # This function creates agent instances based on the output from Phase 2.
    # ====================================================
    def _create_agents_from_phase2(self, agent_definitions: List[Dict]) -> List[ClaudeAgent]:
        """
        Create agents dynamically based on Phase 2's output.
        
        Args:
            agent_definitions: List of agent definitions from Phase 2
            
        Returns:
            List of ClaudeAgent instances
        """
        agents = []
        
        # If no agent definitions were provided, use fallback agents
        if not agent_definitions:
            for config in self.fallback_agent_configs:
                agents.append(
                    ClaudeAgent(
                        name=config["name"],
                        role=config["description"],
                        responsibilities=config["responsibilities"],
                        prompt_template=self.base_prompt_template
                    )
                )
            return agents
        
        # Create Claude agents based on the provided definitions
        for agent_def in agent_definitions:
            # Extract relevant information from the agent definition
            name = agent_def.get("name", f"Agent {agent_def.get('id', 'Unknown')}")
            description = agent_def.get("description", "analyzing the assigned codebase files")
            
            # Create responsibilities list, either from the definition or a default
            responsibilities = agent_def.get("responsibilities", [])
            if not responsibilities:
                responsibilities = ["Analyze assigned files and provide insights"]
            
            # Create the agent with the extracted information
            agents.append(
                ClaudeAgent(
                    name=name,
                    role=description,
                    responsibilities=responsibilities,
                    prompt_template=None  # Use default template in ClaudeAgent
                )
            )
        
        return agents
    
    # ====================================================
    # Run Analysis Function
    # This function runs the deep analysis using the created agents.
    # ====================================================
    async def run(self, analysis_plan: Dict, tree: List[str], project_dir: Path) -> Dict:
        """
        Run the Deep Analysis Phase using dynamically created Claude agents.
        
        Args:
            analysis_plan: Dictionary containing the analysis plan from Phase 2
            tree: List of strings representing the project directory tree
            project_dir: Path to the project directory
            
        Returns:
            Dictionary containing the results of the phase
        """
        # Extract agent definitions from the analysis plan
        agent_definitions = analysis_plan.get("agents", [])
        
        # Create agents dynamically based on Phase 2's output
        self.agents = self._create_agents_from_phase2(agent_definitions)
        
        # Prepare the base context for the agents
        base_context = {
            "tree_structure": tree
        }
        
        # Create agent-specific contexts with their assigned files
        agent_contexts = []
        agent_tasks = []
        
        # Match agents with their definitions
        for i, agent in enumerate(self.agents):
            # Get the corresponding agent definition
            agent_def = agent_definitions[i] if i < len(agent_definitions) else None
            
            if agent_def and "file_assignments" in agent_def:
                # Get file contents for this agent's assignments
                agent_files = agent_def["file_assignments"]
                agent_file_contents = get_filtered_formatted_contents(project_dir, agent_files)
                
                # Create context with base info plus agent-specific file contents
                context = base_context.copy()
                context["assigned_files"] = agent_files
                context["file_contents"] = agent_file_contents
                
                # Format the prompt for this agent
                custom_prompt = self._format_agent_prompt(
                    {"name": agent.name, "description": agent.role},
                    context
                )
                
                # Don't override the template, pass the formatted prompt directly to the context
                # This avoids the issue of the agent trying to format an already formatted string
                context["formatted_prompt"] = custom_prompt
            else:
                # If no assignments were found, use all files
                all_files = [f for agent_def in agent_definitions for f in agent_def.get("file_assignments", [])]
                file_contents = get_filtered_formatted_contents(project_dir, all_files)
                
                # Create context with base info plus all file contents
                context = base_context.copy()
                context["assigned_files"] = all_files
                context["file_contents"] = file_contents
            
            # Add to list of contexts and create the agent task
            agent_contexts.append(context)
            agent_tasks.append(agent.analyze(context))
        
        # Run all agent tasks concurrently
        results = await asyncio.gather(*agent_tasks)
        
        # ====================================================
        # Process and Return Results
        # This section processes the results from each agent and returns them.
        # ====================================================
        # Return the results with agent names and findings
        named_results = []
        for i, result in enumerate(results):
            agent_name = self.agents[i].name
            
            # Check if the result has an error
            if "error" in result:
                named_results.append({
                    "agent": agent_name,
                    "error": result["error"],
                    "findings": f"Error occurred during analysis: {result['error']}"
                })
            else:
                # Check if the result has findings
                findings = result.get("findings", "No findings provided")
                named_results.append({
                    "agent": agent_name,
                    "findings": findings
                })
        
        return {
            "phase": "Deep Analysis",
            "findings": named_results
        }
