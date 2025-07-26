"""
Cline VS Code extension configuration formatter.

Generates .clinerules/ directory with MCP integration support.
"""

from typing import Dict, Any, List
from .base import BaseFormatter


class ClineFormatter(BaseFormatter):
    """Formatter for Cline VS Code extension configurations."""
    
    def format(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Format analysis results for Cline."""
        config_files = {}
        
        # Get core analysis content
        main_analysis = self.extract_analysis_content(analysis_results)
        project_type = self.get_project_type(analysis_results)
        technologies = self.get_project_technologies(analysis_results)
        
        # Main cline rules
        config_files[".clinerules/main.md"] = self._generate_main_rules(
            main_analysis, project_type, technologies
        )
        
        # MCP configuration
        config_files[".clinerules/mcp-config.md"] = self._generate_mcp_config(technologies)
        
        # Legacy single file for backward compatibility
        config_files[".clinerules"] = self._generate_legacy_rules(main_analysis)
        
        return config_files
    
    def get_output_files(self) -> List[str]:
        """Get list of output files for Cline."""
        return [
            ".clinerules/main.md",
            ".clinerules/mcp-config.md", 
            ".clinerules"
        ]
    
    def _generate_main_rules(self, analysis: str, project_type: str, technologies: List[str]) -> str:
        """Generate main cline rules file."""
        tech_list = ", ".join(technologies[:5]) if technologies else "Various"
        
        return f"""# Cline AI Configuration - Main Rules

## Project Overview
You are working on a {project_type} project using {tech_list}.

## Cline-Specific Instructions
You are an AI agent with access to terminal, file system, and development tools.

### Core Capabilities
- Execute terminal commands safely and efficiently
- Read, write, and modify files across the project
- Use MCP (Model Context Protocol) for enhanced integrations
- Perform multi-step development workflows
- Test and validate changes automatically

### Working Style
{self._extract_cline_instructions(analysis)}

### Technology Guidelines
{self._format_cline_tech_guidelines(technologies)}

### Development Workflow
1. Understand the task and analyze existing code
2. Plan changes with consideration for existing patterns
3. Implement changes incrementally
4. Test changes and verify functionality
5. Document significant modifications

### Safety Guidelines
- Always backup important files before major changes
- Test changes in development environment first
- Use version control for tracking modifications
- Validate file permissions before writing
- Confirm destructive operations with user

### Project Context
{self._extract_cline_context(analysis)}
"""
    
    def _generate_mcp_config(self, technologies: List[str]) -> str:
        """Generate MCP (Model Context Protocol) configuration."""
        return f"""# MCP Configuration for Cline

## Model Context Protocol Setup
Cline supports MCP for enhanced development capabilities.

### Recommended MCP Servers
Based on your technology stack, consider these MCP integrations:

{self._suggest_mcp_servers(technologies)}

### Integration Guidelines
- Use MCP servers for specialized development tasks
- Leverage context protocol for better code understanding
- Enable appropriate servers based on project needs
- Monitor MCP server performance and reliability

### Configuration Notes
- MCP servers can be configured in Cline settings
- Each server provides specific capabilities
- Multiple servers can be used simultaneously
- Custom MCP servers can be developed for specific needs

### Troubleshooting
- Check MCP server connectivity in Cline status
- Verify server configurations and permissions
- Monitor server logs for error diagnosis
- Restart servers if connectivity issues occur
"""
    
    def _generate_legacy_rules(self, analysis: str) -> str:
        """Generate legacy single-file rules for backward compatibility."""
        truncated = analysis[:1500] + "..." if len(analysis) > 1500 else analysis
        
        return f"""# Cline AI Assistant Rules

You are an AI assistant with terminal and file system access.

{truncated}

## Key Guidelines:
- Use terminal commands safely and efficiently
- Test changes before finalizing
- Follow established project patterns
- Leverage MCP integrations when available

Note: See .clinerules/ directory for detailed configuration.
"""
    
    def _extract_cline_instructions(self, analysis: str) -> str:
        """Extract instructions optimized for Cline's capabilities."""
        lines = analysis.split('\n')
        instructions = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['should', 'must', 'follow', 'use']):
                if len(line) > 15 and len(line) < 150:
                    instructions.append(f"- {line}")
        
        return '\n'.join(instructions[:8]) if instructions else "- Follow project conventions and best practices"
    
    def _format_cline_tech_guidelines(self, technologies: List[str]) -> str:
        """Format technology guidelines for Cline."""
        if not technologies:
            return "- Apply best practices for the project's technology stack"
        
        guidelines = []
        for tech in technologies[:5]:
            guidelines.append(f"- **{tech}**: Use appropriate {tech} development tools and practices")
        
        return '\n'.join(guidelines)
    
    def _suggest_mcp_servers(self, technologies: List[str]) -> str:
        """Suggest relevant MCP servers based on technologies."""
        suggestions = []
        tech_lower = [t.lower() for t in technologies]
        
        if any(t in tech_lower for t in ['git', 'github']):
            suggestions.append("- **Git MCP Server**: For advanced git operations and repository management")
        
        if any(t in tech_lower for t in ['docker', 'kubernetes']):
            suggestions.append("- **Container MCP Server**: For Docker and Kubernetes operations")
        
        if any(t in tech_lower for t in ['node.js', 'npm', 'yarn']):
            suggestions.append("- **Node.js MCP Server**: For Node.js package management and tooling")
        
        if any(t in tech_lower for t in ['python', 'pip', 'poetry']):
            suggestions.append("- **Python MCP Server**: For Python package management and virtual environments")
        
        if any(t in tech_lower for t in ['database', 'sql', 'postgresql', 'mysql']):
            suggestions.append("- **Database MCP Server**: For database operations and migrations")
        
        if not suggestions:
            suggestions.append("- **General Development MCP Server**: For common development tasks")
            suggestions.append("- **File System MCP Server**: For enhanced file operations")
        
        return '\n'.join(suggestions)
    
    def _extract_cline_context(self, analysis: str) -> str:
        """Extract project context optimized for Cline."""
        lines = analysis.split('\n')
        context_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 40 and not line.startswith('-') and not line.startswith('*'):
                context_lines.append(line)
                if len(context_lines) >= 3:
                    break
        
        return '\n'.join(context_lines) if context_lines else "Work within the established project architecture and patterns."