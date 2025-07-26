#!/usr/bin/env python3
"""
Script to fix import statements in the reorganized package structure.

This script updates all import statements from the old structure to the new
package structure with relative imports.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path: Path, src_root: Path):
    """Fix imports in a single Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Calculate relative path from file to src root
        relative_path = file_path.relative_to(src_root)
        depth = len(relative_path.parts) - 1  # -1 because we don't count the file itself
        
        # Create the appropriate number of dots for relative imports
        if depth == 0:
            prefix = "."
        else:
            prefix = "." * (depth + 1)
        
        # Fix imports from core, config, cli modules
        patterns = [
            (r'^from core\.', f'from {prefix}core.'),
            (r'^from config\.', f'from {prefix}config.'),
            (r'^from cli\.', f'from {prefix}cli.'),
            (r'^import core\.', f'import {prefix}core.'),
            (r'^import config\.', f'import {prefix}config.'),
            (r'^import cli\.', f'import {prefix}cli.'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # Special case: fix imports from main module
        if 'from main import' in content:
            content = re.sub(r'^from main import', f'from {prefix}main import', content, flags=re.MULTILINE)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all imports."""
    src_root = Path(__file__).parent.parent / "src" / "cursorrules_architect"
    
    if not src_root.exists():
        print(f"Source root not found: {src_root}")
        return
    
    print(f"Fixing imports in: {src_root}")
    
    # Find all Python files
    python_files = list(src_root.rglob("*.py"))
    
    fixed_count = 0
    for py_file in python_files:
        if fix_imports_in_file(py_file, src_root):
            fixed_count += 1
    
    print(f"\nFixed imports in {fixed_count} files out of {len(python_files)} Python files.")

if __name__ == "__main__":
    main()
