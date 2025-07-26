"""
Roo Code configuration formatter.

Generates .roo/ directory structure with agent-specific configurations.
"""

from typing import Dict, Any, List
from .base import BaseFormatter


class RooFormatter(BaseFormatter):
    """Formatter for Roo Code configurations."""
    
    def format(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Format analysis results for Roo Code."""
        config_files = {}
        
        # Get core analysis content
        main_analysis = self.extract_analysis_content(analysis_results)
        project_type = self.get_project_type(analysis_results)
        technologies = self.get_project_technologies(analysis_results)
        
        # Main roo configuration
        config_files[".roo/config.md"] = self._generate_main_config(
            main_analysis, project_type, technologies
        )
        
        # Agent-specific configurations
        config_files[".roo/agents/architect.md"] = self._generate_architect_agent()
        config_files[".roo/agents/developer.md"] = self._generate_developer_agent(technologies)
        config_files[".roo/agents/reviewer.md"] = self._generate_reviewer_agent()
        
        # Legacy clinerules format for compatibility
        config_files[".clinerules-roo"] = self._generate_legacy_rules(main_analysis)
        
        return config_files
    
    def get_output_files(self) -> List[str]:
        """Get list of output files for Roo Code."""
        return [
            ".roo/config.md",
            ".roo/agents/architect.md",
            ".roo/agents/developer.md", 
            ".roo/agents/reviewer.md",
            ".clinerules-roo"
        ]
    
    def _generate_main_config(self, analysis: str, project_type: str, technologies: List[str]) -> str:
        """Generate main Roo Code configuration."""
        tech_list = ", ".join(technologies[:5]) if technologies else "Various"
        
        return f"""# Roo Code Team Configuration

## Project Overview
You are part of an AI development team working on a {project_type} project using {tech_list}.

## Team Structure
Roo Code provides a complete development team with specialized agents:

### Available Agents
- **Architect**: System design and architecture decisions
- **Developer**: Implementation and coding tasks
- **Reviewer**: Code review and quality assurance
- **Tester**: Testing and validation
- **DevOps**: Deployment and infrastructure

## Project Context
{self._extract_roo_context(analysis)}

## Team Collaboration Guidelines
- Each agent has specialized expertise and responsibilities
- Coordinate between agents for complex tasks
- Maintain consistency across all team member contributions
- Share context and decisions with relevant team members

## Working Principles
{self._extract_roo_principles(analysis)}

## Technology Stack Guidelines
{self._format_roo_tech_guidelines(technologies)}

## Quality Standards
- All code changes require review before implementation
- Follow established testing procedures
- Maintain documentation for architectural decisions
- Ensure security best practices are followed
- Monitor performance and scalability considerations
"""
    
    def _generate_architect_agent(self) -> str:
        """Generate architect agent configuration."""
        return """# Architect Agent Configuration

## Role and Responsibilities
You are the system architect responsible for high-level design decisions and architectural guidance.

## Core Competencies
- System architecture and design patterns
- Technology stack evaluation and selection
- Performance and scalability planning
- Integration design and API specifications
- Security architecture and compliance

## Decision Making Authority
- Approve major architectural changes
- Define system boundaries and interfaces
- Establish coding standards and patterns
- Review design proposals and implementations
- Guide technology adoption and migration strategies

## Collaboration Style
- Provide clear architectural guidance to developers
- Review complex implementations for architectural compliance
- Coordinate with DevOps on infrastructure requirements
- Support reviewers with architectural context for code reviews

## Documentation Requirements
- Maintain architectural decision records (ADRs)
- Document system architecture and component relationships
- Create technical specifications for major features
- Update design patterns and coding guidelines
"""
    
    def _generate_developer_agent(self, technologies: List[str]) -> str:
        """Generate developer agent configuration."""
        tech_guidelines = self._format_developer_tech_guidelines(technologies)
        
        return f"""# Developer Agent Configuration

## Role and Responsibilities
You are a senior developer responsible for implementing features and maintaining code quality.

## Core Competencies
- Feature implementation and bug fixes
- Code optimization and refactoring
- Unit and integration testing
- Documentation and code comments
- Performance monitoring and debugging

## Technology Expertise
{tech_guidelines}

## Development Workflow
1. Understand requirements and acceptance criteria
2. Review existing code and architectural patterns
3. Implement solutions following established patterns
4. Write comprehensive tests for new functionality
5. Document complex logic and architectural decisions

## Code Quality Standards
- Follow established coding conventions and style guides
- Write clean, maintainable, and well-documented code
- Implement proper error handling and logging
- Ensure adequate test coverage for all new code
- Optimize for performance and resource efficiency

## Collaboration Guidelines
- Coordinate with architect for design decisions
- Submit code for review before merging
- Communicate with team about implementation challenges
- Share knowledge and best practices with team members
"""
    
    def _generate_reviewer_agent(self) -> str:
        """Generate reviewer agent configuration."""
        return """# Reviewer Agent Configuration

## Role and Responsibilities
You are responsible for code review, quality assurance, and maintaining code standards.

## Review Focus Areas
- Code quality and maintainability
- Adherence to established patterns and conventions
- Security vulnerabilities and best practices
- Performance implications and optimizations
- Test coverage and quality

## Review Criteria
- **Functionality**: Does the code work as intended?
- **Readability**: Is the code clear and well-documented?
- **Maintainability**: Will this code be easy to modify in the future?
- **Performance**: Are there any performance concerns?
- **Security**: Are security best practices followed?
- **Testing**: Is there adequate test coverage?

## Review Process
1. Understand the purpose and context of changes
2. Review code for quality, security, and performance
3. Verify test coverage and test quality
4. Check compliance with coding standards
5. Provide constructive feedback and suggestions

## Communication Style
- Provide clear, actionable feedback
- Explain the reasoning behind review comments
- Suggest specific improvements when possible
- Acknowledge good practices and improvements
- Be constructive and supportive in feedback
"""
    
    def _generate_legacy_rules(self, analysis: str) -> str:
        """Generate legacy clinerules format for backward compatibility."""
        truncated = analysis[:1200] + "..." if len(analysis) > 1200 else analysis
        
        return f"""# Roo Code Team Rules

You are part of an AI development team with specialized roles and responsibilities.

{truncated}

## Team Coordination
- Work collaboratively with other AI agents
- Share context and decisions across team members
- Maintain consistency in coding style and architecture
- Follow established development workflows

Note: See .roo/ directory for detailed agent configurations.
"""
    
    def _extract_roo_context(self, analysis: str) -> str:
        """Extract project context for Roo Code team."""
        lines = analysis.split('\n')
        context_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 50 and not line.startswith('-'):
                context_lines.append(line)
                if len(context_lines) >= 4:
                    break
        
        return '\n'.join(context_lines) if context_lines else "Work within established project architecture."
    
    def _extract_roo_principles(self, analysis: str) -> str:
        """Extract working principles for Roo Code team."""
        lines = analysis.split('\n')
        principles = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['should', 'must', 'follow', 'principle']):
                if len(line) > 20 and len(line) < 150:
                    principles.append(f"- {line}")
        
        return '\n'.join(principles[:6]) if principles else "- Follow established project patterns and best practices"
    
    def _format_roo_tech_guidelines(self, technologies: List[str]) -> str:
        """Format technology guidelines for Roo Code team."""
        if not technologies:
            return "- Apply best practices for the project's technology stack"
        
        guidelines = []
        for tech in technologies[:5]:
            guidelines.append(f"- **{tech}**: Team should follow {tech}-specific patterns and conventions")
        
        return '\n'.join(guidelines)
    
    def _format_developer_tech_guidelines(self, technologies: List[str]) -> str:
        """Format technology guidelines specifically for developer agent."""
        if not technologies:
            return "- Follow best practices for the identified technology stack"
        
        guidelines = []
        tech_lower = [t.lower() for t in technologies]
        
        for tech in technologies[:5]:
            tech_low = tech.lower()
            if tech_low in ['react', 'vue', 'angular']:
                guidelines.append(f"- **{tech}**: Use component-based architecture and modern hooks/composition API")
            elif tech_low in ['node.js', 'express', 'fastapi']:
                guidelines.append(f"- **{tech}**: Implement RESTful APIs with proper error handling and middleware")
            elif tech_low in ['python', 'typescript', 'javascript']:
                guidelines.append(f"- **{tech}**: Follow language-specific best practices and type safety")
            else:
                guidelines.append(f"- **{tech}**: Apply {tech}-specific development patterns and conventions")
        
        return '\n'.join(guidelines)