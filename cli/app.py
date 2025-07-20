"""
Main Typer application for CursorRules Architect CLI.

Modern 2025 CLI with interactive TUI mode and direct command support.
"""

import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from .commands.generate import generate_command
from .commands.list_tools import list_tools_command
from .commands.validate import validate_command

# Create the main Typer app
app = typer.Typer(
    name="cursorrules-architect",
    help="🚀 Generate AI agent configurations for any project",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,  # Disable for now, can be enabled later
)

# Initialize Rich console
console = Console()

# Add commands to the app
app.command("generate", help="Generate AI agent configuration files")(generate_command)
app.command("list", help="List all supported AI coding tools")(list_tools_command)
app.command("validate", help="Validate existing configuration files")(validate_command)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, 
        "--version", 
        "-v",
        help="Show version information"
    ),
    interactive: Optional[bool] = typer.Option(
        None,
        "--interactive",
        "-i", 
        help="Launch interactive TUI mode"
    ),
):
    """
    🚀 **CursorRules Architect** - Modern AI Agent Configuration Generator
    
    **Usage Patterns:**
    
    • `cursorrules-architect` - Launch interactive TUI mode
    • `cursorrules-architect /path/to/project` - Quick analysis mode  
    • `cursorrules-architect generate --tool cursor /path/to/project` - Direct generation
    
    **Supported AI Tools (2025):**
    Cursor, Windsurf, Cline, Roo Code, Claude Code, PearAI, GitHub Copilot, and more!
    """
    
    if version:
        show_version()
        raise typer.Exit()
    
    # If a command was invoked, let it handle execution
    if ctx.invoked_subcommand is not None:
        return
    
    # If interactive flag set, launch TUI
    if interactive:
        launch_interactive_mode()
        raise typer.Exit()
    
    # If no command provided, launch interactive mode by default
    launch_interactive_mode()
    raise typer.Exit()


def show_version():
    """Display version information with rich formatting."""
    version_panel = Panel(
        Text.assemble(
            ("CursorRules Architect", "bold cyan"),
            "\n",
            ("Version: ", "dim"),
            ("2.0.0-2025", "green bold"),
            "\n",
            ("Modern AI Agent Configuration Generator", "dim"),
            "\n\n",
            ("🎯 Supported Tools: ", "dim"),
            ("12+ AI coding tools", "yellow"),
            "\n",
            ("⚡ Framework: ", "dim"),
            ("Textual + Rich + Typer", "magenta"),
            "\n",
            ("🧠 Engine: ", "dim"),
            ("Context Engineering + Protocol Engine", "blue"),
        ),
        title="Version Info",
        border_style="cyan"
    )
    console.print(version_panel)


def launch_interactive_mode():
    """Launch the interactive TUI mode."""
    try:
        from .interactive.main_app import ConfiguratorApp
        app = ConfiguratorApp()
        app.run()
    except ImportError as e:
        console.print(
            Panel(
                Text.assemble(
                    ("❌ Interactive mode unavailable", "red bold"),
                    "\n\n",
                    ("Missing dependency: ", "dim"),
                    (str(e), "yellow"),
                    "\n\n",
                    ("Install with: ", "dim"),
                    ("pip install textual", "green"),
                ),
                title="Error",
                border_style="red"
            )
        )
        console.print("\n💡 [dim]Use direct commands instead:[/] cursorrules-architect generate --help")




if __name__ == "__main__":
    app()