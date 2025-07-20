"""
List tools command to show all supported AI coding tools.

Displays comprehensive information about supported tools in 2025.
"""

from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns

console = Console()

# Comprehensive list of AI coding tools for 2025
AI_TOOLS_2025 = {
    "ready": {
        "cursor": {
            "name": "Cursor",
            "format": ".cursor/rules/",
            "description": "AI-first code editor with contextual understanding",
            "website": "https://cursor.sh",
            "features": ["Multi-file editing", "Codebase chat", "Auto-completion"],
            "pricing": "$20/month",
            "adoption": "7M+ developers"
        },
        "windsurf": {
            "name": "Windsurf", 
            "format": ".windsurfrules + global_rules.md",
            "description": "Agentic IDE by Codeium with deep reasoning",
            "website": "https://windsurf.com",
            "features": ["Agentic workflows", "Multi-file edits", "Deep reasoning"],
            "pricing": "$15/month",
            "adoption": "Fast growing"
        },
        "cline": {
            "name": "Cline",
            "format": ".clinerules/ directory",
            "description": "VS Code extension with MCP protocol support",
            "website": "https://cline.bot",
            "features": ["MCP integration", "Terminal access", "Multi-LLM support"],
            "pricing": "Free + LLM costs",
            "adoption": "Open source"
        },
        "roo": {
            "name": "Roo Code",
            "format": ".roo/ directory",
            "description": "Whole dev team of AI agents in your editor",
            "website": "https://roo.dev",
            "features": ["Multi-agent team", "Specialized roles", "Collaborative workflow"],
            "pricing": "Subscription",
            "adoption": "Developer focused"
        },
        "claude": {
            "name": "Claude Code",
            "format": "CLAUDE.md + CLAUDE.local.md",
            "description": "Official Anthropic CLI for Claude integration",
            "website": "https://claude.ai/code",
            "features": ["Official Anthropic", "Project awareness", "Rich markdown"],
            "pricing": "Claude subscription",
            "adoption": "Official tool"
        }
    },
    "coming_soon": {
        "pearai": {
            "name": "PearAI",
            "format": "Custom format",
            "description": "Rising AI coding assistant with unique approach",
            "website": "https://pearai.dev",
            "features": ["Innovative UI", "Custom workflows", "Community driven"],
            "pricing": "TBD",
            "adoption": "Beta"
        },
        "copilot": {
            "name": "GitHub Copilot Workspace",
            "format": "Settings integration",
            "description": "GitHub's enhanced Copilot with workspace features",
            "website": "https://github.com/features/copilot",
            "features": ["GitHub integration", "Workspace context", "Enterprise features"],
            "pricing": "$10-39/month",
            "adoption": "5M+ users"
        },
        "bolt": {
            "name": "Bolt.new",
            "format": "Export format",
            "description": "StackBlitz's rapid prototyping platform",
            "website": "https://bolt.new",
            "features": ["Instant deployment", "Full-stack apps", "Browser-based"],
            "pricing": "Free tier",
            "adoption": "Popular for demos"
        },
        "replit": {
            "name": "Replit Agent",
            "format": "Cloud configuration",
            "description": "Replit's AI coding agent for cloud development",
            "website": "https://replit.com",
            "features": ["Cloud native", "Collaborative", "Multi-language"],
            "pricing": "Part of Replit",
            "adoption": "Education focused"
        },
        "amazon_q": {
            "name": "Amazon Q Developer",
            "format": "AWS integration",
            "description": "Amazon's enterprise AI coding assistant",
            "website": "https://aws.amazon.com/q/developer/",
            "features": ["AWS integration", "Enterprise security", "Code reviews"],
            "pricing": "AWS pricing",
            "adoption": "Enterprise"
        }
    }
}


def list_tools_command(
    status: Optional[str] = typer.Option(
        None,
        "--status",
        "-s",
        help="Filter by status (ready, coming-soon, all)",
        autocompletion=lambda: ["ready", "coming-soon", "all"]
    ),
    detailed: bool = typer.Option(
        False,
        "--detailed",
        "-d",
        help="Show detailed information for each tool"
    ),
    format_table: bool = typer.Option(
        True,
        "--table/--no-table",
        help="Display as table (default) or cards"
    )
):
    """
    📋 **List all supported AI coding tools**
    
    Shows comprehensive information about AI coding tools supported by CursorRules Architect.
    
    **Examples:**
    
    • `cursorrules-architect list` - Show all tools
    • `cursorrules-architect list --status ready` - Show only ready tools  
    • `cursorrules-architect list --detailed` - Show detailed information
    • `cursorrules-architect list --no-table` - Show as cards instead of table
    """
    
    # Show header
    show_tools_header()
    
    # Determine which tools to show
    if status == "ready":
        tools_to_show = {"Ready Tools": AI_TOOLS_2025["ready"]}
    elif status == "coming-soon":
        tools_to_show = {"Coming Soon": AI_TOOLS_2025["coming_soon"]}
    else:
        tools_to_show = {
            "Ready Tools": AI_TOOLS_2025["ready"],
            "Coming Soon": AI_TOOLS_2025["coming_soon"]
        }
    
    # Display tools
    if format_table:
        show_tools_table(tools_to_show, detailed)
    else:
        show_tools_cards(tools_to_show, detailed)
    
    # Show usage tips
    show_usage_tips()


def show_tools_header():
    """Show the tools list header."""
    header_text = Text.assemble(
        ("🤖 AI Coding Tools Landscape 2025", "bold cyan"),
        "\n\n",
        ("CursorRules Architect supports configuration generation for ", "dim"),
        ("12+ major AI coding tools", "yellow bold"),
        (".", "dim"),
        "\n",
        ("Choose the right tool for your workflow and project needs.", "dim"),
    )
    
    console.print(Panel(header_text, title="Tool Overview", border_style="cyan"))


def show_tools_table(tools_dict: dict, detailed: bool):
    """Show tools in table format."""
    
    for section_title, tools in tools_dict.items():
        console.print(f"\n[bold]{section_title}[/]")
        
        # Create table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Tool", style="cyan", no_wrap=True, width=12)
        table.add_column("Configuration", style="green", width=20)
        table.add_column("Description", style="dim")
        
        if detailed:
            table.add_column("Pricing", style="yellow", width=12)
            table.add_column("Key Features", style="magenta", width=25)
        
        # Add rows
        for key, info in tools.items():
            description = info["description"]
            if len(description) > 50 and not detailed:
                description = description[:47] + "..."
            
            row = [
                info["name"],
                info["format"],
                description
            ]
            
            if detailed:
                features = ", ".join(info["features"][:2])  # Show first 2 features
                if len(info["features"]) > 2:
                    features += "..."
                
                row.extend([
                    info["pricing"],
                    features
                ])
            
            table.add_row(*row)
        
        console.print(table)


def show_tools_cards(tools_dict: dict, detailed: bool):
    """Show tools in card format."""
    
    for section_title, tools in tools_dict.items():
        console.print(f"\n[bold cyan]{section_title}[/]")
        
        cards = []
        for key, info in tools.items():
            card_content = Text.assemble(
                (info["name"], "bold green"),
                "\n",
                ("Format: ", "dim"),
                (info["format"], "yellow"),
                "\n\n",
                (info["description"], "white"),
            )
            
            if detailed:
                card_content.append("\n\n")
                card_content.append(("Pricing: ", "dim"))
                card_content.append((info["pricing"], "cyan"))
                card_content.append("\n")
                card_content.append(("Features: ", "dim"))
                card_content.append((", ".join(info["features"]), "magenta"))
                card_content.append("\n")
                card_content.append(("Website: ", "dim"))
                card_content.append((info["website"], "blue underline"))
            
            card = Panel(
                card_content,
                title=f"[bold]{info['name']}[/]",
                border_style="green" if section_title == "Ready Tools" else "yellow",
                width=40
            )
            cards.append(card)
        
        # Display cards in columns
        if len(cards) > 1:
            console.print(Columns(cards, equal=True, expand=True))
        else:
            console.print(cards[0])


def show_usage_tips():
    """Show usage tips and next steps."""
    tips_text = Text.assemble(
        ("💡 Quick Start Tips", "bold yellow"),
        "\n\n",
        ("🎯 For Cursor users: ", "dim"),
        ("cursorrules-architect generate --tool cursor /path/to/project", "green"),
        "\n",
        ("🌊 For Windsurf users: ", "dim"),
        ("cursorrules-architect generate --tool windsurf /path/to/project", "green"),
        "\n",
        ("🔧 For Cline users: ", "dim"),
        ("cursorrules-architect generate --tool cline /path/to/project", "green"),
        "\n",
        ("🚀 For all tools: ", "dim"),
        ("cursorrules-architect generate --tool all /path/to/project", "green"),
        "\n\n",
        ("📚 Learn more: ", "dim"),
        ("cursorrules-architect generate --help", "blue"),
    )
    
    console.print(Panel(tips_text, title="Usage Tips", border_style="blue"))
    
    # Show statistics
    ready_count = len(AI_TOOLS_2025["ready"])
    coming_count = len(AI_TOOLS_2025["coming_soon"])
    total_count = ready_count + coming_count
    
    stats_text = f"📊 [bold]Status:[/] {ready_count} ready • {coming_count} coming soon • {total_count} total"
    console.print(f"\n{stats_text}")
    console.print("[dim]More tools are added regularly. Check back for updates![/]")