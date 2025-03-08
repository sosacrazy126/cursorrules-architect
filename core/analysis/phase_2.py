# core/analysis/phase_2.py
"""
This module provides functionality for Phase 2 (Methodical Planning) of the project analysis.
It defines the methods needed for creating a detailed analysis plan based on Phase 1 results.
"""

# ====================================================
# Import Statements
# This section imports necessary modules and functions for the script.
# ====================================================

import logging  # Used for logging messages
from typing import Dict, List  # Used for type hinting, making code more readable
from core.agents.openai import OpenAIAgent  # The OpenAI agent class
from config.prompts.phase_2_prompts import PHASE_2_PROMPT, format_phase2_prompt  # Prompts for Phase 2
from core.utils.tools.agent_parser import parse_agents_from_phase2  # Function to parse agent definitions

# ====================================================
# Logger Initialization
# Get the logger for this module.
# ====================================================
logger = logging.getLogger("project_extractor")

# ====================================================
# Phase 2 Analysis Class
# This class handles the methodical planning phase.
# ====================================================

class Phase2Analysis:
    """
    Class responsible for Phase 2 (Methodical Planning) of the project analysis.
    
    This phase uses OpenAI's o1 model to create a detailed analysis plan based on
    the findings from Phase 1.
    """
    
    # ====================================================
    # Initialization
    # Sets up the Phase 2 analysis.
    # ====================================================
    def __init__(self, model: str = "o1"):
        """
        Initialize the Phase 2 analysis with the required OpenAI agent.
        
        Args:
            model: The OpenAI model to use (default: "o1")
        """
        self.openai_agent = OpenAIAgent(model=model)  # Create an instance of the OpenAI agent
    
    # ====================================================
    # Run Method
    # Executes the methodical planning phase.
    # ====================================================
    async def run(self, phase1_results: Dict, tree: List[str] = None) -> Dict:
        """
        Run the Methodical Planning Phase using o1.
        
        Args:
            phase1_results: Dictionary containing the results from Phase 1
            tree: List of strings representing the project directory tree
            
        Returns:
            Dictionary containing the analysis plan and token usage
        """
        try:
            # ====================================================
            # Prompt Formatting
            # Format the prompt using the template.
            # ====================================================
            prompt = format_phase2_prompt(phase1_results, tree)
            
            # ====================================================
            # Analysis Plan Creation
            # Use the OpenAIAgent to create an analysis plan.
            # ====================================================
            analysis_plan_response = await self.openai_agent.create_analysis_plan(phase1_results, prompt)
            
            # ====================================================
            # Error Handling
            # Check for errors and return if any.
            # ====================================================
            if "error" in analysis_plan_response:
                return analysis_plan_response
            
            # ====================================================
            # Plan Extraction and Agent Parsing
            # Get the plan and parse agent definitions.
            # ====================================================
            plan_text = analysis_plan_response.get("plan", "")  # Extract the raw plan text
            agents = parse_agents_from_phase2(plan_text)  # Parse the agent definitions
            analysis_plan_response["agents"] = agents  # Add the agents to the response
            
            return analysis_plan_response
        except Exception as e:
            logger.error(f"Error in Phase 2: {str(e)}")
            return {"error": str(e)}
