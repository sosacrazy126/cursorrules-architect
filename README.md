# 🧠 CursorRules Architect

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-o1%20%7C%20o3--mini%20%7C%20gpt--4o-blue.svg)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-claude--3.7--sonnet-purple.svg)](https://www.anthropic.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-deepseek--reasoner-red.svg)](https://deepseek.com/)
[![Google](https://img.shields.io/badge/Google-gemini--2.0--flash%20%7C%20gemini--2.5--pro-green.svg)](https://ai.google.dev/)

**AI-powered project analysis and configuration generator for development tools**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](docs/) • [Contributing](docs/CONTRIBUTING.md)

</div>

## 🌟 Overview

CursorRules Architect is a sophisticated AI-powered tool that analyzes your codebase and generates optimized configurations for AI development tools like Cursor, Windsurf, Cline, and more. Using a multi-phase analysis pipeline with support for multiple AI providers, it creates intelligent `.cursorrules` files and tool-specific configurations that enhance your AI-assisted development experience.

### Key Capabilities

- **🤖 Multi-AI Provider Support** - Works with Anthropic Claude, OpenAI (o1, o3-mini, GPT-4o), DeepSeek, and Google Gemini
- **🎯 Universal Tool Support** - Generates configurations for Cursor, Windsurf, Cline, Roo Code, Claude Code CLI, and more
- **📊 6-Phase Analysis Pipeline** - Comprehensive project understanding through structured analysis phases
- **⚡ Modern CLI Interface** - Rich terminal UI with preview modes and interactive tool selection
- **🔧 Highly Configurable** - Customize AI models, analysis phases, and output formats

## ✨ Features

### 🚀 AI-Powered Analysis
- **Multi-Provider Support** - Anthropic Claude, OpenAI (o1, o3-mini, GPT-4o), DeepSeek, Google Gemini
- **Dynamic Agent Creation** - Specialized analysis agents based on your codebase
- **6-Phase Pipeline** - Structured analysis from discovery to final recommendations
- **Parallel Processing** - Async execution for faster analysis

### 🎯 Universal Tool Support
- **Cursor IDE** - `.cursorrules` files optimized for Cursor
- **Windsurf** - `.windsurfrules` for agentic development
- **Cline** - `.clinerules` for VS Code extension
- **Roo Code** - `.roorules` for AI development teams
- **Claude Code CLI** - `CLAUDE.md` context files
- **Preview Mode** - See configurations before saving

### 🛠️ Developer Experience
- **Modern CLI** - Rich terminal interface with interactive selection
- **Flexible Configuration** - Customize models, phases, and outputs
- **Smart Exclusions** - Focus analysis on relevant files
- **Comprehensive Reports** - Detailed documentation for each phase
- **Metrics Tracking** - Analysis time and token usage

## 🚀 Quick Start

### Requirements
- **Python 3.8+**
- **API Key** for at least one provider:
  - Anthropic (Claude), OpenAI (o1/o3-mini/GPT-4o), DeepSeek, or Google Gemini

### Installation

1. **Clone and Install**
   ```bash
   git clone https://github.com/sosacrazy126/cursorrules-architect.git
   cd cursorrules-architect
   pip install -e .
   ```

2. **Set API Keys**
   ```bash
   # Choose one or more providers
   export ANTHROPIC_API_KEY='your-key'
   export OPENAI_API_KEY='your-key'
   export DEEPSEEK_API_KEY='your-key'
   export GEMINI_API_KEY='your-key'
   ```

   Or create a `.env` file:
   ```env
   ANTHROPIC_API_KEY=your-anthropic-key
   OPENAI_API_KEY=your-openai-key
   DEEPSEEK_API_KEY=your-deepseek-key
   GEMINI_API_KEY=your-gemini-key
   ```

### Usage

```bash
# Generate configuration for specific AI tool
python -m cursorrules_architect generate /path/to/project --tool cursor

# Interactive tool selection
python -m cursorrules_architect generate /path/to/project

# Preview before saving
python -m cursorrules_architect generate /path/to/project --tool cursor --preview

# Generate for all supported tools
python -m cursorrules_architect generate /path/to/project --tool all

# List supported tools
python -m cursorrules_architect list

# Get help
python -m cursorrules_architect --help
```

## 📋 Supported AI Tools

| Tool | Configuration File | Description |
|------|------------------|-------------|
| **Cursor** | `.cursorrules` | Cursor IDE with AI assistant |
| **Windsurf** | `.windsurfrules` | Windsurf agentic IDE |
| **Cline** | `.clinerules` | Cline VS Code extension |
| **Roo Code** | `.roorules` | Roo Code AI development team |
| **Claude Code** | `CLAUDE.md` | Claude Code CLI tool |

## 📖 Documentation

- **[Complete Documentation](docs/)** - Comprehensive guides and references
- **[CLI Reference](docs/CLI_README.md)** - Detailed command-line usage
- **[Configuration Guide](docs/PROJECT_SCOPE.md)** - Customization options
- **[Contributing](docs/CONTRIBUTING.md)** - How to contribute
- **[Architecture](docs/indydevdan-architect-alignment-matrix.md)** - System design

## 🔧 Configuration

Customize AI models for each analysis phase in `src/cursorrules_architect/config/agents.py`:

```python
MODEL_CONFIG = {
    "phase1": GEMINI_BASIC,           # Initial discovery
    "phase2": CLAUDE_WITH_REASONING,  # Planning
    "phase3": O1_HIGH,                # Deep analysis
    "phase4": DEEPSEEK_REASONER,      # Synthesis
    "phase5": GEMINI_BASIC,           # Consolidation
    "final": CLAUDE_WITH_REASONING,   # Final analysis
}
```

## 📊 Output

The tool generates comprehensive analysis outputs:

```
your-project/
├── .cursorrules              # Cursor IDE configuration
├── .windsurfrules           # Windsurf configuration
├── .clinerules              # Cline VS Code extension
├── .roorules                # Roo Code AI team
├── CLAUDE.md                # Claude Code CLI context
└── phases_output/           # Detailed analysis reports
    ├── phase1_discovery.md
    ├── phase2_planning.md
    ├── phase3_analysis.md
    ├── phase4_synthesis.md
    ├── phase5_consolidation.md
    └── final_analysis.md
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and standards
- Testing requirements
- Pull request process

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Original Project**: [SlyyCooper's CursorRules Architect](https://github.com/SlyyCooper/cursorrules-architect)
- **Enhanced Fork**: Advanced analysis pipeline and universal tool support

Built with ❤️ using Claude, GPT-4o, DeepSeek, and Gemini

