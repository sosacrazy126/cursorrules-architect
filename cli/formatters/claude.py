"""
Claude Code configuration formatter.

Generates CLAUDE.md and CLAUDE.local.md following Anthropic's patterns.
"""

from typing import Dict, Any, List
from .base import BaseFormatter


class ClaudeFormatter(BaseFormatter):
    """Formatter for Claude Code configurations."""
    
    def format(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Format analysis results for Claude Code."""
        config_files = {}
        
        # Get core analysis content
        main_analysis = self.extract_analysis_content(analysis_results)
        project_type = self.get_project_type(analysis_results)
        technologies = self.get_project_technologies(analysis_results)
        
        # Main CLAUDE.md file (shared)
        config_files["CLAUDE.md"] = self._generate_claude_md(
            main_analysis, project_type, technologies
        )
        
        # Local CLAUDE.local.md file (user-specific, gitignored)
        config_files["CLAUDE.local.md"] = self._generate_claude_local()
        
        return config_files
    
    def get_output_files(self) -> List[str]:
        """Get list of output files for Claude Code."""
        return ["CLAUDE.md", "CLAUDE.local.md"]
    
    def _generate_claude_md(self, analysis: str, project_type: str, technologies: List[str]) -> str:
        """Generate main CLAUDE.md file."""
        tech_list = ", ".join(technologies[:5]) if technologies else "Various technologies"
        
        return f"""# Claude Code Configuration

## Project Overview

This is a {project_type} project using {tech_list}.

## Commands

Common development commands for this project:

{self._extract_commands(technologies)}

## Code Style

{self._extract_code_style(analysis, technologies)}

## Architecture

{self._extract_architecture_notes(analysis)}

## Working Guidelines

{self._extract_claude_guidelines(analysis)}

## Technology Stack

{self._format_claude_tech_notes(technologies)}

## Development Workflow

1. Review existing code patterns before making changes
2. Follow established architectural conventions
3. Write tests for new functionality
4. Document complex logic and decisions
5. Ensure code quality and maintainability

## Project Context

{self._extract_claude_context(analysis)}
"""
    
    def _generate_claude_local(self) -> str:
        """Generate CLAUDE.local.md file for user-specific settings."""
        return """# Claude Code Local Configuration

This file contains user-specific Claude Code settings and is typically gitignored.

## Personal Preferences

Add your personal Claude Code preferences here:

- Preferred code style settings
- Custom development commands
- Personal workflow notes
- Environment-specific configurations

## Local Commands

Add any local development commands specific to your environment:

```bash
# Example: Local development server
npm run dev:local

# Example: Local database setup
make db-setup-local
```

## Notes

- This file should not be committed to version control
- Add CLAUDE.local.md to your .gitignore file
- Use this for environment-specific or personal configurations

## Environment Variables

Document any local environment variables needed:

```bash
# Example environment variables
export API_KEY="your-local-api-key"
export DEBUG_MODE="true"
```
"""
    
    def _extract_commands(self, technologies: List[str]) -> str:
        """Extract common development commands based on technologies."""
        commands = []
        tech_lower = [t.lower() for t in technologies]
        
        if any(t in tech_lower for t in ['npm', 'node.js', 'react', 'vue', 'next.js']):
            commands.extend([
                "- `npm install`: Install dependencies", 
                "- `npm run dev`: Start development server",
                "- `npm run build`: Build for production",
                "- `npm test`: Run tests"
            ])
        
        if any(t in tech_lower for t in ['python', 'django', 'flask', 'fastapi']):
            commands.extend([
                "- `pip install -r requirements.txt`: Install dependencies",
                "- `python manage.py runserver`: Start development server",
                "- `python -m pytest`: Run tests"
            ])
        
        if any(t in tech_lower for t in ['docker']):
            commands.extend([
                "- `docker-compose up`: Start services",
                "- `docker-compose down`: Stop services"
            ])
        
        if not commands:
            commands = [
                "- Add project-specific commands here",
                "- Document build and test procedures",
                "- Include deployment instructions"
            ]
        
        return '\n'.join(commands)
    
    def _extract_code_style(self, analysis: str, technologies: List[str]) -> str:
        """Extract code style guidelines."""
        style_rules = []
        tech_lower = [t.lower() for t in technologies]
        
        # Technology-specific style rules
        if 'typescript' in tech_lower or 'javascript' in tech_lower:
            style_rules.append("- Use ES modules (import/export) syntax, not CommonJS (require)")
            style_rules.append("- Destructure imports when possible")
            style_rules.append("- Use async/await instead of Promises")
        
        if 'react' in tech_lower:
            style_rules.append("- Use functional components with hooks")
            style_rules.append("- Follow React naming conventions")
        
        if 'python' in tech_lower:
            style_rules.append("- Follow PEP 8 style guidelines")
            style_rules.append("- Use type hints for function parameters and return values")
        
        # Generic style rules
        if not style_rules:
            style_rules = [
                "- Follow established project conventions",
                "- Maintain consistent formatting and naming",
                "- Write clear, self-documenting code"
            ]
        
        return '\n'.join(style_rules)
    
    def _extract_architecture_notes(self, analysis: str) -> str:
        """Extract architecture notes from analysis."""
        lines = analysis.split('\n')
        arch_notes = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['architecture', 'pattern', 'structure', 'design']):
                if len(line) > 30 and len(line) < 200:
                    arch_notes.append(f"- {line}")
        
        if arch_notes:
            return '\n'.join(arch_notes[:5])
        else:
            return "- Follow established architectural patterns\n- Maintain separation of concerns\n- Use consistent project structure"
    
    def _extract_claude_guidelines(self, analysis: str) -> str:
        """Extract working guidelines for Claude Code."""
        lines = analysis.split('\n')
        guidelines = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['should', 'must', 'follow', 'ensure']):
                if len(line) > 25 and len(line) < 180:
                    guidelines.append(f"- {line}")
        
        if guidelines:
            return '\n'.join(guidelines[:8])
        else:
            return "- Follow project conventions and best practices\n- Maintain code quality and consistency\n- Write comprehensive tests for new features"
    
    def _format_claude_tech_notes(self, technologies: List[str]) -> str:
        """Format technology-specific notes for Claude Code."""
        if not technologies:
            return "- Apply best practices for the project's technology stack"
        
        notes = []
        for tech in technologies[:6]:
            notes.append(f"- **{tech}**: Follow {tech}-specific conventions and best practices")
        
        return '\n'.join(notes)
    
    def _extract_claude_context(self, analysis: str) -> str:
        """Extract project context for Claude Code."""
        lines = analysis.split('\n')
        context_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 40 and not line.startswith('-') and not line.startswith('*'):
                # Filter out lines that look like headers or commands
                if not line.startswith('#') and not line.isupper():
                    context_lines.append(line)
                    if len(context_lines) >= 5:
                        break
        
        return '\n'.join(context_lines) if context_lines else "Work within the established project architecture and follow existing patterns."