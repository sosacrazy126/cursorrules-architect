#!/usr/bin/env python3

from pathlib import Path
import typer
from rich import print
from rich.tree import Tree
from rich.console import Console
from rich.prompt import Prompt, Confirm
import sys
import time
import watchdog.events
import watchdog.observers
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = typer.Typer()

def should_exclude(path: Path, exclude_dirs: set[str]) -> bool:
    """Determine if a path should be excluded."""
    # Directories to exclude
    if path.is_dir() and (path.name in exclude_dirs or path.name.startswith('.')):
        return True
        
    # File extensions to exclude
    excluded_extensions = {
        '.svg', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp',  # Images
        '.lock', '.log',  # Lock and log files
        '.map', '.min.js', '.min.css',  # Generated/minified files
        '.woff', '.woff2', '.ttf', '.eot',  # Fonts
        '.mp4', '.webm', '.ogg', '.mp3', '.wav',  # Media files
        '.pdf', '.doc', '.docx', '.xls', '.xlsx',  # Documents
        '.pyc', '.pyo', '.pyd',  # Python compiled files
    }
    
    # Specific files to exclude
    excluded_files = {
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',  # Package locks
        '.gitignore', '.gitattributes', '.gitmodules',  # Git files
        'LICENSE', 'LICENSE.md', 'LICENSE.txt',  # License files
        'CHANGELOG.md', 'CONTRIBUTING.md',  # Project docs
        '__init__.py',  # Empty Python init files
        'requirements.txt', 'Pipfile.lock',  # Python dependency files
        'poetry.lock', 'Cargo.lock',  # More lock files
        '.npmrc', '.yarnrc', '.npmignore',  # Package manager configs
        'tsconfig.tsbuildinfo',  # TypeScript build info
        'CNAME', 'robots.txt', 'sitemap.xml',  # Web files
        'Thumbs.db', '.DS_Store', 'desktop.ini',  # System files
        'LICENSE-MIT', 'LICENSE-APACHE',  # More license variants
        'NOTICE', 'PATENTS', 'AUTHORS',  # Legal files
        'yarn-error.log', 'npm-debug.log',  # Error logs
        '.eslintignore', '.prettierignore',  # Tool ignore files
        'babel.config.js', 'jest.config.js',  # Tool configs
        '.editorconfig',  # Editor configs
    }
    
    # Files to always include even if they start with .
    important_files = {
        '.env', '.env.test', '.env.local', '.env.development',
        '.env.production', '.env.example'
    }
    
    if path.name in important_files:
        return False
        
    return (path.suffix.lower() in excluded_extensions or 
            path.name in excluded_files or
            (path.name.startswith('.') and path.name not in important_files))

def generate_tree(directory: Path, tree: Tree, exclude_dirs: set[str] = None) -> None:
    """Recursively generate a directory tree."""
    if exclude_dirs is None:
        exclude_dirs = {
            'node_modules', '__pycache__', '.next', 'build', 'dist',
            'coverage', '.pytest_cache', '.sass-cache', '.turbo',
            'out', '.output', '.nuxt', '.cache', '.parcel-cache',
            'vendor', 'tmp', 'temp', '.temp', '.idea', '.vscode',
            'venv', '.venv', 'env', '.env', '.tox', 'eggs',
            '.mypy_cache', '.ruff_cache', '.pytest_cache',
            'htmlcov', '.coverage', '.hypothesis'
        }
    
    try:
        # Sort directories first, then files
        paths = sorted(directory.iterdir(), 
                      key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for path in paths:
            if should_exclude(path, exclude_dirs):
                continue
                
            # Create new branch
            if path.is_dir():
                branch = tree.add(f"📁 {path.name}")
                generate_tree(path, branch, exclude_dirs)
            else:
                tree.add(f"📄 {path.name}")
    except PermissionError:
        tree.add("[red]⚠️ Permission denied[/red]")

def save_tree_to_markdown(tree_str: str, output_file: Path) -> None:
    """Save the tree to a markdown file."""
    content = f"""# Project Directory Structure
------------------------------
```
{tree_str}
```
"""
    output_file.write_text(content)

class FileChangeHandler(FileSystemEventHandler):
    """Handle file system events and update the .cursorrules file."""
    def __init__(self, root_path: Path, cursorrules_path: Path, exclude_dirs: set[str]):
        self.root_path = root_path
        self.cursorrules_path = cursorrules_path
        self.exclude_dirs = exclude_dirs
        self.update_cursorrules()

    def on_any_event(self, event):
        # Ignore directory modifications and temporary files
        if event.is_directory or any(part.startswith('.') for part in Path(event.src_path).parts):
            return
        
        # Wait a brief moment to let all related changes complete
        time.sleep(0.5)
        self.update_cursorrules()
        print(f"\n[green]✓[/green] Updated .cursorrules after detecting changes")

    def update_cursorrules(self):
        """Generate new tree and update .cursorrules file."""
        # Create new tree
        tree = Tree(f"📁 {self.root_path.name}")
        generate_tree(self.root_path, tree, self.exclude_dirs)
        
        # Get tree as string
        console_str = Console(record=True)
        console_str.print(tree)
        tree_str = console_str.export_text()
        
        # Read existing .cursorrules content
        if self.cursorrules_path.exists():
            content = self.cursorrules_path.read_text()
            
            # Define markers with more flexible whitespace handling
            start_marker = "<!-- BEGIN_STRUCTURE -->"
            end_marker = "<!-- END_STRUCTURE -->"
            
            # Find the markers
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker, start_idx + len(start_marker)) if start_idx != -1 else -1
            
            if start_idx != -1 and end_idx != -1:
                # Extract the content before and after the structure section
                before_content = content[:start_idx]
                after_content = content[end_idx + len(end_marker):]
                
                # Create the new structure section
                new_structure = f"{start_marker}\n# Project Directory Structure\n------------------------------\n```\n{tree_str}```\n{end_marker}"
                
                # Combine all parts
                new_content = f"{before_content}{new_structure}{after_content}"
                self.cursorrules_path.write_text(new_content)
            else:
                # If markers not found, create new section with tags
                print("\n[yellow]Warning: Could not find tree section in .cursorrules. Creating new section.[/yellow]")
                if not content.strip():
                    # If file is empty or only whitespace
                    new_content = f"{start_marker}\n# Project Directory Structure\n------------------------------\n```\n{tree_str}```\n{end_marker}"
                else:
                    # Append to existing content
                    new_content = f"{content.rstrip()}\n\n{start_marker}\n# Project Directory Structure\n------------------------------\n```\n{tree_str}```\n{end_marker}"
                self.cursorrules_path.write_text(new_content)

@app.command()
def main(
    path: str = typer.Option(".", help="Root directory path to generate tree from"),
    output: str = typer.Option("docs/directory_structure.md", help="Output markdown file path"),
    exclude: str = typer.Option("", help="Additional directories to exclude (comma-separated)"),
) -> None:
    """Generate a directory tree visualization with interactive mode selection."""
    console = Console()
    
    # Print welcome message
    console.print("\n[bold blue]Directory Tree Generator[/bold blue]")
    console.print("================================\n")
    
    # Interactive mode selection
    choices = {
        "1": "Generate directory tree only",
        "2": "Generate tree and monitor for changes",
        "3": "Generate tree and update .cursorrules",
        "4": "Generate tree, update .cursorrules, and monitor for changes",
        "q": "Quit"
    }
    
    # Display menu
    console.print("[yellow]Please select an option:[/yellow]")
    for key, value in choices.items():
        console.print(f"  {key}) {value}")
    
    choice = Prompt.ask("\nEnter your choice", choices=list(choices.keys()))
    
    if choice == "q":
        console.print("\n[yellow]Goodbye![/yellow]")
        return
    
    # Get paths
    root_path = Path(path).resolve()
    output_path = Path(output)
    cursorrules_path = root_path / ".cursorrules"
    
    # Create exclude set
    exclude_dirs = {
        'node_modules', '__pycache__', '.next', 'build', 'dist',
        'coverage', '.pytest_cache', '.sass-cache', '.turbo',
        'out', '.output', '.nuxt', '.cache', '.parcel-cache',
        'vendor', 'tmp', 'temp', '.temp', '.idea', '.vscode',
        'venv', '.venv', 'env', '.env', '.tox', 'eggs',
        '.mypy_cache', '.ruff_cache', '.pytest_cache',
        'htmlcov', '.coverage', '.hypothesis'
    }
    if exclude:
        exclude_dirs.update(exclude.split(','))
    
    # Create initial tree
    tree = Tree(f"📁 {root_path.name}")
    generate_tree(root_path, tree, exclude_dirs)
    
    # Save to markdown file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    console_str = Console(record=True)
    console_str.print(tree)
    save_tree_to_markdown(console_str.export_text(), output_path)
    
    print(f"\n[green]✓[/green] Directory tree generated and saved to: [blue]{output_path}[/blue]")
    
    # Handle different modes
    if choice in ["3", "4"]:
        # Update .cursorrules
        event_handler = FileChangeHandler(root_path, cursorrules_path, exclude_dirs)
        print(f"\n[green]✓[/green] Updated .cursorrules file")
    
    if choice in ["2", "4"]:
        # Start monitoring
        print("\n[yellow]Starting file system monitor...[/yellow]")
        if choice == "2":
            event_handler = FileChangeHandler(root_path, cursorrules_path, exclude_dirs)
        observer = Observer()
        observer.schedule(event_handler, str(root_path), recursive=True)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\n[yellow]Stopping monitor...[/yellow]")
        observer.join()
    else:
        print("\nPreview of the generated tree:")
        console.print(tree)

if __name__ == "__main__":
    app()
