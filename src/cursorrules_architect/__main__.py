"""
Main entry point for running CursorRules Architect as a module.

This allows the package to be executed with:
    python -m cursorrules_architect
"""

from .cli.main import app

if __name__ == "__main__":
    app()
