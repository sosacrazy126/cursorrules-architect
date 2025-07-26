"""
Windsurf IDE configuration formatter.

Generates .windsurfrules and global_rules.md following Windsurf patterns.
"""

from typing import Dict, Any, List
from .base import BaseFormatter


class WindsurfFormatter(BaseFormatter):
    """Formatter for Windsurf IDE configurations."""
    
    def format(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Format analysis results for Windsurf IDE."""
        config_files = {}
        
        # Get core analysis content
        main_analysis = self.extract_analysis_content(analysis_results)
        project_type = self.get_project_type(analysis_results)
        technologies = self.get_project_technologies(analysis_results)
        
        # Main windsurf rules file
        config_files[".windsurfrules"] = self._generate_windsurf_rules(
            main_analysis, project_type, technologies
        )
        
        return config_files
    
    def get_output_files(self) -> List[str]:
        """Get list of output files for Windsurf."""
        return [".windsurfrules"]
    
    def _generate_windsurf_rules(self, analysis: str, project_type: str, technologies: List[str]) -> str:
        """Generate main windsurf rules file."""
        tech_list = ", ".join(technologies[:5]) if technologies else "Various"
        
        return f"""# Windsurf AI Configuration

## Project Overview
This is a {project_type} project using {tech_list}.

## AI Guidelines
You are an expert AI assistant with deep knowledge of the project's architecture and patterns.

### Core Instructions
{self._extract_windsurf_instructions(analysis)}

### Technology Stack
{self._format_tech_guidelines(technologies)}

### Coding Standards
- Follow established project patterns and conventions
- Maintain consistency with existing code style
- Prioritize code readability and maintainability
- Write comprehensive tests for new functionality
- Document complex logic and architectural decisions

### Windsurf-Specific Behavior
- Use agentic workflows for multi-file operations
- Apply deep reasoning for complex problems
- Leverage contextual understanding across the codebase
- Provide step-by-step problem solving approach

### Project Context
{self._extract_windsurf_context(analysis)}

### Response Guidelines
- Provide clear, actionable solutions
- Include code examples when helpful
- Explain reasoning for significant changes
- Suggest improvements and optimizations
- Use Windsurf's multi-file editing capabilities effectively
"""
    
    def _extract_windsurf_instructions(self, analysis: str) -> str:
        """Extract core instructions optimized for Windsurf."""
        lines = analysis.split('\n')
        instructions = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['should', 'must', 'follow', 'use', 'implement']):
                if len(line) > 20 and len(line) < 200:
                    instructions.append(f"- {line}")
        
        return '\n'.join(instructions[:8]) if instructions else "- Follow established project patterns"
    
    def _format_tech_guidelines(self, technologies: List[str]) -> str:
        """Format technology-specific guidelines for Windsurf."""
        if not technologies:
            return "- Follow best practices for the identified technologies"
        
        guidelines = []
        for tech in technologies[:5]:
            guidelines.append(f"- **{tech}**: Apply {tech}-specific best practices and patterns")
        
        return '\n'.join(guidelines)
    
    def _extract_windsurf_context(self, analysis: str) -> str:
        """Extract project context optimized for Windsurf."""
        lines = analysis.split('\n')
        context_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 50 and not line.startswith('-'):
                context_lines.append(line)
                if len(context_lines) >= 4:
                    break
        
        return '\n'.join(context_lines) if context_lines else "Follow the established project architecture."