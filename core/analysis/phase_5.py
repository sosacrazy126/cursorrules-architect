# core/analysis/phase_5.py
# =============================================================================
# Phase 5: Consolidation
# This file contains the code for Phase 5 of the project analysis, which
# consolidates the results from all previous phases into a single report.
# =============================================================================

# =============================================================================
# Import Statements
# These lines import necessary modules and functions for this phase.
# - json: For handling JSON data.
# - logging: For logging events and errors.
# - Dict: For type hinting dictionaries.
# - Anthropic: The Anthropic API client.
# - PHASE_5_PROMPT, format_phase5_prompt: Specific prompt and formatting
#   function for Phase 5 from the config.prompts module.
# =============================================================================
import json
import logging
from typing import Dict
from anthropic import Anthropic
from config.prompts.phase_5_prompts import PHASE_5_PROMPT, format_phase5_prompt

# =============================================================================
# Initialize the Anthropic Client and Logger
# This section initializes the Anthropic client for API calls and sets up
# logging to track the process.
# =============================================================================
anthropic_client = Anthropic()
logger = logging.getLogger("project_extractor")

# =============================================================================
# Phase 5 Analysis Class
# This class handles the consolidation of results from all previous phases.
# =============================================================================
class Phase5Analysis:
    """
    Class responsible for Phase 5 (Consolidation) of the project analysis.
    
    This phase uses Claude to consolidate the results from all previous phases
    into a comprehensive final report.
    """
    
    # =========================================================================
    # Initialization Method
    # Sets up the Phase 5 analysis with the specified Claude model.
    # =========================================================================
    def __init__(self, model: str = "claude-3-7-sonnet-20250219"):
        """
        Initialize the Phase 5 analysis with the specified Claude model.
        
        Args:
            model: The Claude model to use (default: "claude-3-7-sonnet-20250219")
        """
        self.model = model
    
    # =========================================================================
    # Run Method
    # Executes the consolidation phase, sending a request to the Anthropic API.
    # =========================================================================
    async def run(self, all_results: Dict) -> Dict:
        """
        Run the Consolidation Phase using Claude.
        
        Args:
            all_results: Dictionary containing the results from all previous phases
            
        Returns:
            Dictionary containing the consolidated report
        """
        try:
            # Format the prompt using the template from the prompts file
            prompt = format_phase5_prompt(all_results)
            
            # Send a request to the Anthropic Claude API to consolidate the
            # results from all previous phases into a final report.
            response = anthropic_client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Return the consolidated report.
            return {
                "phase": "Consolidation",
                "report": response.content[0].text
            }
        except Exception as e:
            logger.error(f"Error in Phase 5: {str(e)}")
            return {
                "phase": "Consolidation",
                "error": str(e)
            }
