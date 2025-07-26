"""
Main CLI entry point for CursorRules Architect.

This module provides the main entry point for the CLI application,
exporting the Typer app from app.py for use by setuptools entry points.
"""

from .app import app

# Export the app for setuptools entry points
__all__ = ["app"]

if __name__ == "__main__":
    app()