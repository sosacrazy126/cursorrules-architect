"""
core/analysis/phase_1.py

This module provides functionality for Phase 1 (Initial Discovery) of the project analysis.
It defines the agents and methods needed for the initial exploration of the project.
"""

# ====================================================
# Importing Required Libraries
# This section imports all the necessary libraries and modules needed for this phase.
# ====================================================

import asyncio  # For running asynchronous tasks concurrently.
import json     # For handling JSON data.
from typing import Dict, List  # For type hinting.
from core.agents.anthropic import AnthropicArchitect  # The AnthropicArchitect class for interacting with the Anthropic API.
from config.prompts.phase_1_prompts import ( # Prompts used for configuring the agents in Phase 1.
    PHASE_1_BASE_PROMPT,
    STRUCTURE_AGENT_PROMPT,
    DEPENDENCY_AGENT_PROMPT,
    TECH_STACK_AGENT_PROMPT,
)
from config.agents import get_architect_for_phase  # Function to get the appropriate architect for a phase
import logging  # For logging information about the execution
from rich import print

# ====================================================
# Phase 1 Analysis Class
# This class handles the initial discovery phase of the project analysis.
# ====================================================

class Phase1Analysis:
    """
    Class responsible for Phase 1 (Initial Discovery) of the project analysis.
    
    This phase uses Anthropic models to perform initial exploration of the project,
    analyzing directory structure, dependencies, and technology stack.
    """
    
    # ----------------------------------------------------
    # Initialization
    # Sets up the agents required for the initial discovery.
    # ----------------------------------------------------
    def __init__(self):
        """
        Initialize the Phase 1 analysis with the required architects.
        """
        # Use the Architect architecture
        self.architects = [
            get_architect_for_phase(
                "phase1",
                name=STRUCTURE_AGENT_PROMPT["name"],
                role=STRUCTURE_AGENT_PROMPT["role"],
                responsibilities=STRUCTURE_AGENT_PROMPT["responsibilities"],
                prompt_template=PHASE_1_BASE_PROMPT
            ),
            get_architect_for_phase(
                "phase1",
                name=DEPENDENCY_AGENT_PROMPT["name"],
                role=DEPENDENCY_AGENT_PROMPT["role"],
                responsibilities=DEPENDENCY_AGENT_PROMPT["responsibilities"],
                prompt_template=PHASE_1_BASE_PROMPT
            ),
            get_architect_for_phase(
                "phase1",
                name=TECH_STACK_AGENT_PROMPT["name"],
                role=TECH_STACK_AGENT_PROMPT["role"],
                responsibilities=TECH_STACK_AGENT_PROMPT["responsibilities"],
                prompt_template=PHASE_1_BASE_PROMPT
            )
        ]
    
    # ----------------------------------------------------
    # Run Method
    # Executes the Initial Discovery phase.
    # ----------------------------------------------------
    async def run(self, tree: List[str], package_info: Dict) -> Dict:
        """
        Run the Initial Discovery Phase.
        
        Args:
            tree: List of strings representing the project directory tree
            package_info: Dictionary containing information about project dependencies
            
        Returns:
            Dictionary containing the results of the phase
        """
        # Create a context object with the tree structure and package information.
        context = {
            "tree_structure": tree,
            "package_info": package_info
        }
        
        logging.info("[bold]Phase 1:[/bold] Starting analysis with 3 agents")
        
        # Use the Architect architecture - create a dictionary to map each architect to its index
        architect_indices = {architect: i for i, architect in enumerate(self.architects)}
        
        # Run each architect in parallel with its own context
        async def run_architect_with_logging(architect, ctx):
            agent_num = architect_indices[architect] + 1
            logging.info(f"[bold cyan]Agent {agent_num}:[/bold cyan] {architect.name} starting analysis")
            result = await architect.analyze(ctx)
            logging.info(f"[bold green]Agent {agent_num}:[/bold green] {architect.name} completed analysis")
            return result
        
        architect_tasks = [run_architect_with_logging(architect, context) for architect in self.architects]
        results = await asyncio.gather(*architect_tasks)
        
        logging.info("[bold green]Phase 1:[/bold green] All agents have completed their analysis")
        
        # Return the results with phase information.
        return {
            "phase": "Initial Discovery",
            "findings": results
        }
