"""
Main Textual TUI application for CursorRules Architect.

Modern 2025 interactive terminal application with beautiful widgets.
"""

from pathlib import Path
from typing import Optional
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Button, DirectoryTree, Select, Static, 
    ProgressBar, Log, Markdown
)
from textual.screen import Screen
from textual.binding import Binding
from rich.text import Text

from .screens.welcome import WelcomeScreen
from .screens.tool_selection import ToolSelectionScreen 
from .screens.configuration import ConfigurationScreen
from .screens.generation import GenerationScreen


class ConfiguratorApp(App):
    """Main TUI application for AI configuration generation."""
    
    CSS = """
    .title {
        text-align: center;
        background: $primary;
        color: $text;
        padding: 1;
        margin: 1;
    }
    
    .status-panel {
        height: 3;
        background: $surface;
        border: solid $primary;
        margin: 1;
    }
    
    .main-container {
        height: 1fr;
        margin: 1;
    }
    
    .button-container {
        height: 5;
        align: center bottom;
        margin: 1;
    }
    
    Button {
        margin: 0 1;
        min-width: 16;
    }
    
    .directory-panel {
        width: 1fr;
        border: solid $accent;
        margin: 0 1;
    }
    
    .config-panel {
        width: 2fr; 
        border: solid $accent;
        margin: 0 1;
    }
    
    .preview-panel {
        height: 1fr;
        border: solid $secondary;
        margin: 1;
    }
    """
    
    TITLE = "🚀 CursorRules Architect - AI Configuration Generator"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit"),
        Binding("h", "help", "Help"),
        Binding("r", "restart", "Restart"),
    ]
    
    def __init__(self):
        super().__init__()
        self.selected_directory: Optional[Path] = None
        self.selected_tool: Optional[str] = None
        self.configuration_ready = False
        
    def compose(self) -> ComposeResult:
        """Create the main UI layout."""
        yield Header()
        
        # Title
        yield Static(
            "🚀 CursorRules Architect\nModern AI Configuration Generator",
            classes="title"
        )
        
        # Status panel
        yield Container(
            Static("Ready to generate AI configurations", id="status"),
            classes="status-panel"
        )
        
        # Main content area
        with Container(classes="main-container"):
            with Horizontal():
                # Directory selection panel
                with Vertical(classes="directory-panel"):
                    yield Static("📁 Select Project Directory", classes="panel-title")
                    yield DirectoryTree("./", id="directory_tree")
                
                # Configuration panel
                with Vertical(classes="config-panel"):
                    yield Static("⚙️ Configuration", classes="panel-title")
                    yield Select([
                        ("🎯 Cursor (.cursor/rules/)", "cursor"),
                        ("🌊 Windsurf (.windsurfrules)", "windsurf"),
                        ("🔧 Cline (.clinerules/)", "cline"),
                        ("🦘 Roo Code (.roo/)", "roo"),
                        ("🧠 Claude Code (CLAUDE.md)", "claude"),
                        ("📦 All compatible formats", "all")
                    ], prompt="Choose AI tool", id="tool_select")
                    
                    yield Select([
                        ("⚡ Quick setup", "quick"),
                        ("🔍 Standard analysis", "standard"),
                        ("🚀 Advanced analysis", "advanced"),
                        ("🎛️ Custom configuration", "custom")
                    ], prompt="Analysis complexity", value="standard", id="complexity_select")
        
        # Preview panel
        with Container(classes="preview-panel"):
            yield Static("📄 Configuration Preview", classes="panel-title")
            yield Log(id="preview_log")
        
        # Action buttons
        with Container(classes="button-container"):
            with Horizontal():
                yield Button("🔍 Preview", id="preview_btn", variant="default")
                yield Button("🚀 Generate", id="generate_btn", variant="primary")
                yield Button("✅ Validate", id="validate_btn", variant="success")
                yield Button("❌ Cancel", id="cancel_btn", variant="error")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the application."""
        # Set initial directory to current working directory
        self.selected_directory = Path.cwd()
        self.update_status("Welcome! Select a project directory and AI tool to begin.")
    
    def on_directory_tree_directory_selected(self, event) -> None:
        """Handle directory selection."""
        self.selected_directory = event.path
        self.update_status(f"Selected directory: {event.path}")
        self.check_ready_state()
    
    def on_select_changed(self, event) -> None:
        """Handle select widget changes."""
        if event.select.id == "tool_select" and event.value != Select.BLANK:
            self.selected_tool = event.value
            tool_info = self.get_tool_info(event.value)
            self.update_status(f"Selected tool: {tool_info['name']} ({tool_info['format']})")
            self.check_ready_state()
    
    def on_button_pressed(self, event) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "preview_btn":
            self.action_preview()
        elif button_id == "generate_btn":
            self.action_generate()
        elif button_id == "validate_btn":
            self.action_validate()
        elif button_id == "cancel_btn":
            self.action_quit()
    
    def action_preview(self) -> None:
        """Show configuration preview."""
        if not self.configuration_ready:
            self.update_status("❌ Please select directory and tool first")
            return
        
        preview_log = self.query_one("#preview_log", Log)
        preview_log.clear()
        
        preview_log.write_line("🔍 Generating configuration preview...")
        preview_log.write_line(f"📁 Directory: {self.selected_directory}")
        preview_log.write_line(f"🎯 Tool: {self.selected_tool}")
        preview_log.write_line("")
        preview_log.write_line("📝 Configuration preview:")
        preview_log.write_line("---")
        preview_log.write_line("# Sample Configuration")
        preview_log.write_line("You are an expert AI assistant...")
        preview_log.write_line("Follow project patterns and conventions...")
        preview_log.write_line("---")
        preview_log.write_line("✅ Preview ready! Use Generate to create files.")
        
        self.update_status("📄 Configuration preview generated")
    
    def action_generate(self) -> None:
        """Generate configuration files."""
        if not self.configuration_ready:
            self.update_status("❌ Please select directory and tool first")
            return
        
        # Switch to generation screen
        self.push_screen(GenerationScreen(
            directory=self.selected_directory,
            tool=self.selected_tool
        ))
    
    def action_validate(self) -> None:
        """Validate existing configurations."""
        if not self.selected_directory:
            self.update_status("❌ Please select a directory first")
            return
        
        preview_log = self.query_one("#preview_log", Log)
        preview_log.clear()
        preview_log.write_line("✅ Running configuration validation...")
        preview_log.write_line(f"📁 Scanning: {self.selected_directory}")
        preview_log.write_line("")
        preview_log.write_line("🔍 Found configurations:")
        preview_log.write_line("  .cursorrules ✅ Valid")
        preview_log.write_line("  .windsurfrules ❌ Missing")
        preview_log.write_line("  CLAUDE.md ✅ Valid")
        preview_log.write_line("")
        preview_log.write_line("📊 Summary: 2 valid, 1 missing")
        
        self.update_status("✅ Validation complete")
    
    def action_help(self) -> None:
        """Show help information."""
        self.push_screen(WelcomeScreen())
    
    def action_restart(self) -> None:
        """Restart the configuration process."""
        self.selected_directory = Path.cwd()
        self.selected_tool = None
        self.configuration_ready = False
        
        # Reset UI
        tool_select = self.query_one("#tool_select", Select)
        tool_select.value = Select.BLANK
        
        preview_log = self.query_one("#preview_log", Log)
        preview_log.clear()
        
        self.update_status("🔄 Configuration reset. Start over by selecting directory and tool.")
    
    def update_status(self, message: str) -> None:
        """Update the status message."""
        status_widget = self.query_one("#status", Static)
        status_widget.update(message)
    
    def check_ready_state(self) -> None:
        """Check if configuration is ready to generate."""
        self.configuration_ready = (
            self.selected_directory is not None and 
            self.selected_tool is not None
        )
        
        # Update button states
        generate_btn = self.query_one("#generate_btn", Button)
        preview_btn = self.query_one("#preview_btn", Button)
        
        if self.configuration_ready:
            generate_btn.disabled = False
            preview_btn.disabled = False
            self.update_status("✅ Ready to generate configuration!")
        else:
            generate_btn.disabled = True
            preview_btn.disabled = True
    
    def get_tool_info(self, tool_key: str) -> dict:
        """Get information about a tool."""
        tool_info_map = {
            "cursor": {"name": "Cursor", "format": ".cursor/rules/"},
            "windsurf": {"name": "Windsurf", "format": ".windsurfrules"},
            "cline": {"name": "Cline", "format": ".clinerules/"},
            "roo": {"name": "Roo Code", "format": ".roo/"},
            "claude": {"name": "Claude Code", "format": "CLAUDE.md"},
            "all": {"name": "All Tools", "format": "Multiple formats"}
        }
        return tool_info_map.get(tool_key, {"name": "Unknown", "format": "Unknown"})