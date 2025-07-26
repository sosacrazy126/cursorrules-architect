# CursorRules Architect - Detailed Guide

## 🌟 Advanced Fork Development

This is an enhanced fork of [SlyyCooper's CursorRules Architect](https://github.com/SlyyCooper/cursorrules-architect) that has evolved into a comprehensive AI-assisted development platform. While preserving the original's multi-provider analysis capabilities, we've added groundbreaking **Context Engineering** paradigms and **Universal Tool Support**.

### What We've Built On Top

**🔬 Context Engineering Paradigm** - Revolutionary AI context management using neural field dynamics, protocol shell execution, and semantic field resonance for enhanced analysis coherence.

**🛠️ Universal AI Tool Support** - Beyond `.cursorrules`, now generates optimized configurations for Cursor, Windsurf, Cline, Roo Code, Claude Code CLI, and more.

**⚡ Enhanced CLI Generator** - Modern command-line interface with preview modes, tool-specific adaptations, and rich terminal UX.

**🧠 Neural Field Processing** - Continuous semantic understanding through field dynamics, attractor patterns, and resonance scaffolding.

## 🧠 Context Engineering Paradigm

Our revolutionary Context Engineering system enhances analysis quality through persistent semantic understanding and collaborative processing.

### Neural Field Dynamics

The system maintains **neural semantic fields** that continuously process and understand project context:

```python
# Neural fields track semantic resonance patterns
primary_field = NeuralField(
    attractors=["architecture", "performance", "security", "usability"],
    resonance_threshold=0.7,
    field_decay=0.1
)

# Process context through field dynamics  
field_result = neural_field_manager.process_context(
    project_context, 
    query="software architecture patterns"
)
```

### Protocol Shell Engine

Execute collaborative protocols using **Pareto-lang** format for enhanced coordination:

```yaml
# Example protocol execution
protocol: neural.field.process
input:
  field_state: current_semantic_field
  target_patterns: [analysis_focus_areas]
  coherence_targets: {phase_analysis: 0.8}
output:
  enhanced_context: processed_understanding
  resonance_metrics: field_coherence_scores
```

### Memory Integration

Cross-session learning and pattern recognition:

- **Analysis Memory**: Persistent project knowledge across sessions
- **Similar Project Insights**: Learn from previous analysis patterns  
- **Phase Pattern Recognition**: Optimize planning based on historical data
- **Symbolic Residue Tracking**: Maintain context through field dynamics

## 🎯 Universal CLI Generator

Generate optimized configurations for any AI coding tool through our unified interface.

### Supported AI Tools

| Tool | Configuration File | Status | Description |
|------|------------------|--------|-------------|
| **Cursor** | `.cursorrules` | ✅ Ready | Cursor IDE with AI assistant |
| **Windsurf** | `.windsurfrules` | ✅ Ready | Windsurf agentic IDE |
| **Cline** | `.clinerules` | ✅ Ready | Cline VS Code extension with MCP |
| **Roo Code** | `.roorules` | ✅ Ready | Roo Code AI development team |
| **Claude Code** | `CLAUDE.md` | ✅ Ready | Claude Code CLI tool |
| **PearAI** | Custom format | 🚧 Soon | PearAI coding assistant |
| **GitHub Copilot** | Settings integration | 🚧 Soon | GitHub Copilot Workspace |
| **Bolt.new** | Export format | 🚧 Soon | Bolt.new rapid prototyping |

### CRS-1 Specification Compliance

All generated configurations follow the **Cursor Rules Specification v1 (CRS-1)** for optimal AI assistance:

1. **Identity Establishment** - Clear AI role and expertise definition
2. **Temporal Framework** - Current context and technology versions  
3. **Technical Constraints** - Environment, dependencies, configuration
4. **Imperative Directives** - Explicit numbered requirements
5. **Knowledge Framework** - Comprehensive domain-specific knowledge
6. **Implementation Examples** - Concrete code patterns
7. **Negative Patterns** - Anti-patterns to avoid
8. **Knowledge Evolution** - Learning and adaptation mechanisms

### Tool-Specific Adaptations

Each AI tool receives optimized content:

- **Cursor**: Focus on IDE integration and real-time assistance
- **Windsurf**: Emphasis on autonomous development capabilities  
- **Cline**: MCP support and VS Code extension patterns
- **Roo Code**: Team-based AI development workflows
- **Claude Code**: CLI context and command-line interaction patterns

## ⚙️ Advanced Configuration

### Model Configuration

CursorRules Architect allows you to customize which AI models are used for each analysis phase through the `src/cursorrules_architect/config/agents.py` file.

### Model Configurations

The system defines several predefined model configurations you can use:

```python
# Anthropic Configurations
CLAUDE_BASIC = ModelConfig(
    provider=ModelProvider.ANTHROPIC,
    model_name="claude-3-7-sonnet-20250219",
    reasoning=ReasoningMode.DISABLED
)

CLAUDE_WITH_REASONING = ModelConfig(
    provider=ModelProvider.ANTHROPIC,
    model_name="claude-3-7-sonnet-20250219",
    reasoning=ReasoningMode.ENABLED
)

# OpenAI Configurations
O1_HIGH = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o1",
    reasoning=ReasoningMode.HIGH
)

O3_MINI_MEDIUM = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="o3-mini",
    reasoning=ReasoningMode.MEDIUM
)

GPT4O_CREATIVE = ModelConfig(
    provider=ModelProvider.OPENAI,
    model_name="gpt-4o",
    reasoning=ReasoningMode.TEMPERATURE,
    temperature=0.9
)

# DeepSeek Configurations
DEEPSEEK_REASONER = ModelConfig(
    provider=ModelProvider.DEEPSEEK,
    model_name="deepseek-reasoner",
    reasoning=ReasoningMode.ENABLED
)

# Gemini Configurations
GEMINI_BASIC = ModelConfig(
    provider=ModelProvider.GEMINI,
    model_name="gemini-2.0-flash",
    reasoning=ReasoningMode.DISABLED
)

GEMINI_WITH_REASONING = ModelConfig(
    provider=ModelProvider.GEMINI,
    model_name="gemini-2.5-pro-exp-03-25",
    reasoning=ReasoningMode.ENABLED
)
```

### Customizing Phase Models

To change which model is used for each phase, simply update the `MODEL_CONFIG` dictionary:

```python
MODEL_CONFIG = {
    "phase1": GEMINI_BASIC,                # Use Gemini-2.0-flash for Phase 1
    "phase2": GEMINI_WITH_REASONING,       # Use Gemini-2.5-pro with reasoning for Phase 2
    "phase3": CLAUDE_WITH_REASONING,       # Use Claude with reasoning for Phase 3
    "phase4": O1_HIGH,                     # Use OpenAI's o1 with high reasoning for Phase 4
    "phase5": DEEPSEEK_REASONER,           # Use DeepSeek Reasoner for Phase 5
    "final": CLAUDE_WITH_REASONING,        # Use Claude with reasoning for final analysis
}
```

### Exclusion Settings

You can customize which files and directories are excluded from analysis by modifying `src/cursorrules_architect/config/exclusions.py`:

```python
EXCLUDED_DIRS = {
    'node_modules', '.next', '.git', 'venv', '__pycache__', 
    'dist', 'build', '.vscode', '.idea', 'coverage',
    # Add your custom directories here
}

EXCLUDED_FILES = {
    'package-lock.json', 'yarn.lock', '.DS_Store', '.env',
    # Add your custom files here
}

EXCLUDED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.ico', '.svg', 
    '.pyc', '.pyo', '.pyd', '.so', '.db', '.sqlite',
    # Add your custom extensions here
}
```

## 🛠️ Requirements

- Python 3.8+
- API keys for at least one of the supported providers:
  - Anthropic API key with access to `claude-3-7-sonnet-20250219`
  - OpenAI API key with access to `o1`, `o3-mini`, or `gpt-4o`
  - DeepSeek API key with access to DeepSeek Reasoner
  - Google API key with access to `gemini-2.0-flash` or `gemini-2.5-pro-exp-03-25`
- Dependencies:
  - `anthropic` for Anthropic API access
  - `openai` for OpenAI API access
  - `google-generativeai` for Google Gemini API access
  - `rich` for beautiful terminal output
  - `typer` for CLI interface
  - `pathlib` for path manipulation
  - `asyncio` for async operations

## 📊 Enhanced Output Examples

### Universal Tool Generation Output

AI tool-specific configurations with CRS-1 compliance:

```
your-project/
├── .cursorrules                 # Cursor IDE configuration (CRS-1 compliant)
├── .windsurfrules              # Windsurf agentic IDE configuration  
├── .clinerules                 # Cline VS Code extension configuration
├── .roorules                   # Roo Code AI team configuration
├── CLAUDE.md                   # Claude Code CLI context file
└── config_generation_log.md    # Generation details and tool-specific tips
```

### Context Engineering Artifacts

Enhanced analysis with persistent knowledge:

```
your-project/
├── analysis_context_field.json # Context field state
├── phase2_protocols.json       # Collaborative protocol definitions
└── context_engineering/        # Context Engineering outputs
    ├── neural_field_state.json     # Neural field dynamics
    ├── resonance_patterns.json     # Field resonance patterns
    ├── attractor_emergence.json    # Pattern co-emergence data
    └── symbolic_residue.json       # Persistent knowledge residue
```

### Analysis Metrics

The system tracks performance metrics for the analysis:
- Total analysis time
- Token usage for phases using reasoning models
- Per-agent execution times

## 🛠️ Related Tools

Check out [cursorrules-tools](https://github.com/SlyyCooper/cursorrules-tools) for additional utilities that can help with Cursor IDE development. This collection includes tools for managing `.cursorrules` and `.cursorignore` files, generating codebase snapshots, analyzing dependencies, and more.
