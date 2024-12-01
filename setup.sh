#!/bin/bash
echo "Setting up CursorRules Architect..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run setup
python3 -m backend.memory.setup_vector_db

echo "Setup complete! You can now run: python3 cursorrules-architect.py" 