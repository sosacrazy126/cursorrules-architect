#!/usr/bin/env python3
"""
Modern CLI entry point for CursorRules Architect (2025).

This is the new modern CLI interface using Typer, Rich, and Textual.
Run this instead of main.py for the enhanced experience.
"""

from cli.app import app

if __name__ == "__main__":
    app()