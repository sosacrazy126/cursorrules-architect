"""
Base formatter interface for AI tool configurations.

Defines the common interface that all tool-specific formatters must implement.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console

console = Console()


class BaseFormatter(ABC):
    """Base class for all configuration formatters."""
    
    def __init__(self):
        """Initialize the formatter."""
        self.tool_name = self.__class__.__name__.replace("Formatter", "").lower()
    
    @abstractmethod
    def format(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Format analysis results into tool-specific configuration.
        
        Args:
            analysis_results: Complete analysis results from the pipeline
            
        Returns:
            Dictionary mapping filename to content for tool-specific files
        """
        pass
    
    @abstractmethod 
    def get_output_files(self) -> List[str]:
        """
        Get list of output filenames this formatter generates.
        
        Returns:
            List of filenames (relative to project root)
        """
        pass
    
    def save(
        self, 
        config_content: Dict[str, str], 
        output_directory: Path, 
        preview: bool = False,
        force: bool = False
    ) -> List[str]:
        """
        Save configuration files to the output directory.
        
        Args:
            config_content: Dictionary mapping filename to content
            output_directory: Directory to save files to
            preview: If True, show preview instead of saving
            force: If True, overwrite existing files
            
        Returns:
            List of file paths that were created/would be created
        """
        created_files = []
        
        for filename, content in config_content.items():
            file_path = output_directory / filename
            
            if preview:
                self._show_preview(filename, content)
                created_files.append(str(file_path))
                continue
            
            # Check if file exists
            if file_path.exists() and not force:
                console.print(f"[yellow]⚠️  File exists: {file_path}[/]")
                # In CLI context, we might want to prompt, but for now skip
                continue
            
            # Create directory if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the file
            try:
                file_path.write_text(content, encoding="utf-8")
                console.print(f"[green]✅ Generated: {file_path.relative_to(output_directory)}[/]")
                created_files.append(str(file_path))
            except Exception as e:
                console.print(f"[red]❌ Failed to write {filename}: {str(e)}[/]")
        
        return created_files
    
    def _show_preview(self, filename: str, content: str):
        """Show a preview of the file content."""
        from rich.panel import Panel
        from rich.syntax import Syntax
        
        # Determine syntax highlighting based on file extension
        syntax = "markdown"
        if filename.endswith((".json", ".jsonc")):
            syntax = "json"
        elif filename.endswith((".yaml", ".yml")):
            syntax = "yaml"
        elif filename.endswith(".toml"):
            syntax = "toml"
        
        # Truncate very long content for preview
        preview_content = content
        if len(content) > 1000:
            preview_content = content[:1000] + "\n\n... (truncated)"
        
        # Show syntax-highlighted preview
        syntax_obj = Syntax(preview_content, syntax, theme="monokai", line_numbers=True)
        
        console.print(Panel(
            syntax_obj,
            title=f"📄 Preview: {filename}",
            border_style="blue"
        ))
    
    def extract_analysis_content(self, analysis_results: Dict[str, Any]) -> str:
        """
        Extract the main analysis content from results.
        
        Args:
            analysis_results: Complete analysis results
            
        Returns:
            Main analysis content as string
        """
        # Try to get final analysis first
        final_analysis = analysis_results.get("final_analysis", {})
        if isinstance(final_analysis, dict):
            content = final_analysis.get("analysis", "")
            if content:
                return content
        
        # Fallback to consolidated report
        consolidated = analysis_results.get("consolidated_report", {})
        if isinstance(consolidated, dict):
            content = consolidated.get("report", "")
            if content:
                return content
        
        # Last resort: try to reconstruct from phases
        return self._reconstruct_from_phases(analysis_results)
    
    def _reconstruct_from_phases(self, analysis_results: Dict[str, Any]) -> str:
        """Reconstruct analysis content from individual phases."""
        content_parts = []
        
        for phase in ["phase1", "phase2", "phase3", "phase4"]:
            phase_data = analysis_results.get(phase, {})
            if isinstance(phase_data, dict):
                # Extract meaningful content from phase
                if "analysis" in phase_data:
                    content_parts.append(f"## {phase.title()}\n{phase_data['analysis']}")
                elif "plan" in phase_data:
                    content_parts.append(f"## {phase.title()}\n{phase_data['plan']}")
        
        return "\n\n".join(content_parts) if content_parts else "Analysis content not available"
    
    def get_project_technologies(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Extract list of technologies from analysis results."""
        technologies = []
        
        # Check phase1 for tech stack
        phase1 = analysis_results.get("phase1", {})
        if isinstance(phase1, dict):
            tech_stack = phase1.get("tech_stack", [])
            if isinstance(tech_stack, list):
                technologies.extend(tech_stack)
        
        # Check for technologies in other phases
        for phase in ["phase2", "phase3", "phase4"]:
            phase_data = analysis_results.get(phase, {})
            if isinstance(phase_data, dict) and "technologies" in phase_data:
                tech_list = phase_data["technologies"]
                if isinstance(tech_list, list):
                    technologies.extend(tech_list)
        
        # Remove duplicates and return
        return list(set(technologies))
    
    def get_project_type(self, analysis_results: Dict[str, Any]) -> str:
        """Determine the project type from analysis results."""
        # Check phase1 for project type
        phase1 = analysis_results.get("phase1", {})
        if isinstance(phase1, dict):
            project_type = phase1.get("project_type", "")
            if project_type:
                return project_type
        
        # Infer from technologies
        technologies = self.get_project_technologies(analysis_results)
        tech_lower = [t.lower() for t in technologies]
        
        if any(t in tech_lower for t in ["react", "vue", "angular", "nextjs", "nuxt"]):
            return "web_frontend"
        elif any(t in tech_lower for t in ["express", "fastapi", "django", "flask", "nodejs"]):
            return "web_backend"
        elif any(t in tech_lower for t in ["react-native", "flutter", "ionic"]):
            return "mobile"
        elif any(t in tech_lower for t in ["electron", "tauri"]):
            return "desktop"
        else:
            return "general"