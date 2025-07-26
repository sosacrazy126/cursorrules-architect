"""
core/agents/gemini.py

This module provides the GeminiArchitect class for interacting with Google's Gemini models.
It handles the creation and execution of agent-based analysis using Gemini models.

This module is used by the main analysis process to perform specialized analysis tasks.
"""

# ====================================================
# Importing Required Libraries
# This section imports all the necessary libraries needed for the script.
# ====================================================

import json  # Used for handling JSON data
import logging  # Used for logging events and errors
import asyncio  # For async operations
import os  # For accessing environment variables
import random  # For exponential backoff jitter
from typing import Dict, List, Any, Optional  # Used for type hinting
from google import genai  # The Google Gemini API client
from google.genai import types  # Types for Gemini API configuration
from ...core.agents.base import BaseArchitect, ModelProvider, ReasoningMode  # Import the base class

# ====================================================
# Initialize the Gemini Client
# This section initializes the client for interacting with the Gemini API.
# ====================================================

# Initialize the Gemini client (actual initialization will happen when API key is available)
gemini_client = None

# ====================================================
# Get Logger
# Set up logger to track events and issues.
# ====================================================

# Get logger
logger = logging.getLogger("project_extractor")

# ====================================================
# GeminiArchitect Class Definition
# This class implements the BaseArchitect for Google's Gemini models.
# ====================================================

class GeminiArchitect(BaseArchitect):
    """
    Architect class for interacting with Google's Gemini models.
    
    This class provides a structured way to create specialized agents that use
    Gemini models for different analysis tasks.
    """
    
    # ====================================================
    # Initialization Function (__init__)
    # This function sets up the new GeminiArchitect object when it's created.
    # ====================================================
    
    def __init__(
        self, 
        model_name: str = "gemini-2.0-flash",
        reasoning: ReasoningMode = ReasoningMode.DISABLED,
        name: Optional[str] = None,
        role: Optional[str] = None,
        responsibilities: Optional[List[str]] = None,
        prompt_template: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize a Gemini architect with specific configurations.
        
        Args:
            model_name: The Gemini model to use
            reasoning: Whether to enable thinking models
            name: Optional name for specialized roles
            role: Optional role description
            responsibilities: Optional list of responsibilities
            prompt_template: Optional custom prompt template
            api_key: Optional API key for Gemini
        """
        super().__init__(
            provider=ModelProvider.GEMINI,
            model_name=model_name,
            reasoning=reasoning,
            name=name,
            role=role,
            responsibilities=responsibilities
        )
        self.prompt_template = prompt_template or self._get_default_prompt_template()
        
        # Try to get the API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
        
        # Initialize the Gemini client if not already initialized
        global gemini_client
        if gemini_client is None and api_key:
            gemini_client = genai.Client(api_key=api_key)
        self.gemini_client = gemini_client
    
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
            agent_name=self.name or "Gemini Architect",
            agent_role=self.role or "analyzing the project",
            agent_responsibilities=responsibilities_str,
            context=context_str
        )

    # ====================================================
    # Analysis Function (analyze)
    # This function sends a request to the Gemini API and processes the response.
    # ====================================================

    async def analyze(self, context: Dict) -> Dict:
        """
        Run agent analysis using Gemini model.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Dictionary containing the agent's findings or error information
        """
        try:
            if not self.gemini_client:
                raise ValueError("Gemini client not initialized. Please provide an API key.")
                
            # Check if the context already contains a formatted prompt
            if "formatted_prompt" in context:
                prompt = context["formatted_prompt"]
            else:
                # Format the prompt using the template
                prompt = self.format_prompt(context)
            
            # Configure model parameters based on model and reasoning mode
            model = self.model_name
            
            # Check if we should use a thinking model
            if self.reasoning == ReasoningMode.ENABLED:
                # Use the thinking variant of the selected model
                if "gemini-2.0-flash" in model:
                    model = "gemini-2.0-flash-thinking-exp"
                elif "gemini-2.5-pro" in model:
                    model = "gemini-2.5-pro-exp-03-25"
            
            # Determine if we need to use a system instruction
            system_instruction = None
            if self.role:
                system_instruction = f"You are {self.name or 'an AI assistant'}, responsible for {self.role}."
            
            # Create the generation config
            config = None
            if system_instruction:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            
            # Get the model configuration name
            from core.utils.tools.model_config_helper import get_model_config_name
            model_config_name = get_model_config_name(self)
            
            agent_name = self.name or "Gemini Architect"
            logger.info(f"[bold green]{agent_name}:[/bold green] Sending request to {model} (Config: {model_config_name})" + 
                       (" with thinking" if self.reasoning == ReasoningMode.ENABLED else ""))
            
            # Send a request to the Gemini API with retry logic
            response = await self._make_api_call_with_retry(
                model=model,
                contents=[prompt],
                config=config
            )
            
            logger.info(f"[bold green]{agent_name}:[/bold green] Received response from {model}")
            
            # Return the agent's findings.
            return {
                "agent": agent_name,
                "findings": response.text
            }
        except Exception as e:
            agent_name = self.name or "Gemini Architect"
            logger.error(f"[bold red]Error in {agent_name}:[/bold red] {str(e)}")
            # Return an error message if something goes wrong.
            return {
                "agent": agent_name,
                "error": str(e)
            }
    
    # ====================================================
    # Create Analysis Plan - Not primary function but implemented for compatibility
    # ====================================================
    async def create_analysis_plan(self, phase1_results: Dict, prompt: Optional[str] = None) -> Dict:
        """
        Create an analysis plan based on Phase 1 results.
        
        This is implemented for compatibility with the base class but not the
        primary function of the Gemini model in the current architecture.
        
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
        primary function of the Gemini model in the current architecture.
        
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
        primary function of the Gemini model in the current architecture.
        
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
    # Retry Logic with Exponential Backoff
    # ====================================================
    
    async def _make_api_call_with_retry(
        self, 
        model: str, 
        contents: List[str], 
        config: Optional[types.GenerateContentConfig],
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        """
        Make API call with exponential backoff retry logic.
        
        Args:
            model: The model to use
            contents: The content to send
            config: Optional configuration
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            
        Returns:
            API response
            
        Raises:
            Exception: If all retries are exhausted
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                # Make the API call
                if config:
                    response = self.gemini_client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config
                    )
                else:
                    response = self.gemini_client.models.generate_content(
                        model=model,
                        contents=contents
                    )
                return response
                
            except Exception as e:
                last_exception = e
                agent_name = self.name or "Gemini Architect"
                
                # Log the attempt
                if attempt < max_retries:
                    logger.warning(f"[bold yellow]{agent_name}:[/bold yellow] API call failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
                    
                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jittered_delay = delay * (0.5 + random.random() * 0.5)  # Add 50% jitter
                    
                    logger.info(f"[bold cyan]{agent_name}:[/bold cyan] Retrying in {jittered_delay:.1f} seconds...")
                    await asyncio.sleep(jittered_delay)
                else:
                    logger.error(f"[bold red]{agent_name}:[/bold red] All {max_retries + 1} attempts failed. Last error: {str(e)}")
        
        # If we get here, all retries have been exhausted
        raise last_exception
    
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
            
            # Configure model parameters
            model = self.model_name
            
            # Check if we should use a thinking model
            if self.reasoning == ReasoningMode.ENABLED:
                # Use the thinking variant of the selected model
                if "gemini-2.0-flash" in model:
                    model = "gemini-2.0-flash-thinking-exp"
                elif "gemini-2.5-pro" in model:
                    model = "gemini-2.5-pro-exp-03-25"
            
            # Send a request to the Gemini API with retry logic
            response = await self._make_api_call_with_retry(
                model=model,
                contents=[content],
                config=None
            )
            
            # Return the consolidated report
            return {
                "phase": "Consolidation",
                "report": response.text
            }
        except Exception as e:
            logger.error(f"Error in consolidation: {str(e)}")
            return {
                "phase": "Consolidation",
                "error": str(e)
            }

# ====================================================
# Legacy GeminiAgent Class 
# Maintained for backward compatibility
# ====================================================

class GeminiAgent:
    """
    Agent class for interacting with Google's Gemini models.
    
    This class provides a structured way to create specialized agents that use
    Gemini models for different analysis tasks.
    
    Note: This class is maintained for backward compatibility. New code should use
    GeminiArchitect instead.
    """
    
    def __init__(self, name: str, role: str, responsibilities: List[str], prompt_template: str = None, api_key: str = None):
        """
        Initialize a Gemini agent with a specific name, role, and responsibilities.
        
        Args:
            name: The name of the agent (e.g., "Structure Agent")
            role: The role of the agent (e.g., "analyzing directory and file organization")
            responsibilities: A list of specific tasks the agent is responsible for
            prompt_template: Optional custom prompt template to use instead of the default
            api_key: Optional API key for Gemini
        """
        self.name = name
        self.role = role
        self.responsibilities = responsibilities
        
        # Store the provided prompt template first
        self._provided_prompt_template = prompt_template
        
        # Create underlying GeminiArchitect
        self._architect = GeminiArchitect(
            name=name,
            role=role,
            responsibilities=responsibilities,
            prompt_template=prompt_template,
            api_key=api_key
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
        Run agent analysis using Gemini model.
        
        Args:
            context: Dictionary containing the context for analysis
            
        Returns:
            Dictionary containing the agent's findings or error information
        """
        return await self._architect.analyze(context)
