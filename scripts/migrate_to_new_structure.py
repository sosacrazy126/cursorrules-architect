#!/usr/bin/env python3
"""
Migration script to move from old structure to new organized structure.

This script helps migrate existing installations to the new clean structure.
"""

import shutil
import sys
from pathlib import Path


def main():
    """Main migration function."""
    print("🚀 CursorRules Architect - Structure Migration")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    
    # Check if we're in the right directory
    if not (project_root / "main.py").exists():
        print("❌ Error: Run this script from the project root directory")
        sys.exit(1)
    
    print(f"📁 Project root: {project_root}")
    
    # Create backup
    backup_dir = project_root / "backup_old_structure"
    if backup_dir.exists():
        print(f"🗑️  Removing existing backup: {backup_dir}")
        shutil.rmtree(backup_dir)
    
    print(f"💾 Creating backup: {backup_dir}")
    backup_dir.mkdir()
    
    # Backup old files
    old_files = [
        "main.py",
        "modern_cli.py", 
        "demo_blueprint.py",
        "cli/",
        "core/",
        "config/",
        "requirements.txt",
    ]
    
    for item in old_files:
        old_path = project_root / item
        if old_path.exists():
            if old_path.is_dir():
                shutil.copytree(old_path, backup_dir / item)
            else:
                shutil.copy2(old_path, backup_dir / item)
            print(f"   ✓ Backed up: {item}")
    
    # Remove old structure (keep important files)
    keep_files = {
        ".git", ".gitignore", "README.md", "LICENSE", 
        "CHANGELOG.md", "CONTRIBUTING.md", ".env",
        "phases_output", "tests", "PROMPTS",
        "analysis_memory.db", "analysis_memory.json",
        ".cursorrules", ".cursorignore"
    }
    
    print("\n🧹 Cleaning old structure...")
    for item in project_root.iterdir():
        if item.name not in keep_files and item.name != "backup_old_structure" and not item.name.startswith("src"):
            if item.is_dir():
                print(f"   🗑️  Removing directory: {item.name}")
                shutil.rmtree(item)
            else:
                print(f"   🗑️  Removing file: {item.name}")
                item.unlink()
    
    print("\n✅ Migration completed!")
    print("\n📋 Next steps:")
    print("1. Install the package in development mode:")
    print("   pip install -e .")
    print("2. Test the new CLI:")
    print("   cursorrules-architect --help")
    print("3. If everything works, you can remove the backup:")
    print(f"   rm -rf {backup_dir}")
    
    print("\n🎉 Welcome to the new CursorRules Architect structure!")


if __name__ == "__main__":
    main()
