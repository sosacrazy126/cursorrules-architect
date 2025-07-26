"""
config/exclusions.py

This module contains exclusion settings for the project analyzer.
It defines sets of directories, files, and extensions that should be
excluded from the project tree structure and analysis.
"""

# ----------------------------------------------------------------------
# ---[ Excluded Files and Directories Configuration ]---
# ----------------------------------------------------------------------

# These sets define directories, files, and file extensions to exclude
# from the tree structure. This helps to keep the tree clean and
# focused on relevant project files.

EXCLUDED_DIRS = {
    'node_modules', '.next', '.git', 'venv', '__pycache__', '_pycache_',
    'dist', 'build', '.vscode', '.idea', 'coverage',
    '.pytest_cache', '.mypy_cache', 'env', '.env', '.venv',
    'site-packages'
}

EXCLUDED_FILES = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    '.DS_Store', '.env', '.env.local', '.gitignore',
    'README.md', 'LICENSE', '.eslintrc', '.prettierrc',
    'tsconfig.json', 'requirements.txt', 'poetry.lock',
    'Pipfile.lock', '.gitattributes', '.gitconfig', '.gitmodules',
}

EXCLUDED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.ico',
    '.svg', '.mp4', '.mp3', '.pdf', '.zip',
    '.woff', '.woff2', '.ttf', '.eot',
    '.pyc', '.pyo', '.pyd', '.so', '.pkl', '.pickle',
    '.db', '.sqlite', '.log', '.cache'
}
