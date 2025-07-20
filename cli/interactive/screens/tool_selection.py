"""Tool selection screen placeholder."""

from textual.screen import Screen
from textual.widgets import Static


class ToolSelectionScreen(Screen):
    """Tool selection screen."""
    
    def compose(self):
        yield Static("Tool Selection Screen - Coming Soon")