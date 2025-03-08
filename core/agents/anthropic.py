"""
core/agents/anthropic.py

This module provides the AnthropicArchitect class for interacting with Anthropic's Claude models.
It handles the creation and execution of agent-based analysis using Claude models.

This module is used by the main analysis process to perform specialized analysis tasks.
"""

# ====================================================
# Importing Required Libraries
# This section imports all the necessary libraries needed for the script.
# ====================================================

import json  # Used for handling JSON data
import logging  # Used for logging events and errors
from typing import Dict, List, Any, Optional  # Used for type hinting
from anthropic import Anthropic  # The Anthropic API client
from core.agents.base import BaseArchitect, ModelProvider, ReasoningMode  # Import the base class

# ====================================================
# Initialize the Anthropic Client
# This section initializes the client for interacting with the Anthropic API.
# ====================================================

# Initialize the Anthropic client
anthropic_client = Anthropic()

# ====================================================
# Get Logger
# Set up logger to track events and issues.
# ====================================================

# Get logger
logger = logging.getLogger("project_extractor")

# ====================================================
# AnthropicArchitect Class Definition
# This class implements the BaseArchitect for Anthropic's Claude models.
# ====================================================

class AnthropicArchitect(BaseArchitect):
    """
    Architect class for interacting with Anthropic's Claude models.
    
    This class provides a structured way to create specialized agents that use
    Claude models for different analysis tasks.
    """
    
    # ====================================================
    # Initialization Function (__init__)
    # This function sets up the new AnthropicArchitect object when it's created.
    # ====================================================
    
    def __init__(
        self, 
        model_name: str = "claude-3-7-sonnet-20250219",
        reasoning: ReasoningMode = ReasoningMode.DISABLED,
        name: Optional[str] = None,
        role: Optional[str] = None,
        responsibilities: Optional[List[str]] = None,
        prompt_template: Optional[str] = None
    ):
        """
        Initialize an Anthropic architect with specific configurations.
        
        Args:
            model_name: The Anthropic model to use
            reasoning: Whether to enable reasoning mode
            name: Optional name for specialized roles
            role: Optional role description
            responsibilities: Optional list of responsibilities
            prompt_template: Optional custom prompt template
        """
        super().__init__(
            provider=ModelProvider.ANTHROPIC,
            model_name=model_name,
            reasoning=reasoning,
            name=name,
            role=role,
            responsibilities=responsibilities
        )
        self.prompt_template = prompt_template or self._get_default_prompt_template()
    
    # ====================================================
    # Default Prompt Template Function (_get_default_prompt_template)
    # This function returns the default prompt template for the agent.
    # ====================================================
    
    def _get_default_prompt_template(self) -> str:
        """Get the default prompt template for the agent."""
        return """You are the {agent_name}, responsible for {agent_role}.
        
        Your specific responsibilities are:
        {agent_responsibilities}
        
        Analyze this project context and provide a detailed report focused on your domain:
        
        {context}
        
        Format your response as a structured report with clear sections and findings."""
    
    # ====================================================
    # Prompt Formatting Function (format_prompt)
    # This function formats the prompt with specific agent information and context.
    # ====================================================
    
    def format_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format the prompt template with the agent's information and context.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Formatted prompt string
        """
        responsibilities_str = "\n".join(f"- {r}" for r in self.responsibilities)
        context_str = json.dumps(context, indent=2)
        
        return self.prompt_template.format(
            agent_name=self.name or "Claude Architect",
            agent_role=self.role or "analyzing the project",
            agent_responsibilities=responsibilities_str,
            context=context_str
        )

    # ====================================================
    # Analysis Function (analyze)
    # This function sends a request to the Anthropic API and processes the response.
    # ====================================================

    async def analyze(self, context: Dict) -> Dict:
        """
        Run agent analysis using Claude model.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Dictionary containing the agent's findings or error information
        """
        try:
            # Check if the context already contains a formatted prompt
            if "formatted_prompt" in context:
                prompt = context["formatted_prompt"]
            else:
                # Format the prompt using the template
                prompt = self.format_prompt(context)
            
            # Configure model parameters based on reasoning mode
            params = {
                "model": self.model_name,
                "max_tokens": 4000,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            }
            
            # Add thinking parameter if reasoning is enabled
            if self.reasoning == ReasoningMode.ENABLED:
                params["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": 16000
                }
            
            # Send a request to the Anthropic Claude API to analyze the given context.
            response = anthropic_client.messages.create(**params)
            
            # Return the agent's findings.
            return {
                "agent": self.name or "Claude Architect",
                "findings": response.content[0].text
            }
        except Exception as e:
            logger.error(f"Error in {self.name or 'Claude Architect'} analysis: {str(e)}")
            # Return an error message if something goes wrong.
            return {
                "agent": self.name or "Claude Architect",
                "error": str(e)
            }
    
    # ====================================================
    # Create Analysis Plan - Not primary function but implemented for compatibility
    # ====================================================
    async def create_analysis_plan(self, phase1_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Create an analysis plan based on Phase 1 results.
        
        This is implemented for compatibility with the base class but not the
        primary function of the Anthropic model in the current architecture.
        
        Args:
            phase1_results: Dictionary containing the results from Phase 1
            prompt: Optional custom prompt to use
            
        Returns:
            Dictionary containing the analysis plan
        """
        context = {"phase1_results": phase1_results, "formatted_prompt": prompt} if prompt else {"phase1_results": phase1_results}
        result = await self.analyze(context)
        
        return {
            "plan": result.get("findings", "No plan generated"),
            "error": result.get("error", None)
        }
    
    # ====================================================
    # Synthesize Findings - Not primary function but implemented for compatibility
    # ====================================================
    async def synthesize_findings(self, phase3_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Synthesize findings from Phase 3.
        
        This is implemented for compatibility with the base class but not the
        primary function of the Anthropic model in the current architecture.
        
        Args:
            phase3_results: Dictionary containing the results from Phase 3
            prompt: Optional custom prompt to use
            
        Returns:
            Dictionary containing the synthesis
        """
        context = {"phase3_results": phase3_results, "formatted_prompt": prompt} if prompt else {"phase3_results": phase3_results}
        result = await self.analyze(context)
        
        return {
            "analysis": result.get("findings", "No synthesis generated"),
            "error": result.get("error", None)
        }
    
    # ====================================================
    # Final Analysis - Not primary function but implemented for compatibility
    # ====================================================
    async def final_analysis(self, consolidated_report: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Perform final analysis on the consolidated report.
        
        This is implemented for compatibility with the base class but not the
        primary function of the Anthropic model in the current architecture.
        
        Args:
            consolidated_report: Dictionary containing the consolidated report
            prompt: Optional custom prompt to use
            
        Returns:
            Dictionary containing the final analysis
        """
        context = {"consolidated_report": consolidated_report, "formatted_prompt": prompt} if prompt else {"consolidated_report": consolidated_report}
        result = await self.analyze(context)
        
        return {
            "analysis": result.get("findings", "No final analysis generated"),
            "error": result.get("error", None)
        }
    
    # ====================================================
    # Consolidate Results - Primary method for Phase 5
    # ====================================================
    async def consolidate_results(self, all_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Consolidate results from all previous phases.
        
        Args:
            all_results: Dictionary containing all phase results
            prompt: Optional custom prompt to use
            
        Returns:
            Dictionary containing the consolidated report
        """
        try:
            # Use the provided prompt or format a default one
            content = prompt if prompt else f"Consolidate these results into a comprehensive report:\n\n{json.dumps(all_results, indent=2)}"
            
            # Configure model parameters based on reasoning mode
            params = {
                "model": self.model_name,
                "max_tokens": 4000,
                "messages": [{
                    "role": "user",
                    "content": content
                }]
            }
            
            # Add thinking parameter if reasoning is enabled
            if self.reasoning == ReasoningMode.ENABLED:
                params["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": 16000
                }
            
            # Send a request to the Anthropic Claude API
            response = anthropic_client.messages.create(**params)
            
            # Return the consolidated report
            return {
                "phase": "Consolidation",
                "report": response.content[0].text
            }
        except Exception as e:
            logger.error(f"Error in consolidation: {str(e)}")
            return {
                "phase": "Consolidation",
                "error": str(e)
            }

# ====================================================
# Legacy ClaudeAgent Class 
# Maintained for backward compatibility
# ====================================================

class ClaudeAgent:
    """
    Agent class for interacting with Anthropic's Claude models.
    
    This class provides a structured way to create specialized agents that use
    Claude models for different analysis tasks.
    
    Note: This class is maintained for backward compatibility. New code should use
    AnthropicArchitect instead.
    """
    
    def __init__(self, name: str, role: str, responsibilities: List[str], prompt_template: str = None):
        """
        Initialize a Claude agent with a specific name, role, and responsibilities.
        
        Args:
            name: The name of the agent (e.g., "Structure Agent")
            role: The role of the agent (e.g., "analyzing directory and file organization")
            responsibilities: A list of specific tasks the agent is responsible for
            prompt_template: Optional custom prompt template to use instead of the default
        """
        self.name = name
        self.role = role
        self.responsibilities = responsibilities
        
        # Store the provided prompt template first
        self._provided_prompt_template = prompt_template
        
        # Create underlying AnthropicArchitect
        self._architect = AnthropicArchitect(
            name=name,
            role=role,
            responsibilities=responsibilities,
            prompt_template=prompt_template
        )
        
        # Now initialize the prompt_template properly
        self.prompt_template = prompt_template or self._get_default_prompt_template()
    
    def _get_default_prompt_template(self) -> str:
        """Get the default prompt template for the agent."""
        # Always delegate to the architect to get the default template
        return self._architect._get_default_prompt_template()
    
    def format_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format the prompt template with the agent's information and context.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Formatted prompt string
        """
        return self._architect.format_prompt(context)

    async def analyze(self, context: Dict) -> Dict:
        """
        Run agent analysis using Claude-3-7-sonnet model.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Dictionary containing the agent's findings or error information
        """
        return await self._architect.analyze(context)
