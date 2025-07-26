# CursorRules Architect Documentation

Welcome to the CursorRules Architect documentation! This tool helps you generate AI assistant configurations for modern development environments.

## Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/sosacrazy126/cursorrules-architect.git
cd cursorrules-architect
pip install -e .

# Or install development version
pip install -e .[dev]
```

### Basic Usage

```bash
# Generate configuration for your project
cursorrules-architect generate /path/to/your/project

# Generate for specific AI tool
cursorrules-architect generate /path/to/your/project --tool windsurf

# List supported tools
cursorrules-architect list

# Validate existing configuration
cursorrules-architect validate .cursorrules
```

## Configuration

### Environment Variables

Set up your AI provider API keys:

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_API_KEY="your-google-key"
```

### Configuration File

Create a `cursorrules.yaml` file in your project root:

```yaml
# Analysis settings
max_file_size: 1048576  # 1MB
max_files_per_agent: 50
enable_context_engineering: false
parallel_execution: true

# Timeouts
phase_timeout: 300  # 5 minutes
total_timeout: 1800  # 30 minutes

# Output settings
output:
  generate_cursorrules: true
  generate_cursorignore: true
  generate_phase_outputs: true
  output_format: "markdown"
  include_project_structure: true

# File exclusions
exclusions:
  directories:
    - "__pycache__"
    - ".git"
    - "node_modules"
    - "dist"
    - "build"
  files:
    - "*.pyc"
    - "*.log"
    - ".DS_Store"
  extensions:
    - ".tmp"
    - ".cache"
```

## Architecture

### Analysis Pipeline

The tool uses a 6-phase analysis pipeline:

1. **Phase 1: Initial Discovery** - Parallel analysis of project structure, dependencies, and tech stack
2. **Phase 2: Methodical Planning** - Creates detailed analysis plan and agent assignments
3. **Phase 3: Deep Analysis** - Specialized agents analyze assigned files in detail
4. **Phase 4: Synthesis** - Combines findings from all agents
5. **Phase 5: Consolidation** - Creates comprehensive project report
6. **Final Analysis** - Generates AI tool-specific configuration

### AI Model Support

- **Anthropic Claude** - Full support with reasoning mode
- **OpenAI GPT/O1** - Full support with different reasoning levels
- **Google Gemini** - Full support with configurable parameters
- **DeepSeek** - Basic support (experimental)

## Output Files

The tool generates several output files:

```
your-project/
├── .cursorrules              # Main AI assistant configuration
├── .cursorignore            # File patterns to ignore
└── phases_output/           # Detailed analysis results
    ├── phase1_discovery.md
    ├── phase2_planning.md
    ├── phase3_analysis.md
    ├── phase4_synthesis.md
    ├── phase5_consolidation.md
    ├── final_analysis.md
    └── summary.md
```

## Development

### Setting Up Development Environment

```bash
# Clone and install
git clone https://github.com/sosacrazy126/cursorrules-architect.git
cd cursorrules-architect

# Install development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Run linting
make lint
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/cursorrules_architect

# Run specific test file
pytest tests/unit/test_config.py

# Run integration tests
pytest tests/integration/
```

### Code Quality

The project uses several tools for code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **pre-commit** - Git hooks

## Troubleshooting

### Common Issues

**API Key Errors**
```bash
# Make sure your API keys are set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
echo $GOOGLE_API_KEY
```

**Permission Errors**
```bash
# Make sure you have read access to the project directory
ls -la /path/to/your/project
```

**Large Project Analysis**
```bash
# For large projects, increase timeouts
export CRA_PHASE_TIMEOUT=600
export CRA_MAX_FILES_PER_AGENT=100
```

### Debug Mode

Enable verbose logging:

```bash
cursorrules-architect generate /path/to/project --verbose
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](../LICENSE) for details.
