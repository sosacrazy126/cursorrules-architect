"""Welcome screen for the TUI application."""

from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical
from textual.app import ComposeResult


class WelcomeScreen(Screen):
    """Welcome and help screen."""
    
    CSS = """
    .welcome-container {
        align: center middle;
        width: 80%;
        height: 80%;
        border: solid $primary;
        background: $surface;
    }
    
    .welcome-content {
        padding: 2;
        text-align: center;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(classes="welcome-container"):
            with Vertical(classes="welcome-content"):
                yield Static("""
# 🚀 Welcome to CursorRules Architect

## Modern AI Configuration Generator (2025)

Generate optimized configuration files for all major AI coding tools:

**Supported Tools:**
• 🎯 Cursor - AI-first code editor (.cursor/rules/)
• 🌊 Windsurf - Agentic IDE (.windsurfrules)  
• 🔧 Cline - VS Code extension (.clinerules/)
• 🦘 Roo Code - AI dev team (.roo/)
• 🧠 Claude Code - Official Anthropic CLI (CLAUDE.md)

**Features:**
• Interactive directory browser
• Live configuration preview
• Multi-format generation
• Validation and error checking
• Modern terminal UI with Rich styling

**Quick Start:**
1. Select your project directory
2. Choose target AI tool
3. Preview configuration
4. Generate files

Press Enter to continue or Q to quit.
                """)
                yield Button("Continue", id="continue_btn", variant="primary")
    
    def on_button_pressed(self, event) -> None:
        if event.button.id == "continue_btn":
            self.dismiss()
    
    def on_key(self, event) -> None:
        if event.key == "enter":
            self.dismiss()
        elif event.key == "q":
            self.app.exit()