import os
import logging
from typing import Dict, Optional, List, Any
import json
import asyncio
from openai import OpenAI

# Import the base classes
from .base import BaseArchitect, ModelProvider, ReasoningMode

# Set up logging
logger = logging.getLogger(__name__)

# Placeholder for the DeepSeek client import
# In actual implementation, you would import the appropriate client
# import deepseek

class DeepSeekArchitect(BaseArchitect):
    """
    Architect class for interacting with DeepSeek's Reasoner model.
    
    This class implements the BaseArchitect abstract class to provide
    methods for using DeepSeek Reasoner model in the analysis pipeline.
    
    The DeepSeek Reasoner model uses an OpenAI-compatible API but with a different base_url
    and special handling for reasoning content.
    """
    
    def __init__(
        self, 
        model_name: str = "deepseek-reasoner",  # Only supports the reasoner model
        reasoning: ReasoningMode = ReasoningMode.ENABLED,  # Reasoning is always enabled
        temperature: Optional[float] = None,  # Temperature not supported for reasoner
        name: Optional[str] = None,
        role: Optional[str] = None,
        responsibilities: Optional[List[str]] = None,
        prompt_template: Optional[str] = None,
        base_url: str = "https://api.deepseek.com"
    ):
        """
        Initialize a DeepSeek architect.
        
        Args:
            model_name: Set to "deepseek-reasoner" (only option)
            reasoning: Always set to ENABLED (only option)
            temperature: Not supported for DeepSeek Reasoner
            name: Optional name of the architect 
            role: Optional role description
            responsibilities: Optional list of responsibilities
            prompt_template: Optional custom prompt template
            base_url: The base URL for the DeepSeek API
        """
        # Force model to be deepseek-reasoner with reasoning enabled
        model_name = "deepseek-reasoner"
        reasoning = ReasoningMode.ENABLED
        temperature = None
        
        super().__init__(
            provider=ModelProvider.DEEPSEEK,
            model_name=model_name,
            reasoning=reasoning,
            temperature=temperature,
            name=name,
            role=role,
            responsibilities=responsibilities
        )
        self.prompt_template = prompt_template or self._get_default_prompt_template()
        self.base_url = base_url
        
        # Setup DeepSeek client (using OpenAI SDK)
        self.client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url=self.base_url
        )

    def _get_default_prompt_template(self) -> str:
        """Get the default prompt template for DeepSeek Reasoner."""
        return """You are {agent_name}, a code architecture analyst with expertise in {agent_role}.

Your responsibilities:
{agent_responsibilities}

Please analyze the following context and provide a detailed analysis:

Context:
{context}

Provide your analysis in a structured format with clear sections and actionable insights.
"""

    def format_prompt(self, context: Dict[str, Any]) -> str:
        """Format the analysis prompt with the provided context."""
        responsibilities_text = "\n".join([f"- {r}" for r in self.responsibilities]) if self.responsibilities else "Analyzing code architecture and patterns"
        
        return self.prompt_template.format(
            agent_name=self.name or "DeepSeek Reasoner",
            agent_role=self.role or "code architecture analysis",
            agent_responsibilities=responsibilities_text,
            context=json.dumps(context, indent=2)
        )
    
    def _get_api_parameters(self, messages: List[Dict]) -> Dict:
        """
        Get the API parameters for DeepSeek Reasoner.
        
        Args:
            messages: The messages to send to the model
            
        Returns:
            Dictionary of API parameters
        """
        return {
            "model": "deepseek-reasoner",
            "messages": messages,
            "max_tokens": 4000  # Default max tokens for deepseek-reasoner
        }

    async def analyze(self, context: Dict) -> Dict:
        """
        Perform analysis on the provided context using DeepSeek Reasoner.
        
        Args:
            context: Dictionary containing the information to analyze
            
        Returns:
            Dictionary containing the analysis results and reasoning
        """
        try:
            content = self.format_prompt(context)
            
            # Create messages format
            messages = [{"role": "user", "content": content}]
            
            # Get API parameters
            params = self._get_api_parameters(messages)
            
            # Get the model configuration name
            from core.utils.tools.model_config_helper import get_model_config_name
            model_config_name = get_model_config_name(self)
            
            agent_name = self.name or "DeepSeek Reasoner"
            logger.info(f"[bold teal]{agent_name}:[/bold teal] Sending request to {self.model_name} (Config: {model_config_name})")
            
            # Call the DeepSeek API via OpenAI SDK
            response = self.client.chat.completions.create(**params)
            
            logger.info(f"[bold green]{agent_name}:[/bold green] Received response from {self.model_name}")
            
            # Extract reasoning content from deepseek-reasoner
            reasoning_content = response.choices[0].message.reasoning_content
            content = response.choices[0].message.content
            
            return {
                "agent": agent_name,
                "findings": content,
                "reasoning": reasoning_content
            }
        except Exception as e:
            agent_name = self.name or "DeepSeek Reasoner"
            logger.error(f"[bold red]Error in {agent_name}:[/bold red] {str(e)}")
            return {
                "agent": agent_name,
                "error": str(e)
            }
    
    # Phase-specific methods
    async def create_analysis_plan(self, phase1_results: Dict, prompt: Optional[str] = None) -> Dict:
        """Create an analysis plan based on Phase 1 results."""
        try:
            # Use the provided prompt or generate one
            content = prompt if prompt else f"Create an analysis plan based on the Phase 1 results: {json.dumps(phase1_results, indent=2)}"
            
            # Create messages format
            messages = [{"role": "user", "content": content}]
            
            # Get API parameters
            params = self._get_api_parameters(messages)
            
            # Call the DeepSeek API
            response = self.client.chat.completions.create(**params)
            
            # Process response
            reasoning_content = response.choices[0].message.reasoning_content
            content = response.choices[0].message.content
            
            return {
                "agent": self.name or "DeepSeek Reasoner",
                "plan": content,
                "reasoning": reasoning_content
            }
        except Exception as e:
            logger.error(f"Error in create_analysis_plan: {str(e)}")
            return {
                "agent": self.name or "DeepSeek Reasoner",
                "error": str(e)
            }
    
    async def synthesize_findings(self, phase3_results: Dict, prompt: Optional[str] = None) -> Dict:
        """Synthesize findings from Phase 3."""
        try:
            # Similar implementation to create_analysis_plan
            content = prompt if prompt else f"Synthesize the findings from Phase 3: {json.dumps(phase3_results, indent=2)}"
            messages = [{"role": "user", "content": content}]
            params = self._get_api_parameters(messages)
            response = self.client.chat.completions.create(**params)
            
            return {
                "agent": self.name or "DeepSeek Reasoner",
                "analysis": response.choices[0].message.content,
                "reasoning": response.choices[0].message.reasoning_content
            }
        except Exception as e:
            logger.error(f"Error in synthesize_findings: {str(e)}")
            return {"agent": self.name or "DeepSeek Reasoner", "error": str(e)}
    
    async def final_analysis(self, consolidated_report: Dict, prompt: Optional[str] = None) -> Dict:
        """Provide final analysis on the consolidated report."""
        try:
            # Similar implementation pattern
            content = prompt if prompt else f"Provide a final analysis on the consolidated report: {json.dumps(consolidated_report, indent=2)}"
            messages = [{"role": "user", "content": content}]
            params = self._get_api_parameters(messages)
            response = self.client.chat.completions.create(**params)
            
            return {
                "agent": self.name or "DeepSeek Reasoner",
                "analysis": response.choices[0].message.content,
                "reasoning": response.choices[0].message.reasoning_content
            }
        except Exception as e:
            logger.error(f"Error in final_analysis: {str(e)}")
            return {"agent": self.name or "DeepSeek Reasoner", "error": str(e)}
    
    async def consolidate_results(self, all_results: Dict, prompt: Optional[str] = None) -> Dict:
        """Consolidate all phase results."""
        try:
            # Similar implementation pattern
            content = prompt if prompt else f"Consolidate all the phase results: {json.dumps(all_results, indent=2)}"
            messages = [{"role": "user", "content": content}]
            params = self._get_api_parameters(messages)
            response = self.client.chat.completions.create(**params)
            
            return {
                "phase": "Consolidation",
                "report": response.choices[0].message.content,
                "reasoning": response.choices[0].message.reasoning_content
            }
        except Exception as e:
            logger.error(f"Error in consolidate_results: {str(e)}")
            return {"phase": "Consolidation", "error": str(e)}

# Simpler Agent class for basic usage
class DeepSeekAgent:
    """
    Agent class for interacting with DeepSeek Reasoner model.
    
    This class provides a simpler interface for DeepSeek Reasoner focused on
    specific analysis tasks.
    """
    
    def __init__(
        self, 
        name: Optional[str] = None,
        role: Optional[str] = None,
        responsibilities: Optional[List[str]] = None
    ):
        """
        Initialize a DeepSeek Reasoner agent.
        
        Args:
            name: Optional agent name
            role: Optional role description
            responsibilities: Optional list of responsibilities
        """
        # Create the architect instance
        self.architect = DeepSeekArchitect(
            name=name,
            role=role,
            responsibilities=responsibilities
        )
    
    async def analyze(self, context: Dict) -> Dict:
        """Analyze the provided context."""
        return await self.architect.analyze(context)
        
    async def create_analysis_plan(self, phase1_results: Dict, prompt: Optional[str] = None) -> Dict:
        """Create an analysis plan based on Phase 1 results."""
        return await self.architect.create_analysis_plan(phase1_results, prompt)
    
    async def synthesize_findings(self, phase3_results: Dict, prompt: Optional[str] = None) -> Dict:
        """Synthesize findings from Phase 3."""
        return await self.architect.synthesize_findings(phase3_results, prompt)
    
    async def final_analysis(self, consolidated_report: Dict, prompt: Optional[str] = None) -> Dict:
        """Provide final analysis on the consolidated report."""
        return await self.architect.final_analysis(consolidated_report, prompt)
