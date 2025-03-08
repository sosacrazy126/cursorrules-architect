# core/analysis/phase_4.py
"""
This module provides functionality for Phase 4 (Synthesis) of the project analysis.
It defines the methods needed for synthesizing the findings from Phase 3.
"""

# ====================================================
# Import Statements
# This section imports necessary modules and functions for the script.
# ====================================================

import logging  # Used for logging messages
from typing import Dict  # Used for type hinting, making code more readable
from core.agents.openai import OpenAIAgent  # The OpenAI agent class
from config.prompts.phase_4_prompts import PHASE_4_PROMPT, format_phase4_prompt  # Prompts for Phase 4

# ====================================================
# Logger Initialization
# Get the logger for this module.
# ====================================================

# Get logger
logger = logging.getLogger("project_extractor")

# ====================================================
# Phase 4 Analysis Class
# This class handles the Phase 4 (Synthesis) of the project analysis.
# ====================================================

class Phase4Analysis:
    """
    Class responsible for Phase 4 (Synthesis) of the project analysis.
    
    This phase uses OpenAI's o1 model to synthesize the findings from Phase 3,
    providing a deeper analysis and updated directions.
    """
    
    # ====================================================
    # Initialization Method
    # Sets up the Phase 4 analysis with the OpenAI agent.
    # ====================================================
    def __init__(self, model: str = "o1"):
        """
        Initialize the Phase 4 analysis with the required OpenAI agent.
        
        Args:
            model: The OpenAI model to use (default: "o1")
        """
        self.openai_agent = OpenAIAgent(model=model)

    # ====================================================
    # Run Method
    # Executes the Synthesis Phase using the o1 model.
    # ====================================================
    async def run(self, phase3_results: Dict) -> Dict:
        """
        Run the Synthesis Phase using o1.
        
        Args:
            phase3_results: Dictionary containing the results from Phase 3
            
        Returns:
            Dictionary containing the synthesis and token usage
        """
        try:
            # Format the prompt using the template from the prompts file
            prompt = format_phase4_prompt(phase3_results)
            
            # Use the OpenAIAgent to synthesize findings from Phase 3
            return await self.openai_agent.synthesize_findings(phase3_results, prompt)
        except Exception as e:
            logger.error(f"Error in Phase 4: {str(e)}")
            return {"error": str(e)}
