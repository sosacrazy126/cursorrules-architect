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
from ...core.agents.openai import OpenAIAgent  # Custom class for interacting with OpenAI models.
from ...config.prompts.final_analysis_prompt import format_final_analysis_prompt  # Function to format the final analysis prompt.
from ...config.agents import get_architect_for_phase  # Import for dynamic model configuration

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
    
    This phase uses a model configured in config/agents.py to perform a final analysis on the
    consolidated report from Phase 5, providing architectural patterns,
    system structure mapping, and improvement recommendations.
    """
    
    # ====================================================
    # Initialization (__init__)
    # This method sets up the initial state of the FinalAnalysis class.
    # ====================================================
    
    def __init__(self):
        """
        Initialize the Final Analysis with the architect from configuration.
        """
        # Use the factory function to get the appropriate architect based on configuration
        self.architect = get_architect_for_phase("final")
    
    # ====================================================
    # Run Method
    # This method executes the final analysis phase.
    # ====================================================
    
    async def run(self, consolidated_report: Dict, project_structure: List[str] = None) -> Dict:
        """
        Run the Final Analysis Phase using the configured model.
        
        Args:
            consolidated_report: Dictionary containing the consolidated report from Phase 5.
            project_structure: List of strings representing the project directory tree.
            
        Returns:
            Dictionary containing the final analysis and token usage.
        """
        try:
            # Format the prompt using the template from the prompts file.
            prompt = format_final_analysis_prompt(consolidated_report, project_structure)
            
            logger.info("[bold]Final Analysis:[/bold] Creating Cursor rules from consolidated report")
            
            # Use the architect to perform the final analysis with the formatted prompt.
            result = await self.architect.final_analysis(consolidated_report, prompt)
            
            logger.info("[bold green]Final Analysis:[/bold green] Rules creation completed successfully")
            
            return result
        except Exception as e:
            # Log any errors that occur during the analysis.
            logger.error(f"[bold red]Error in Final Analysis:[/bold red] {str(e)}")
            return {"error": str(e)}  # Return the error message.
