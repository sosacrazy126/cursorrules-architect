"""
core/agents/openai.py

This module provides the OpenAIArchitect class for interacting with OpenAI models.
It handles the creation and execution of agent-based analysis using OpenAI models.

This module is used by the main analysis process to perform specialized analysis tasks.
"""

# ====================================================
# Importing Necessary Libraries
# This section imports all the required libraries and modules.
# These are external code packages that provide extra functions.
# ====================================================

import json
import logging
from typing import Dict, List, Optional
from openai import OpenAI
from core.agents.base import BaseArchitect, ModelProvider, ReasoningMode
from config.prompts.phase_2_prompts import PHASE_2_PROMPT, format_phase2_prompt
from config.prompts.phase_4_prompts import PHASE_4_PROMPT, format_phase4_prompt
from config.prompts.final_analysis_prompt import FINAL_ANALYSIS_PROMPT, format_final_analysis_prompt

# ====================================================
# Initialize OpenAI Client
# This section sets up the connection to the OpenAI API.
# It creates a client object that allows us to interact with OpenAI.
# ====================================================

# Initialize the OpenAI client as None first - will be initialized when needed
openai_client = None

# ====================================================
# Setup Logger
# This part sets up a logger to track and record events.
# It helps in debugging and monitoring the application.
# ====================================================

# Get logger
logger = logging.getLogger("project_extractor")

# ====================================================
# Define the OpenAIArchitect Class
# This section defines a class called OpenAIArchitect.
# A class is like a blueprint for creating objects that have specific functions and data.
# ====================================================

class OpenAIArchitect(BaseArchitect):
    """
    Architect class for interacting with OpenAI models.
    
    This class provides a structured way to create specialized architects that use
    OpenAI models for different analysis tasks.
    """
    
    # ====================================================
    # Initialization Function (__init__)
    # This function is called when a new OpenAIArchitect object is created.
    # It sets the initial state of the architect.
    # ====================================================
    def __init__(
        self,
        model_name: str = "o1",
        reasoning: ReasoningMode = None,
        temperature: Optional[float] = None,
        name: Optional[str] = None,
        role: Optional[str] = None,
        responsibilities: Optional[List[str]] = None,
        prompt_template: Optional[str] = None
    ):
        """
        Initialize an OpenAI architect with a specific model.
        
        Args:
            model_name: The OpenAI model to use (default: "o1")
            reasoning: Reasoning mode (defaults based on model type)
            temperature: Temperature value for temperature-based models like GPT-4o
            name: Optional name for specialized roles
            role: Optional role description
            responsibilities: Optional list of responsibilities
            prompt_template: Optional custom prompt template to use
        """
        # Set default reasoning based on model
        if reasoning is None:
            if model_name in ["o1", "o3-mini"]:
                reasoning = ReasoningMode.HIGH
            elif model_name == "gpt-4o":
                reasoning = ReasoningMode.TEMPERATURE
            else:
                reasoning = ReasoningMode.DISABLED
        
        # Set default temperature for GPT-4o if not specified
        if model_name == "gpt-4o" and temperature is None and reasoning == ReasoningMode.TEMPERATURE:
            temperature = 0.7  # Default temperature for GPT-4o
        
        super().__init__(
            provider=ModelProvider.OPENAI,
            model_name=model_name,
            reasoning=reasoning,
            temperature=temperature,
            name=name,
            role=role,
            responsibilities=responsibilities
        )
        
        # Store the prompt template
        self.prompt_template = prompt_template or self._get_default_prompt_template()
    
    def _get_default_prompt_template(self) -> str:
        """Get the default prompt template for the agent."""
        return """You are {agent_name}, responsible for {agent_role}.
        
Your specific responsibilities are:
{agent_responsibilities}

Analyze this project context and provide a detailed report focused on your domain:

{context}

Format your response as a structured report with clear sections and findings."""
    
    def format_prompt(self, context: Dict) -> str:
        """
        Format the prompt template with the agent's information and context.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Formatted prompt string
        """
        responsibilities_str = "\n".join(f"- {r}" for r in self.responsibilities) if self.responsibilities else ""
        context_str = json.dumps(context, indent=2) if isinstance(context, dict) else str(context)
        
        return self.prompt_template.format(
            agent_name=self.name or "OpenAI Architect",
            agent_role=self.role or "analyzing the project",
            agent_responsibilities=responsibilities_str,
            context=context_str
        )
    
    # ====================================================
    # Helper Methods
    # These methods help with common tasks needed by the public methods.
    # ====================================================
    
    def _get_model_parameters(self, content: str) -> Dict:
        """
        Get the appropriate model parameters based on model and reasoning mode.
        
        Args:
            content: The prompt content to send to the model
            
        Returns:
            Dictionary of model parameters
        """
        # Start with base parameters
        params = {
            "model": self.model_name,
            "messages": [{
                "role": "user",
                "content": content
            }]
        }
        
        # Add reasoning parameters based on model and mode
        if self.model_name in ["o1", "o3-mini"]:
            # For O1 and O3-Mini models, use reasoning_effort parameter
            if self.reasoning in [ReasoningMode.LOW, ReasoningMode.MEDIUM, ReasoningMode.HIGH]:
                # Use the value directly from the enum
                params["reasoning_effort"] = self.reasoning.value
            elif self.reasoning == ReasoningMode.ENABLED:
                # If using general ENABLED mode, default to HIGH
                params["reasoning_effort"] = "high"
            else:
                # Default to MEDIUM if not specified or using DISABLED
                params["reasoning_effort"] = "medium"
        elif self.model_name == "gpt-4o" or self.reasoning == ReasoningMode.TEMPERATURE:
            # For temperature-based models like GPT-4o
            if self.temperature is not None:
                params["temperature"] = self.temperature
        
        return params
    
    # ====================================================
    # Analyze Method
    # This method implements the abstract analyze method from BaseArchitect.
    # ====================================================
    
    async def analyze(self, context: Dict) -> Dict:
        """
        Run analysis using the OpenAI model.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Dictionary containing the analysis results or error information
        """
        try:
            # Initialize OpenAI client when needed
            global openai_client
            if openai_client is None:
                openai_client = OpenAI()
                logger.info("Initialized OpenAI client from OpenAIArchitect.analyze")
            
            # Check if the context already contains a formatted prompt
            if "formatted_prompt" in context:
                content = context["formatted_prompt"]
            else:
                # Format the prompt using the template
                content = self.format_prompt(context)
            
            # Get model parameters
            params = self._get_model_parameters(content)
            
            # Try to get the model config name
            from core.utils.tools.model_config_helper import get_model_config_name
            model_config_name = get_model_config_name(self)
            
            agent_name = self.name or "OpenAI Architect"
            logger.info(f"[bold blue]{agent_name}:[/bold blue] Sending request to {self.model_name} (Config: {model_config_name})")
            
            # Call the OpenAI API
            response = openai_client.chat.completions.create(**params)
            
            logger.info(f"[bold green]{agent_name}:[/bold green] Received response from {self.model_name}")
            
            return {
                "agent": agent_name,
                "findings": response.choices[0].message.content
            }
        except Exception as e:
            agent_name = self.name or "OpenAI Architect"
            logger.error(f"[bold red]Error in {agent_name}:[/bold red] {str(e)}")
            return {
                "agent": agent_name,
                "error": str(e)
            }
    
    # ------------------------------------
    # Phase 2: Analysis Planning
    # ------------------------------------
    async def create_analysis_plan(self, phase1_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Create an analysis plan based on Phase 1 results.
        
        Args:
            phase1_results: Dictionary containing the results from Phase 1
            prompt: Optional custom prompt to use instead of the default
            
        Returns:
            Dictionary containing the analysis plan
        """
        try:
            # Initialize OpenAI client when needed
            global openai_client
            if openai_client is None:
                openai_client = OpenAI()
                logger.info("Initialized OpenAI client from OpenAIArchitect.create_analysis_plan")
            
            # Use the provided prompt or the default one
            content = prompt if prompt else format_phase2_prompt(phase1_results)
            
            # Get model parameters
            params = self._get_model_parameters(content)
            
            # Call the OpenAI API
            response = openai_client.chat.completions.create(**params)

            return {
                "plan": response.choices[0].message.content
            }
        except Exception as e:
            logger.error(f"Error in analysis plan creation: {str(e)}")
            return {
                "error": str(e)
            }
    
    # ---------------------------------------
    # Phase 4: Findings Synthesis
    # ---------------------------------------
    async def synthesize_findings(self, phase3_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Synthesize findings from Phase 3.
        
        Args:
            phase3_results: Dictionary containing the results from Phase 3
            prompt: Optional custom prompt to use instead of the default
            
        Returns:
            Dictionary containing the synthesis
        """
        try:
            # Initialize OpenAI client when needed
            global openai_client
            if openai_client is None:
                openai_client = OpenAI()
                logger.info("Initialized OpenAI client from OpenAIArchitect.synthesize_findings")
            
            # Use the provided prompt or the default one
            content = prompt if prompt else format_phase4_prompt(phase3_results)
            
            # Get model parameters
            params = self._get_model_parameters(content)
            
            # Call the OpenAI API
            response = openai_client.chat.completions.create(**params)

            return {
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            logger.error(f"Error in findings synthesis: {str(e)}")
            return {
                "error": str(e)
            }
    
    # -----------------------------------
    # Final Analysis
    # -----------------------------------
    async def final_analysis(self, consolidated_report: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Perform final analysis on the consolidated report.
        
        Args:
            consolidated_report: Dictionary containing the consolidated report
            prompt: Optional custom prompt to use instead of the default
            
        Returns:
            Dictionary containing the final analysis
        """
        try:
            # Initialize OpenAI client when needed
            global openai_client
            if openai_client is None:
                openai_client = OpenAI()
                logger.info("Initialized OpenAI client from OpenAIArchitect.final_analysis")
            
            # Use the provided prompt or the default one
            content = prompt if prompt else format_final_analysis_prompt(consolidated_report)
            
            # Get model parameters
            params = self._get_model_parameters(content)
            
            # Call the OpenAI API
            response = openai_client.chat.completions.create(**params)

            return {
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            logger.error(f"Error in final analysis: {str(e)}")
            return {
                "error": str(e)
            }
    
    # -----------------------------------
    # Consolidate Results - Implemented for compatibility
    # -----------------------------------
    async def consolidate_results(self, all_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Consolidate results from all previous phases.
        
        This is implemented for compatibility with the base class but not the
        primary function of the OpenAI model in the current architecture.
        
        Args:
            all_results: Dictionary containing all phase results
            prompt: Optional custom prompt to use
            
        Returns:
            Dictionary containing the consolidated report
        """
        try:
            # Initialize OpenAI client when needed
            global openai_client
            if openai_client is None:
                openai_client = OpenAI()
                logger.info("Initialized OpenAI client from OpenAIArchitect.consolidate_results")
            
            # Use the provided prompt or format a default one
            content = prompt if prompt else f"Consolidate these results into a comprehensive report:\n\n{json.dumps(all_results, indent=2)}"
            
            # Get model parameters
            params = self._get_model_parameters(content)
            
            # Call the OpenAI API
            response = openai_client.chat.completions.create(**params)
            
            return {
                "phase": "Consolidation",
                "report": response.choices[0].message.content
            }
        except Exception as e:
            logger.error(f"Error in consolidation: {str(e)}")
            return {
                "phase": "Consolidation",
                "error": str(e)
            }

# ====================================================
# Legacy OpenAIAgent Class 
# Maintained for backward compatibility
# ====================================================

class OpenAIAgent:
    """
    Agent class for interacting with OpenAI models.
    
    This class provides a structured way to create specialized agents that use
    OpenAI models for different analysis tasks.
    
    Note: This class is maintained for backward compatibility. New code should use
    OpenAIArchitect instead.
    """
    
    def __init__(self, model: str = "o1", temperature: Optional[float] = None):
        """
        Initialize an OpenAI agent with a specific model.
        
        Args:
            model: The OpenAI model to use (default: "o1")
            temperature: Temperature value for temperature-based models like GPT-4o
        """
        self.model = model
        
        # Create underlying OpenAIArchitect with appropriate reasoning mode
        if model in ["o1", "o3-mini"]:
            self._architect = OpenAIArchitect(model_name=model, reasoning=ReasoningMode.HIGH)
        elif model == "gpt-4o":
            self._architect = OpenAIArchitect(model_name=model, reasoning=ReasoningMode.TEMPERATURE, temperature=temperature)
        else:
            self._architect = OpenAIArchitect(model_name=model)
        
        # Note: The OpenAI client will be initialized on-demand when needed in the architect methods
    
    async def create_analysis_plan(self, phase1_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Create an analysis plan based on Phase 1 results using o1 model.
        
        Args:
            phase1_results: Dictionary containing the results from Phase 1
            prompt: Optional custom prompt to use instead of the default
            
        Returns:
            Dictionary containing the analysis plan and token usage
        """
        return await self._architect.create_analysis_plan(phase1_results, prompt)
    
    async def synthesize_findings(self, phase3_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Synthesize findings from Phase 3 using o1 model.
        
        Args:
            phase3_results: Dictionary containing the results from Phase 3
            prompt: Optional custom prompt to use instead of the default
            
        Returns:
            Dictionary containing the synthesis and token usage
        """
        return await self._architect.synthesize_findings(phase3_results, prompt)
    
    async def final_analysis(self, consolidated_report: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Perform final analysis on the consolidated report using o1 model.
        
        Args:
            consolidated_report: Dictionary containing the consolidated report
            prompt: Optional custom prompt to use instead of the default
            
        Returns:
            Dictionary containing the final analysis and token usage
        """
        return await self._architect.final_analysis(consolidated_report, prompt)
