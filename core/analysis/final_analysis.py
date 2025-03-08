"""
core/analysis/final_analysis.py

This module provides functionality for the Final Analysis phase of the project analysis.
It defines the methods needed for performing the final analysis on the consolidated report.
"""

# ====================================================
# Importing Required Libraries
# This section imports all the necessary libraries and modules needed for this phase.
# ====================================================

import logging  # Used for logging events and errors.
from typing import Dict, List  # Used for type hinting.
from core.agents.openai import OpenAIAgent  # Custom class for interacting with OpenAI models.
from config.prompts.final_analysis_prompt import format_final_analysis_prompt  # Function to format the final analysis prompt.

# ====================================================
# Logger Setup
# This section sets up the logger for the module.
# ====================================================

# Get logger
logger = logging.getLogger("project_extractor")

# ====================================================
# Final Analysis Class
# This class handles the final analysis phase (Phase 6) of the project.
# It uses AI agents to analyze the consolidated report and provide insights.
# ====================================================

class FinalAnalysis:
    """
    Class responsible for the Final Analysis phase of the project analysis.
    
    This phase uses OpenAI's o1 model to perform a final analysis on the
    consolidated report from Phase 5, providing architectural patterns,
    system structure mapping, and improvement recommendations.
    """
    
    # ====================================================
    # Initialization (__init__)
    # This method sets up the initial state of the FinalAnalysis class.
    # ====================================================
    
    def __init__(self, model: str = "o1"):
        """
        Initialize the Final Analysis with the required OpenAI agent.
        
        Args:
            model: The OpenAI model to use (default: "o1")
        """
        self.openai_agent = OpenAIAgent(model=model)  # Create an instance of the OpenAIAgent.
    
    # ====================================================
    # Run Method
    # This method executes the final analysis phase.
    # ====================================================
    
    async def run(self, consolidated_report: Dict, project_structure: List[str] = None) -> Dict:
        """
        Run the Final Analysis Phase using o1.
        
        Args:
            consolidated_report: Dictionary containing the consolidated report from Phase 5.
            project_structure: List of strings representing the project directory tree.
            
        Returns:
            Dictionary containing the final analysis and token usage.
        """
        try:
            # Format the prompt using the template from the prompts file.
            prompt = format_final_analysis_prompt(consolidated_report, project_structure)
            
            # Use the OpenAIAgent to perform the final analysis with the formatted prompt.
            return await self.openai_agent.final_analysis(consolidated_report, prompt)
        except Exception as e:
            # Log any errors that occur during the analysis.
            logger.error(f"Error in Final Analysis: {str(e)}")
            return {"error": str(e)}  # Return the error message.
