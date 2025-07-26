# 🚀 CursorRules Architect

**Modern AI Agent Configuration Generator for Development Tools**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

CursorRules Architect is a powerful tool that analyzes your codebase and generates optimized AI assistant configurations for modern development environments like Cursor, Windsurf, and other AI-powered IDEs.

## ✨ Features

- 🔍 **Multi-Phase Analysis Pipeline** - Comprehensive 6-phase project analysis
- 🤖 **Multi-Provider AI Support** - Anthropic Claude, OpenAI GPT/O1, Google Gemini
- 📁 **Smart Project Understanding** - Analyzes structure, dependencies, and patterns
- ⚙️ **Configurable Analysis** - Customizable models and analysis parameters
- 📄 **Multiple Output Formats** - Generates .cursorrules, .cursorignore, and detailed reports
- 🎯 **Tool-Specific Optimization** - Tailored configurations for different AI tools
- 🧪 **Comprehensive Testing** - Full test suite with unit and integration tests

## 🚀 Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/sosacrazy126/cursorrules-architect.git
cd cursorrules-architect
pip install -e .

# Or install with development dependencies
pip install -e .[dev]
```

### Setup API Keys

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_API_KEY="your-google-key"
```

### Basic Usage

```bash
# Analyze your project
cursorrules-architect generate /path/to/your/project

# Generate for specific AI tool
cursorrules-architect generate /path/to/your/project --tool windsurf

# List supported tools
cursorrules-architect list

# Validate existing configuration
cursorrules-architect validate .cursorrules
```

## 📖 Documentation

### Command Line Interface

```bash
# Generate configuration
cursorrules-architect generate [PROJECT_PATH] [OPTIONS]

Options:
  --tool TEXT        Target AI tool (cursor, windsurf, etc.)
  --output PATH      Output directory
  --force           Overwrite existing files
  --verbose         Enable verbose logging
  --help            Show help message

# List supported tools
cursorrules-architect list

# Validate configuration
cursorrules-architect validate [CONFIG_PATH]
```

### Configuration

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

# Model configuration per phase
phase_models:
  phase1:
    provider: "gemini"
    model_name: "gemini-2.5-flash-preview-05-20"
    reasoning: "disabled"
  phase2:
    provider: "gemini"
    model_name: "gemini-2.5-flash-preview-05-20"
    reasoning: "enabled"
```

## 🏗️ Architecture

### Analysis Pipeline

The tool uses a sophisticated 6-phase analysis pipeline:

1. **Phase 1: Initial Discovery** - Parallel analysis with specialized agents
   - Structure Agent: Analyzes project organization
   - Dependency Agent: Investigates package dependencies  
   - Tech Stack Agent: Identifies frameworks and technologies

2. **Phase 2: Methodical Planning** - Creates detailed analysis strategy
   - Generates specialized agents for Phase 3
   - Assigns files to agents based on expertise
   - Plans analysis priorities and focus areas

3. **Phase 3: Deep Analysis** - Specialized file-level analysis
   - Dynamic agent creation based on Phase 2 plan
   - Detailed code analysis and pattern recognition
   - Architecture and design pattern identification

4. **Phase 4: Synthesis** - Combines findings from all agents
   - Identifies cross-cutting concerns
   - Synthesizes architectural insights
   - Generates coherent project understanding

5. **Phase 5: Consolidation** - Creates comprehensive report
   - Consolidates all analysis results
   - Generates actionable recommendations
   - Prepares final project assessment

6. **Final Analysis** - Generates AI tool configurations
   - Creates .cursorrules file with project-specific instructions
   - Generates .cursorignore with appropriate exclusions
   - Tailors output for specific AI tools

### Supported AI Providers

- **Anthropic Claude** - Full support with reasoning mode
- **OpenAI GPT/O1/O3** - Complete integration with different reasoning levels
- **Google Gemini** - Full support with configurable parameters
- **DeepSeek** - Basic support (experimental)

## 📁 Output Structure

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

## 🛠️ Development

### Setup Development Environment

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

# Run all checks
make check
```

### Project Structure

```
src/cursorrules_architect/
├── cli/                     # Command-line interface
├── config/                  # Configuration management
├── core/                    # Core analysis engine
│   ├── analysis/           # Analysis pipeline
│   └── agents/             # AI agent implementations
└── utils/                   # Utility modules
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/cursorrules_architect

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING_NEW.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `make check`
5. Commit your changes: `git commit -m 'feat: add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Inspired by the need for better AI assistant configurations
- Built with modern Python best practices and comprehensive testing

---

**Made with ❤️ for the developer community**
