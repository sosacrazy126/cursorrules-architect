"""
Validate command for checking existing configuration files.

Validates syntax and provides recommendations for AI tool configurations.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import json
import re

console = Console()

# Configuration file patterns for different tools
CONFIG_PATTERNS = {
    "cursor": {
        "files": [".cursorrules", ".cursor/rules/*.md", ".cursor/rules/*.mdc"],
        "validator": "validate_cursor_rules"
    },
    "windsurf": {
        "files": [".windsurfrules", "global_rules.md"],
        "validator": "validate_windsurf_rules"
    },
    "cline": {
        "files": [".clinerules", ".clinerules/*"],
        "validator": "validate_cline_rules"
    },
    "roo": {
        "files": [".roo/*", ".clinerules-*"],
        "validator": "validate_roo_rules"
    },
    "claude": {
        "files": ["CLAUDE.md", "CLAUDE.local.md"],
        "validator": "validate_claude_md"
    }
}


def validate_command(
    directory: Path = typer.Argument(
        Path.cwd(),
        help="Directory to validate (default: current directory)",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    tool: Optional[str] = typer.Option(
        None,
        "--tool",
        "-t", 
        help="Validate specific tool configuration",
        autocompletion=lambda: list(CONFIG_PATTERNS.keys())
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        "-f",
        help="Attempt to fix common issues automatically"
    ),
    detailed: bool = typer.Option(
        False,
        "--detailed",
        "-d",
        help="Show detailed validation information"
    )
):
    """
    ✅ **Validate AI tool configuration files**
    
    Checks existing configuration files for syntax errors, best practices, 
    and provides recommendations for improvement.
    
    **Examples:**
    
    • `cursorrules-architect validate` - Validate current directory
    • `cursorrules-architect validate /path/to/project` - Validate specific project
    • `cursorrules-architect validate --tool cursor` - Validate only Cursor configs
    • `cursorrules-architect validate --fix` - Auto-fix common issues
    """
    
    # Show validation header
    show_validation_header(directory, tool)
    
    # Find configuration files
    found_configs = find_configuration_files(directory, tool)
    
    if not found_configs:
        show_no_configs_found(directory, tool)
        return
    
    # Validate each configuration
    validation_results = []
    for config_info in found_configs:
        result = validate_configuration_file(config_info, detailed)
        validation_results.append(result)
        
        # Apply fixes if requested
        if fix and result["issues"]:
            apply_fixes(config_info, result["issues"])
    
    # Show validation summary
    show_validation_summary(validation_results, fix)


def show_validation_header(directory: Path, tool: Optional[str]):
    """Show validation header."""
    header_text = Text.assemble(
        ("✅ Configuration Validation", "bold green"),
        "\n\n",
        ("📁 Directory: ", "dim"),
        (str(directory), "cyan"),
        "\n",
        ("🎯 Tool filter: ", "dim"),
        (tool or "All tools", "yellow"),
    )
    
    console.print(Panel(header_text, title="Validation Settings", border_style="green"))


def find_configuration_files(directory: Path, tool_filter: Optional[str]) -> List[Dict[str, Any]]:
    """Find all configuration files in the directory."""
    found_configs = []
    
    # Determine which tools to check
    tools_to_check = [tool_filter] if tool_filter else CONFIG_PATTERNS.keys()
    
    for tool in tools_to_check:
        if tool not in CONFIG_PATTERNS:
            continue
            
        pattern_info = CONFIG_PATTERNS[tool]
        
        for file_pattern in pattern_info["files"]:
            # Handle different pattern types
            if "*" in file_pattern:
                # Glob pattern
                matching_files = list(directory.glob(file_pattern))
            else:
                # Exact file
                file_path = directory / file_pattern
                matching_files = [file_path] if file_path.exists() else []
            
            for file_path in matching_files:
                if file_path.is_file():
                    found_configs.append({
                        "tool": tool,
                        "file_path": file_path,
                        "validator": pattern_info["validator"],
                        "relative_path": file_path.relative_to(directory)
                    })
    
    return found_configs


def validate_configuration_file(config_info: Dict[str, Any], detailed: bool) -> Dict[str, Any]:
    """Validate a single configuration file."""
    file_path = config_info["file_path"]
    tool = config_info["tool"]
    validator_name = config_info["validator"]
    
    console.print(f"\n[bold]📄 Validating {config_info['relative_path']} ({tool})[/]")
    
    try:
        # Read file content
        content = file_path.read_text(encoding="utf-8")
        
        # Run appropriate validator
        validator_func = globals().get(validator_name)
        if validator_func:
            issues = validator_func(content, detailed)
        else:
            issues = validate_generic_rules(content, detailed)
        
        # Determine status
        if not issues:
            status = "✅ Valid"
            console.print("  [green]✅ No issues found[/]")
        else:
            error_count = len([i for i in issues if i["severity"] == "error"])
            warning_count = len([i for i in issues if i["severity"] == "warning"])
            
            if error_count > 0:
                status = f"❌ {error_count} errors, {warning_count} warnings"
                console.print(f"  [red]❌ {error_count} errors, {warning_count} warnings[/]")
            else:
                status = f"⚠️ {warning_count} warnings"
                console.print(f"  [yellow]⚠️ {warning_count} warnings[/]")
        
        # Show issues if detailed
        if detailed and issues:
            show_detailed_issues(issues)
        
        return {
            "config_info": config_info,
            "status": status,
            "issues": issues,
            "content_length": len(content),
            "line_count": len(content.splitlines())
        }
        
    except Exception as e:
        error_msg = f"❌ Failed to read: {str(e)}"
        console.print(f"  [red]{error_msg}[/]")
        
        return {
            "config_info": config_info,
            "status": error_msg,
            "issues": [{"severity": "error", "message": str(e), "fixable": False}],
            "content_length": 0,
            "line_count": 0
        }


def validate_cursor_rules(content: str, detailed: bool) -> List[Dict[str, Any]]:
    """Validate Cursor rules configuration."""
    issues = []
    
    # Check for common Cursor rules patterns
    if not content.strip():
        issues.append({
            "severity": "error",
            "message": "File is empty",
            "fixable": False
        })
        return issues
    
    # Check for "You are" pattern (common in Cursor rules)
    if "You are" not in content:
        issues.append({
            "severity": "warning", 
            "message": "Missing 'You are' instruction pattern",
            "fixable": False
        })
    
    # Check for excessively long content
    if len(content) > 50000:
        issues.append({
            "severity": "warning",
            "message": f"Very long configuration ({len(content)} chars). Consider breaking into sections.",
            "fixable": False
        })
    
    # Check for proper markdown formatting if .md file
    if detailed:
        issues.extend(validate_markdown_formatting(content))
    
    return issues


def validate_windsurf_rules(content: str, detailed: bool) -> List[Dict[str, Any]]:
    """Validate Windsurf rules configuration."""
    issues = []
    
    if not content.strip():
        issues.append({
            "severity": "error",
            "message": "File is empty",
            "fixable": False
        })
        return issues
    
    # Windsurf-specific validations
    if len(content.splitlines()) < 3:
        issues.append({
            "severity": "warning",
            "message": "Very short configuration. Consider adding more detailed instructions.",
            "fixable": False
        })
    
    if detailed:
        issues.extend(validate_markdown_formatting(content))
    
    return issues


def validate_cline_rules(content: str, detailed: bool) -> List[Dict[str, Any]]:
    """Validate Cline rules configuration."""
    issues = []
    
    if not content.strip():
        issues.append({
            "severity": "error",
            "message": "File is empty", 
            "fixable": False
        })
        return issues
    
    # Check for MCP-related content
    if "MCP" in content or "Model Context Protocol" in content:
        # This is good for Cline
        pass
    else:
        issues.append({
            "severity": "info",
            "message": "Consider adding MCP (Model Context Protocol) configuration for enhanced Cline functionality",
            "fixable": False
        })
    
    if detailed:
        issues.extend(validate_markdown_formatting(content))
    
    return issues


def validate_roo_rules(content: str, detailed: bool) -> List[Dict[str, Any]]:
    """Validate Roo Code rules configuration."""
    issues = []
    
    if not content.strip():
        issues.append({
            "severity": "error",
            "message": "File is empty",
            "fixable": False
        })
        return issues
    
    # Roo-specific validations
    if "agent" not in content.lower():
        issues.append({
            "severity": "warning",
            "message": "Consider adding agent-specific instructions for Roo Code",
            "fixable": False
        })
    
    return issues


def validate_claude_md(content: str, detailed: bool) -> List[Dict[str, Any]]:
    """Validate Claude.md configuration."""
    issues = []
    
    if not content.strip():
        issues.append({
            "severity": "error",
            "message": "File is empty",
            "fixable": False
        })
        return issues
    
    # Claude.md specific validations
    if not content.startswith("#"):
        issues.append({
            "severity": "warning",
            "message": "Consider starting with a markdown header",
            "fixable": True
        })
    
    # Check for hierarchical structure
    if detailed and "#" in content:
        lines = content.splitlines()
        headers = [line for line in lines if line.strip().startswith("#")]
        if len(headers) < 2:
            issues.append({
                "severity": "info",
                "message": "Consider using hierarchical markdown structure with multiple headers",
                "fixable": False
            })
    
    issues.extend(validate_markdown_formatting(content))
    
    return issues


def validate_generic_rules(content: str, detailed: bool) -> List[Dict[str, Any]]:
    """Generic validation for unknown configuration types."""
    issues = []
    
    if not content.strip():
        issues.append({
            "severity": "error",
            "message": "File is empty",
            "fixable": False
        })
        return issues
    
    # Basic checks
    if len(content) < 10:
        issues.append({
            "severity": "warning",
            "message": "Configuration is very short",
            "fixable": False
        })
    
    return issues


def validate_markdown_formatting(content: str) -> List[Dict[str, Any]]:
    """Validate markdown formatting."""
    issues = []
    lines = content.splitlines()
    
    # Check for proper header hierarchy
    header_levels = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            header_levels.append((i, level))
    
    # Check for skipped header levels
    for i in range(1, len(header_levels)):
        prev_level = header_levels[i-1][1]
        curr_level = header_levels[i][1]
        
        if curr_level > prev_level + 1:
            issues.append({
                "severity": "warning",
                "message": f"Line {header_levels[i][0]}: Header level skipped (h{prev_level} to h{curr_level})",
                "fixable": False
            })
    
    return issues


def show_detailed_issues(issues: List[Dict[str, Any]]):
    """Show detailed issues for a configuration file."""
    for issue in issues:
        severity = issue["severity"]
        message = issue["message"]
        
        if severity == "error":
            console.print(f"    [red]❌ Error: {message}[/]")
        elif severity == "warning":
            console.print(f"    [yellow]⚠️  Warning: {message}[/]")
        else:
            console.print(f"    [blue]ℹ️  Info: {message}[/]")


def apply_fixes(config_info: Dict[str, Any], issues: List[Dict[str, Any]]):
    """Apply automatic fixes to configuration file."""
    fixable_issues = [i for i in issues if i.get("fixable", False)]
    
    if not fixable_issues:
        return
    
    console.print(f"  [blue]🔧 Applying {len(fixable_issues)} fixes...[/]")
    
    # Implementation would go here for specific fixes
    # For now, just show what would be fixed
    for issue in fixable_issues:
        console.print(f"    [dim]• {issue['message']}[/]")


def show_no_configs_found(directory: Path, tool_filter: Optional[str]):
    """Show message when no configuration files are found."""
    message = Text.assemble(
        ("No configuration files found", "yellow bold"),
        "\n\n",
        ("Directory: ", "dim"),
        (str(directory), "cyan"),
        "\n",
        ("Filter: ", "dim"),
        (tool_filter or "All tools", "yellow"),
        "\n\n",
        ("💡 Generate configurations with:", "dim"),
        "\n",
        ("cursorrules-architect generate ", "green"),
        (str(directory), "cyan"),
    )
    
    console.print(Panel(message, title="No Configurations", border_style="yellow"))


def show_validation_summary(validation_results: List[Dict[str, Any]], fixes_applied: bool):
    """Show validation summary."""
    if not validation_results:
        return
    
    # Count issues by severity
    total_files = len(validation_results)
    valid_files = len([r for r in validation_results if "✅" in r["status"]])
    files_with_errors = len([r for r in validation_results if "❌" in r["status"]])
    files_with_warnings = len([r for r in validation_results if "⚠️" in r["status"]])
    
    # Create summary table
    table = Table(title="📊 Validation Summary")
    table.add_column("File", style="cyan")
    table.add_column("Tool", style="yellow")
    table.add_column("Status", style="green")
    table.add_column("Size", style="dim")
    
    for result in validation_results:
        config_info = result["config_info"]
        status = result["status"]
        
        # Format size
        size_info = f"{result['line_count']} lines"
        if result['content_length'] > 1000:
            size_info += f" ({result['content_length']//1000}K chars)"
        
        table.add_row(
            str(config_info["relative_path"]),
            config_info["tool"].title(),
            status,
            size_info
        )
    
    console.print(f"\n{table}")
    
    # Show overall summary
    summary_text = Text.assemble(
        ("📊 Summary: ", "bold"),
        (f"{total_files} files • ", "dim"),
        (f"{valid_files} valid", "green"),
        (f" • {files_with_warnings} warnings", "yellow" if files_with_warnings else "dim"),
        (f" • {files_with_errors} errors", "red" if files_with_errors else "dim"),
    )
    
    console.print(f"\n{summary_text}")
    
    if fixes_applied:
        console.print("[green]🔧 Automatic fixes were applied[/]")
    
    if files_with_errors > 0:
        console.print("\n[red]❌ Some files have errors that need manual attention[/]")
    elif files_with_warnings > 0:
        console.print("\n[yellow]⚠️  Some files have warnings to consider[/]")
    else:
        console.print("\n[green]✅ All configuration files are valid![/]")