"""Configuration screen placeholder."""

from textual.screen import Screen
from textual.widgets import Static


class ConfigurationScreen(Screen):
    """Configuration screen."""
    
    def compose(self):
        yield Static("Configuration Screen - Coming Soon")