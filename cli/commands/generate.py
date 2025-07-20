"""
Generate command for creating AI agent configuration files.

Modern 2025 implementation with support for all major AI coding tools.
"""

import asyncio
import time
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

# Import existing analysis components
import sys
import os
sys.path.append(str(Path(__file__).parent.parent.parent))

from main import ProjectAnalyzer

console = Console()

# Define supported tools
SUPPORTED_TOOLS = {
    "cursor": {
        "name": "Cursor",
        "format": ".cursor/rules/",
        "description": "Cursor IDE with directory-based rules",
        "ready": True
    },
    "windsurf": {
        "name": "Windsurf", 
        "format": ".windsurfrules",
        "description": "Windsurf agentic IDE",
        "ready": True
    },
    "cline": {
        "name": "Cline",
        "format": ".clinerules/",
        "description": "Cline VS Code extension with MCP support",
        "ready": True
    },
    "roo": {
        "name": "Roo Code",
        "format": ".roo/",
        "description": "Roo Code AI development team",
        "ready": True
    },
    "claude": {
        "name": "Claude Code",
        "format": "CLAUDE.md",
        "description": "Claude Code CLI tool",
        "ready": True
    },
    "pearai": {
        "name": "PearAI",
        "format": "Custom format",
        "description": "PearAI coding assistant",
        "ready": False
    },
    "copilot": {
        "name": "GitHub Copilot",
        "format": "Settings integration",
        "description": "GitHub Copilot Workspace",
        "ready": False
    },
    "bolt": {
        "name": "Bolt.new",
        "format": "Export format",
        "description": "Bolt.new rapid prototyping",
        "ready": False
    },
    "all": {
        "name": "All Tools",
        "format": "Multiple formats",
        "description": "Generate configurations for all supported tools",
        "ready": True
    }
}


def generate_command(
    directory: Path = typer.Argument(
        ...,
        help="Project directory to analyze",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    tool: Optional[str] = typer.Option(
        None,
        "--tool",
        "-t",
        help="Target AI tool (cursor, windsurf, cline, roo, claude, all)",
        autocompletion=lambda: list(SUPPORTED_TOOLS.keys())
    ),
    complexity: Optional[str] = typer.Option(
        "standard",
        "--complexity", 
        "-c",
        help="Analysis complexity level",
        autocompletion=lambda: ["quick", "standard", "advanced", "custom"]
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Custom output directory (default: project directory)"
    ),
    preview: bool = typer.Option(
        False,
        "--preview",
        "-p",
        help="Preview configuration without saving"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f", 
        help="Overwrite existing configuration files"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output with detailed progress"
    )
):
    """
    🚀 **Generate AI agent configuration files**
    
    Analyzes your project and creates optimized configuration files for AI coding tools.
    
    **Examples:**
    
    • `cursorrules-architect generate /path/to/project`
    • `cursorrules-architect generate /path/to/project --tool cursor`
    • `cursorrules-architect generate /path/to/project --tool all --complexity advanced`
    • `cursorrules-architect generate /path/to/project --preview`
    """
    
    # Show generation header
    show_generation_header(directory, tool, complexity)
    
    # Validate tool selection
    if tool and tool not in SUPPORTED_TOOLS:
        console.print(f"[red]❌ Unknown tool: {tool}[/]")
        console.print(f"[dim]Supported tools: {', '.join(SUPPORTED_TOOLS.keys())}[/]")
        raise typer.Exit(1)
    
    # Check if tool is ready
    if tool and not SUPPORTED_TOOLS[tool]["ready"]:
        console.print(f"[yellow]⚠️  Tool '{tool}' is not yet implemented[/]")
        console.print("[dim]Use --tool cursor, windsurf, cline, roo, or claude for now[/]")
        raise typer.Exit(1)
    
    # Interactive tool selection if not specified
    if not tool:
        tool = prompt_tool_selection()
    
    # Set output directory
    output_directory = output_dir or directory
    
    try:
        # Run the analysis
        analysis_results = run_project_analysis(directory, complexity, verbose)
        
        # Generate configurations
        generated_files = generate_configurations(
            analysis_results, 
            tool, 
            output_directory, 
            preview, 
            force
        )
        
        # Show success summary
        show_success_summary(generated_files, output_directory, preview)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Generation cancelled by user[/]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Generation failed: {str(e)}[/]")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


def show_generation_header(directory: Path, tool: Optional[str], complexity: str):
    """Show the generation header with project info."""
    header_text = Text.assemble(
        ("🚀 AI Configuration Generation", "bold cyan"),
        "\n\n",
        ("📁 Project: ", "dim"),
        (str(directory.name), "green bold"),
        "\n",
        ("📍 Path: ", "dim"),
        (str(directory), "blue"),
        "\n",
        ("🎯 Tool: ", "dim"),
        (tool or "Interactive selection", "yellow"),
        "\n",
        ("⚡ Complexity: ", "dim"),
        (complexity, "magenta"),
    )
    
    console.print(Panel(header_text, title="Generation Settings", border_style="cyan"))


def prompt_tool_selection() -> str:
    """Prompt user for tool selection with rich interface."""
    console.print("\n[bold]🎯 Select target AI tool:[/]")
    
    # Show available tools
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Option", style="yellow", width=10)
    table.add_column("Tool", style="cyan")
    table.add_column("Format", style="green")
    table.add_column("Status", width=12)
    
    options = []
    for key, info in SUPPORTED_TOOLS.items():
        if key == "all":
            continue
        status = "✅ Ready" if info["ready"] else "🚧 Soon"
        table.add_row(key, info["name"], info["format"], status)
        if info["ready"]:
            options.append(key)
    
    table.add_row("all", "All Tools", "Multiple", "✅ Ready")
    options.append("all")
    
    console.print(table)
    
    while True:
        choice = typer.prompt(
            "\nEnter tool choice",
            default="cursor"
        ).lower().strip()
        
        if choice in options:
            return choice
        
        console.print(f"[red]Invalid choice. Use one of: {', '.join(options)}[/]")


def run_project_analysis(directory: Path, complexity: str, verbose: bool) -> dict:
    """Run the project analysis using existing pipeline."""
    
    console.print(f"\n[bold blue]🔍 Analyzing project...[/]")
    
    if verbose:
        console.print(f"[dim]Using {complexity} complexity analysis[/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        analysis_task = progress.add_task("Running 6-phase analysis...", total=6)
        
        # Use the existing ProjectAnalyzer
        analyzer = ProjectAnalyzer(directory)
        
        # Run analysis (this will use the existing rich progress internally)
        analysis_result = asyncio.run(analyzer.analyze())
        
        # Extract results
        results = {
            "phase1": analyzer.phase1_results,
            "phase2": analyzer.phase2_results, 
            "phase3": analyzer.phase3_results,
            "phase4": analyzer.phase4_results,
            "consolidated_report": analyzer.consolidated_report,
            "final_analysis": analyzer.final_analysis,
        }
        
        progress.update(analysis_task, completed=6)
    
    console.print("[green]✅ Analysis complete[/]")
    return results


def generate_configurations(
    analysis_results: dict,
    tool: str, 
    output_directory: Path,
    preview: bool,
    force: bool
) -> List[str]:
    """Generate configuration files for the specified tool(s)."""
    
    console.print(f"\n[bold green]📝 Generating configurations...[/]")
    
    generated_files = []
    
    if tool == "all":
        # Generate for all ready tools
        ready_tools = [k for k, v in SUPPORTED_TOOLS.items() 
                      if k != "all" and v["ready"]]
        
        for tool_name in ready_tools:
            files = generate_single_tool_config(
                analysis_results, tool_name, output_directory, preview, force
            )
            generated_files.extend(files)
    else:
        # Generate for single tool
        files = generate_single_tool_config(
            analysis_results, tool, output_directory, preview, force
        )
        generated_files.extend(files)
    
    return generated_files


def generate_single_tool_config(
    analysis_results: dict,
    tool: str,
    output_directory: Path, 
    preview: bool,
    force: bool
) -> List[str]:
    """Generate configuration for a single tool."""
    
    # Import the appropriate formatter
    try:
        from ..formatters import get_formatter
        formatter = get_formatter(tool)
    except ImportError:
        # Fallback to basic generation using existing system
        return generate_legacy_config(analysis_results, tool, output_directory, preview, force)
    
    # Use the new formatter system
    config_content = formatter.format(analysis_results)
    output_files = formatter.save(config_content, output_directory, preview, force)
    
    return output_files


def generate_legacy_config(
    analysis_results: dict,
    tool: str,
    output_directory: Path,
    preview: bool, 
    force: bool
) -> List[str]:
    """Generate configuration files using the analysis results."""
    
    # Extract the final analysis content (this contains the .cursorrules content)
    final_analysis = analysis_results.get("final_analysis", {})
    cursor_rules = final_analysis.get("analysis", "")
    
    if not cursor_rules:
        console.print("[red]❌ No configuration content generated[/]")
        console.print("[dim]This usually means the final analysis phase failed[/]")
        return []
    
    # Adapt content for specific tools and determine output file
    adapted_content = adapt_content_for_tool(cursor_rules, tool)
    
    filename_map = {
        "cursor": ".cursorrules",
        "windsurf": ".windsurfrules", 
        "cline": ".clinerules",
        "roo": ".roorules",
        "claude": "CLAUDE.md"
    }
    
    filename = filename_map.get(tool, ".cursorrules")
    output_file = output_directory / filename
    
    if preview:
        console.print(f"\n[bold]📄 Preview for {tool} ({filename}):[/]")
        preview_content = adapted_content[:800] + "..." if len(adapted_content) > 800 else adapted_content
        console.print(Panel(preview_content, title=f"{tool.title()} Configuration Preview"))
        return [str(output_file)]
    
    # Check if file exists
    if output_file.exists() and not force:
        console.print(f"[yellow]⚠️  File exists: {output_file}[/]")
        overwrite = typer.confirm("Overwrite?")
        if not overwrite:
            return []
    
    # Write the adapted content to file
    output_file.write_text(adapted_content, encoding="utf-8")
    console.print(f"[green]✅ Generated: {output_file}[/]")
    
    return [str(output_file)]


def adapt_content_for_tool(cursor_rules: str, tool: str) -> str:
    """Adapt the cursor rules content for specific AI tools."""
    
    # Tool-specific adaptations
    tool_adaptations = {
        "cursor": {
            "header": "# Cursor IDE Configuration (.cursorrules)",
            "instructions": "This configuration optimizes Cursor's AI assistant for your project.",
            "format": cursor_rules  # Keep original format
        },
        "windsurf": {
            "header": "# Windsurf Agentic IDE Configuration (.windsurfrules)", 
            "instructions": "This configuration optimizes Windsurf's autonomous development for your project.",
            "format": cursor_rules.replace("Cursor", "Windsurf").replace("cursor", "windsurf")
        },
        "cline": {
            "header": "# Cline VS Code Extension Configuration (.clinerules)",
            "instructions": "This configuration optimizes Cline's autonomous coding capabilities with MCP support.",
            "format": cursor_rules.replace("Cursor", "Cline").replace("cursor", "cline")
        },
        "roo": {
            "header": "# Roo Code AI Development Team Configuration (.roorules)",
            "instructions": "This configuration optimizes Roo's AI development team for your project.",
            "format": cursor_rules.replace("Cursor", "Roo Code").replace("cursor", "roo")
        },
        "claude": {
            "header": "# Claude Code CLI Configuration (CLAUDE.md)",
            "instructions": "This configuration provides context for Claude Code CLI tool interactions.",
            "format": f"""# Claude Code Project Context

{cursor_rules}

## Usage Instructions

This file provides context for Claude Code CLI interactions with your project. 
Place this file in your project root as `CLAUDE.md` to enhance Claude's understanding.

Run Claude Code commands with enhanced context:
```bash
claude-code analyze
claude-code generate
claude-code explain <file>
```
"""
        }
    }
    
    adaptation = tool_adaptations.get(tool, tool_adaptations["cursor"])
    
    # Add tool-specific header and instructions
    adapted_content = f"""{adaptation['header']}

{adaptation['instructions']}

---

{adaptation['format']}
"""
    
    return adapted_content


def show_success_summary(generated_files: List[str], output_dir: Path, preview: bool):
    """Show success summary with generated files."""
    
    if preview:
        console.print(f"\n[bold green]✅ Preview complete[/]")
        console.print(f"[dim]Use without --preview to save configurations[/]")
        return
    
    if not generated_files:
        console.print(f"[yellow]⚠️  No files were generated[/]")
        return
    
    # Success panel
    success_text = Text.assemble(
        ("🎉 Configuration generation complete!", "bold green"),
        "\n\n",
        ("📁 Output directory: ", "dim"),
        (str(output_dir), "cyan"),
        "\n",
        ("📄 Files generated: ", "dim"),
        (str(len(generated_files)), "yellow bold"),
    )
    
    console.print(Panel(success_text, title="Success", border_style="green"))
    
    # Show generated files
    console.print("\n[bold]📄 Generated files:[/]")
    for file_path in generated_files:
        relative_path = Path(file_path).relative_to(output_dir)
        console.print(f"  [green]✅[/] {relative_path}")
    
    # Show usage instructions
    console.print(f"\n[bold cyan]🚀 Next Steps:[/]")
    console.print(f"[dim]1. Copy the generated files to your project directory[/]")
    console.print(f"[dim]2. Restart your AI coding tool to load the new configuration[/]")
    console.print(f"[dim]3. Start coding with enhanced AI assistance![/]")
    
    # Show tool-specific tips
    if len(generated_files) == 1:
        file_path = Path(generated_files[0])
        tool_name = file_path.suffix.replace(".", "").replace("rules", "")
        if tool_name == "md":
            tool_name = "claude"
        
        tool_tips = {
            "cursor": "💡 Restart Cursor IDE to load the new .cursorrules configuration",
            "windsurf": "💡 Restart Windsurf IDE to activate the .windsurfrules configuration", 
            "cline": "💡 Reload VS Code window to activate the .clinerules configuration",
            "roo": "💡 The .roorules file will be automatically detected by Roo Code",
            "claude": "💡 Place CLAUDE.md in your project root for Claude Code CLI context"
        }
        
        tip = tool_tips.get(tool_name, "💡 Restart your AI tool to load the new configuration")
        console.print(f"\n[yellow]{tip}[/]")