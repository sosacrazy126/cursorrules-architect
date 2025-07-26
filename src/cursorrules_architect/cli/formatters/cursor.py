"""
Cursor IDE configuration formatter.

Generates .cursor/rules/ directory structure following 2025 best practices.
"""

from typing import Dict, Any, List
from .base import BaseFormatter


class CursorFormatter(BaseFormatter):
    """Formatter for Cursor IDE configurations."""
    
    def format(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Format analysis results for Cursor IDE.
        
        Cursor 2025 format uses .cursor/rules/ directory with multiple .mdc files
        for token-efficient, on-demand rule loading.
        """
        config_files = {}
        
        # Get core analysis content
        main_analysis = self.extract_analysis_content(analysis_results)
        project_type = self.get_project_type(analysis_results)
        technologies = self.get_project_technologies(analysis_results)
        
        # Main cursor rules file
        config_files[".cursor/rules/main.mdc"] = self._generate_main_rules(
            main_analysis, project_type, technologies
        )
        
        # Technology-specific rules
        if technologies:
            config_files[".cursor/rules/tech-stack.mdc"] = self._generate_tech_rules(technologies)
        
        # Project-specific patterns
        config_files[".cursor/rules/patterns.mdc"] = self._generate_pattern_rules(analysis_results)
        
        # Code style and quality rules
        config_files[".cursor/rules/quality.mdc"] = self._generate_quality_rules(project_type)
        
        # Legacy .cursorrules for backward compatibility
        config_files[".cursorrules"] = self._generate_legacy_rules(main_analysis)
        
        return config_files
    
    def get_output_files(self) -> List[str]:
        """Get list of output files for Cursor."""
        return [
            ".cursor/rules/main.mdc",
            ".cursor/rules/tech-stack.mdc", 
            ".cursor/rules/patterns.mdc",
            ".cursor/rules/quality.mdc",
            ".cursorrules"
        ]
    
    def _generate_main_rules(self, analysis: str, project_type: str, technologies: List[str]) -> str:
        """Generate main cursor rules file."""
        tech_list = ", ".join(technologies[:5]) if technologies else "Various"
        
        return f"""# Cursor AI Configuration - Main Rules

## Project Context
You are an expert AI assistant working on a {project_type} project using {tech_list}.

## Core Instructions
{self._extract_core_instructions(analysis)}

## Working Style
- Follow existing code patterns and conventions
- Maintain consistency with the established architecture
- Prioritize code readability and maintainability
- Write comprehensive tests for new functionality
- Document complex logic and architectural decisions

## Response Format
- Provide clear, actionable solutions
- Include code examples when helpful
- Explain reasoning for significant changes
- Suggest improvements when appropriate

## Project-Specific Context
{self._extract_project_context(analysis)}
"""
    
    def _generate_tech_rules(self, technologies: List[str]) -> str:
        """Generate technology-specific rules."""
        tech_rules = ["# Technology-Specific Rules\n"]
        
        for tech in technologies:
            tech_lower = tech.lower()
            
            if tech_lower in ["react", "nextjs"]:
                tech_rules.append(f"""
## {tech} Guidelines
- Use functional components with hooks
- Implement proper TypeScript types
- Follow React best practices for state management
- Use proper component composition patterns
- Implement proper error boundaries
""")
            
            elif tech_lower in ["node.js", "nodejs", "express"]:
                tech_rules.append(f"""
## {tech} Guidelines  
- Use async/await for asynchronous operations
- Implement proper error handling middleware
- Follow RESTful API design principles
- Use environment variables for configuration
- Implement proper logging and monitoring
""")
            
            elif tech_lower in ["python", "fastapi", "django", "flask"]:
                tech_rules.append(f"""
## {tech} Guidelines
- Follow PEP 8 style guidelines
- Use type hints for better code clarity
- Implement proper exception handling
- Use virtual environments for dependency management
- Follow Python best practices for project structure
""")
            
            elif tech_lower in ["typescript", "javascript"]:
                tech_rules.append(f"""
## {tech} Guidelines
- Use strict TypeScript configuration
- Implement proper type definitions
- Follow modern ES6+ syntax
- Use consistent naming conventions
- Implement proper module organization
""")
        
        return "\n".join(tech_rules)
    
    def _generate_pattern_rules(self, analysis_results: Dict[str, Any]) -> str:
        """Generate project pattern rules."""
        patterns = []
        
        # Extract patterns from analysis
        phase3 = analysis_results.get("phase3", {})
        if isinstance(phase3, dict):
            architecture_patterns = phase3.get("architecture_patterns", [])
            if architecture_patterns:
                patterns.extend(architecture_patterns)
        
        pattern_content = """# Project Patterns and Architecture

## Established Patterns
Follow these patterns that are already established in the codebase:

"""
        
        if patterns:
            for pattern in patterns[:5]:  # Limit to top 5 patterns
                pattern_content += f"- {pattern}\n"
        else:
            pattern_content += "- Maintain consistency with existing code structure\n"
            pattern_content += "- Follow established naming conventions\n"
            pattern_content += "- Respect existing architectural boundaries\n"
        
        pattern_content += """
## Code Organization
- Keep related functionality grouped together
- Maintain clear separation of concerns
- Use consistent file and directory naming
- Document complex architectural decisions

## Best Practices
- Write self-documenting code
- Use meaningful variable and function names
- Keep functions small and focused
- Implement proper error handling
"""
        
        return pattern_content
    
    def _generate_quality_rules(self, project_type: str) -> str:
        """Generate code quality and style rules."""
        return f"""# Code Quality and Style Rules

## Code Quality Standards
- Maintain high code quality and readability
- Write comprehensive tests for new features
- Follow established coding conventions
- Implement proper error handling and logging

## Testing Requirements
- Write unit tests for core functionality
- Implement integration tests for key workflows
- Ensure adequate test coverage
- Use meaningful test descriptions

## Documentation Standards
- Document complex algorithms and business logic
- Maintain up-to-date README files
- Include code comments for non-obvious implementations
- Document API endpoints and data models

## Performance Considerations
- Optimize for {project_type} specific performance patterns
- Monitor and profile critical code paths
- Implement caching where appropriate
- Consider memory usage and resource efficiency

## Security Guidelines
- Follow security best practices for {project_type}
- Validate all user inputs
- Implement proper authentication and authorization
- Keep dependencies up to date
"""
    
    def _generate_legacy_rules(self, analysis: str) -> str:
        """Generate legacy .cursorrules file for backward compatibility."""
        # Extract first 2000 characters for legacy format
        truncated_analysis = analysis[:2000] + "..." if len(analysis) > 2000 else analysis
        
        return f"""You are an expert AI assistant working on this project.

{truncated_analysis}

Follow the existing code patterns and maintain consistency with the established architecture.
Write clean, maintainable code with appropriate tests and documentation.

Note: This is a legacy format. See .cursor/rules/ directory for detailed, modular rules.
"""
    
    def _extract_core_instructions(self, analysis: str) -> str:
        """Extract core instructions from analysis."""
        # Look for key instructional content
        lines = analysis.split('\n')
        instructions = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['should', 'must', 'follow', 'use', 'implement']):
                if len(line) > 20 and len(line) < 200:  # Reasonable instruction length
                    instructions.append(f"- {line}")
        
        if instructions:
            return '\n'.join(instructions[:10])  # Top 10 instructions
        else:
            return "- Follow established project patterns and conventions\n- Maintain code quality and consistency"
    
    def _extract_project_context(self, analysis: str) -> str:
        """Extract project-specific context from analysis."""
        # Look for project description or summary
        lines = analysis.split('\n')
        context_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 50 and not line.startswith('-') and not line.startswith('*'):
                context_lines.append(line)
                if len(context_lines) >= 3:  # Limit context
                    break
        
        return '\n'.join(context_lines) if context_lines else "Follow the established project architecture and patterns."