# 🧠 CursorRules Architect - Advanced Edition

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-o1%20%7C%20o3--mini%20%7C%20gpt--4o-blue.svg)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-claude--3.7--sonnet-purple.svg)](https://www.anthropic.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-deepseek--reasoner-red.svg)](https://deepseek.com/)
[![Google](https://img.shields.io/badge/Google-gemini--2.0--flash%20%7C%20gemini--2.5--pro-green.svg)](https://ai.google.dev/)
[![Context Engineering](https://img.shields.io/badge/Context%20Engineering-Neural%20Fields-cyan.svg)](#-context-engineering-paradigm)
[![Forked From](https://img.shields.io/badge/Forked%20From-SlyyCooper-orange.svg)](https://github.com/SlyyCooper/cursorrules-architect)

**Multi-AI Analysis System with Context Engineering & Universal Tool Support 🚀**

[Features](#-features) • [Context Engineering](#-context-engineering-paradigm) • [Universal CLI](#-universal-cli-generator) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture)

</div>

## 🌟 Advanced Fork Development

This is an enhanced fork of [SlyyCooper's CursorRules Architect](https://github.com/SlyyCooper/cursorrules-architect) that has evolved into a comprehensive AI-assisted development platform. While preserving the original's multi-provider analysis capabilities, we've added groundbreaking **Context Engineering** paradigms and **Universal Tool Support**.

### What We've Built On Top

**🔬 Context Engineering Paradigm** - Revolutionary AI context management using neural field dynamics, protocol shell execution, and semantic field resonance for enhanced analysis coherence.

**🛠️ Universal AI Tool Support** - Beyond `.cursorrules`, now generates optimized configurations for Cursor, Windsurf, Cline, Roo Code, Claude Code CLI, and more.

**⚡ Enhanced CLI Generator** - Modern command-line interface with preview modes, tool-specific adaptations, and rich terminal UX.

**🧠 Neural Field Processing** - Continuous semantic understanding through field dynamics, attractor patterns, and resonance scaffolding.

## ✨ Enhanced Features

### 🚀 Core Capabilities (Original + Enhanced)
- 🌐 **Multi-Provider Support** - Leverage AI models from Anthropic, OpenAI, DeepSeek, and Google Gemini
- 🧠 **Enhanced Reasoning** - Different reasoning modes (enabled/disabled, low/medium/high, temperature)
- 🤖 **Dynamic Agents** - Creates specialized analysis agents based on your specific codebase
- 🔍 **Six-Phase Analysis** - Structured pipeline that builds comprehensive understanding
- 🔄 **Async Processing** - Parallel agent execution for faster analysis
- 📊 **Detailed Metrics** - Track analysis time and token usage

### 🎯 Universal AI Tool Generation
- 🎨 **Multi-Tool Support** - Generate configurations for Cursor, Windsurf, Cline, Roo Code, Claude Code CLI
- 📋 **CRS-1 Specification** - Follows Cursor Rules Specification v1 for optimal AI assistance
- 🔄 **Tool-Specific Adaptations** - Content automatically adapted for each AI tool's requirements
- 👀 **Preview Mode** - See configuration content before saving files
- 📁 **Flexible Output** - Choose output directory and force overwrite options

### 🧠 Context Engineering Paradigm
- 🌊 **Neural Field Dynamics** - Continuous semantic field processing for enhanced context understanding
- 🤝 **Protocol Shell Engine** - Execute collaborative protocols using Pareto-lang format
- 📈 **Field Resonance Scaffolding** - Maintain analysis coherence through resonance patterns
- 🎯 **Attractor Co-Emergence** - Self-organizing pattern recognition and synthesis
- 💾 **Symbolic Residue Tracking** - Persistent project knowledge across analysis sessions
- 🔗 **Memory Integration** - Cross-session learning and pattern recognition

### 🛠️ Enhanced Development Experience
- 📝 **Comprehensive Documentation** - Generated reports for each phase and component
- 📑 **Multi-Format Output** - Separate markdown files for each analysis phase
- 🚫 **Smart Exclusions** - Customizable patterns to focus analysis on relevant files
- 🔧 **Fully Configurable** - Easy to customize which models are used for each phase
- 🎭 **Rich Terminal UI** - Beautiful progress indicators and formatted output

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
  - `click` for CLI interface
  - `pathlib` for path manipulation
  - `asyncio` for async operations

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/slyycooper/cursorrules-architect.git
   cd cursorrules-architect
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**
   ```bash
   # Linux/macOS
   export ANTHROPIC_API_KEY='your-anthropic-api-key'
   export OPENAI_API_KEY='your-openai-api-key'
   export DEEPSEEK_API_KEY='your-deepseek-api-key'
   export GEMINI_API_KEY='your-gemini-api-key'

   # Windows
   set ANTHROPIC_API_KEY=your-anthropic-api-key
   set OPENAI_API_KEY=your-openai-api-key
   set DEEPSEEK_API_KEY=your-deepseek-api-key
   set GEMINI_API_KEY=your-gemini-api-key
   ```

   Alternatively, create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your-anthropic-api-key
   OPENAI_API_KEY=your-openai-api-key
   DEEPSEEK_API_KEY=your-deepseek-api-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

## 🚀 Usage

### Basic Project Analysis

```bash
# Run complete 6-phase analysis (original functionality)
python main.py -p /path/to/your/project
```

### Universal AI Tool Generation

```bash
# Generate configuration for specific AI tool
python -m cli.commands.generate /path/to/project --tool cursor
python -m cli.commands.generate /path/to/project --tool windsurf  
python -m cli.commands.generate /path/to/project --tool claude

# Generate for all supported tools
python -m cli.commands.generate /path/to/project --tool all

# Preview before saving
python -m cli.commands.generate /path/to/project --tool cursor --preview

# Advanced options
python -m cli.commands.generate /path/to/project \
    --tool cursor \
    --complexity advanced \
    --output /custom/output/dir \
    --force \
    --verbose
```

### Interactive Tool Selection

```bash
# Run without --tool flag for interactive selection
python -m cli.commands.generate /path/to/project
```

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

## ⚙️ Configuration

### Model Configuration

CursorRules Architect allows you to customize which AI models are used for each analysis phase through the `config/agents.py` file.

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

You can customize which files and directories are excluded from analysis by modifying `config/exclusions.py`:

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

## 🏗️ Architecture

CursorRules Architect V2 follows a sophisticated multi-phase analysis approach:

### 1. Base Architecture

The system is built on a `BaseArchitect` abstract class that standardizes how different AI model providers are integrated:

- `AnthropicArchitect` - Interface to Anthropic's Claude models
- `OpenAIArchitect` - Interface to OpenAI's models (o1, o3-mini, gpt-4o)
- `DeepSeekArchitect` - Interface to DeepSeek's reasoning models
- `GeminiArchitect` - Interface to Google's Gemini models

Each architect implements standardized methods:
- `analyze()` - Runs general analysis
- `create_analysis_plan()` - Creates a detailed analysis plan (Phase 2)
- `synthesize_findings()` - Synthesizes findings from deep analysis (Phase 4)
- `consolidate_results()` - Consolidates all analysis results (Phase 5)
- `final_analysis()` - Provides final architectural insights

### 2. Analysis Pipeline

#### Phase 1: Initial Discovery
Performs initial exploration of the project structure, dependencies, and technology stack using specialized agents:
- Structure Agent: Analyzes directory and file organization
- Dependency Agent: Investigates package dependencies
- Tech Stack Agent: Identifies frameworks and technologies

#### Phase 2: Methodical Planning
Creates a detailed analysis plan using findings from Phase 1:
- Defines specialized agents with specific responsibilities
- Assigns files to relevant agents based on expertise
- Provides detailed instructions for deeper analysis
- Outputs an XML-structured plan that guides Phase 3

#### Phase 3: Deep Analysis
The heart of the system - dynamically creates specialized agents based on Phase 2's output:
- Each agent focuses on its assigned files and responsibilities
- Agents run in parallel for efficiency
- Performs in-depth analysis of code patterns, architecture, and dependencies
- Falls back to predefined agents if Phase 2 doesn't provide valid definitions

#### Phase 4: Synthesis
Synthesizes findings from Phase 3 into cohesive insights:
- Integrates agent findings into a holistic view
- Identifies relationships between components
- Highlights key architectural patterns
- Updates analysis directions

#### Phase 5: Consolidation
Consolidates results from all previous phases into a comprehensive report:
- Organizes findings by component/module
- Creates comprehensive documentation
- Prepares data for final analysis

#### Final Analysis
Provides high-level insights and recommendations:
- System structure mapping
- Architecture pattern identification
- Relationship documentation
- Improvement recommendations

### 3. Reasoning Modes

The system supports different reasoning modes depending on the model:

- For Anthropic models:
  - `ENABLED` - Use extended thinking capability
  - `DISABLED` - Standard inference

- For OpenAI models:
  - For O1 and O3-mini:
    - `LOW`/`MEDIUM`/`HIGH` - Different reasoning effort levels
  - For GPT-4o:
    - `TEMPERATURE` - Use temperature-based sampling

- For DeepSeek models:
  - Always uses `ENABLED` reasoning mode
  
- For Gemini models:
  - `ENABLED` - Uses the thinking-enabled experimental model variant
  - `DISABLED` - Standard inference

## 📂 Enhanced Project Structure

```
cursorrules-architect/
├── cli/                         # 🆕 Universal CLI Generator
│   ├── commands/                # CLI command implementations
│   │   ├── generate.py          # Multi-tool configuration generator
│   │   ├── list_tools.py        # List supported AI tools
│   │   └── validate.py          # Validate generated configurations
│   ├── formatters/              # Tool-specific formatters
│   │   ├── base.py              # Base formatter interface
│   │   ├── cursor.py            # Cursor IDE formatter
│   │   ├── windsurf.py          # Windsurf agentic IDE formatter
│   │   ├── cline.py             # Cline VS Code extension formatter
│   │   ├── roo.py               # Roo Code AI team formatter
│   │   └── claude.py            # Claude Code CLI formatter
│   └── ui/                      # CLI user interface components
│       ├── configuration.py     # Configuration management UI
│       ├── generation.py        # Generation workflow UI
│       ├── tool_selection.py    # Interactive tool selection
│       └── welcome.py           # Welcome screen and help
├── config/                      # Configuration settings
│   ├── agents.py                # Model and agent configuration
│   ├── exclusions.py            # Exclusion patterns for analysis
│   └── prompts/                 # Centralized prompt templates
│       ├── final_analysis_prompt.py # CRS-1 compliant final analysis
│       ├── phase_1_prompts.py   # Phase 1 agent prompts
│       ├── phase_2_prompts.py   # Phase 2 planning prompts
│       ├── phase_4_prompts.py   # Phase 4 synthesis prompts
│       └── phase_5_prompts.py   # Phase 5 consolidation prompts
├── core/                        # Core functionality
│   ├── agents/                  # Agent implementations
│   │   ├── anthropic.py         # Anthropic agent implementation
│   │   ├── base.py              # Base architect abstract class
│   │   ├── deepseek.py          # DeepSeek agent implementation
│   │   ├── gemini.py            # Google Gemini agent implementation
│   │   └── openai.py            # OpenAI agent implementation
│   ├── analysis/                # Analysis phase implementations
│   │   ├── final_analysis.py    # Final Analysis phase
│   │   ├── phase_1.py           # Initial Discovery phase
│   │   ├── phase_2.py           # Methodical Planning phase
│   │   ├── phase_3.py           # Deep Analysis phase
│   │   ├── phase_4.py           # Synthesis phase
│   │   └── phase_5.py           # Consolidation phase
│   ├── context_engineering/     # 🆕 Context Engineering System
│   │   ├── neural_field_manager.py     # Neural field dynamics
│   │   ├── protocol_shell_engine.py    # Pareto-lang protocol execution
│   │   ├── field_resonance.py          # Resonance scaffolding
│   │   ├── attractor_emergence.py      # Pattern co-emergence
│   │   └── neural_field_config.yaml    # Field configuration
│   ├── memory/                  # 🆕 Cross-Session Memory
│   │   ├── analysis_memory_integration.py  # Memory management
│   │   ├── project_pattern_db.py          # Pattern database
│   │   └── symbolic_residue.py            # Residue tracking
│   ├── context/                 # 🆕 Context Field Integration
│   │   ├── analysis_context_integration.py # Context field dynamics
│   │   ├── field_enhancement.py           # Field-enhanced analysis
│   │   └── resonance_patterns.py          # Pattern recognition
│   ├── protocol/                # 🆕 Protocol Integration
│   │   ├── phase2_protocol_integration.py # Collaborative protocols
│   │   ├── protocol_execution.py          # Protocol execution engine
│   │   └── pareto_lang_parser.py          # Pareto-lang parser
│   ├── types/                   # Type definitions
│   │   └── agent_config.py      # Agent configuration types
│   └── utils/                   # Utility functions and tools
│       ├── file_creation/           # File creation utilities
│       │   ├── cursorignore.py      # .cursorignore management
│       │   ├── cursorrules.py       # .cursorrules management
│       │   └── phases_output.py     # Phase output saving
│       └── tools/                   # Tool utilities
│           ├── agent_parser.py      # Parser for Phase 2 output
│           ├── file_retriever.py    # File content retrieval
│           └── tree_generator.py    # Directory tree generation
├── main.py                      # Main entry point (original analysis)
├── app.py                       # 🆕 Streamlit web interface
└── requirements.txt             # Project dependencies
```

## 📊 Enhanced Output

### Original Analysis Output

Complete 6-phase analysis with comprehensive documentation:

```
your-project/
├── .cursorrules                 # Generated rules file for Cursor IDE  
├── .cursorignore                # Generated ignore patterns for Cursor IDE
└── phases_output/               # Detailed phase outputs
    ├── phase1_discovery.md      # Initial agent findings
    ├── phase2_planning.md       # Planning document with agent assignments
    ├── phase3_analysis.md       # Deep analysis results from dynamic agents
    ├── phase4_synthesis.md      # Synthesized findings
    ├── phase5_consolidation.md  # Consolidated report
    ├── final_analysis.md        # Final recommendations
    ├── complete_report.md       # Overview of all phases
    └── metrics.md               # Analysis metrics
```

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
├── analysis_memory.db          # Cross-session memory database
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

## 💡 Advanced Features

### Dynamic Agent Creation

The system's key innovation is the dynamic agent creation process:

1. **Phase 2 (Planning)**: 
   - Creates an XML-structured output defining specialized agents
   - Each agent is assigned responsibilities and specific files

2. **Agent Parser**:
   - Parses the XML output from Phase 2
   - Creates a structured representation of agent definitions
   - Includes fallback mechanisms for handling parsing issues

3. **Phase 3 (Dynamic Analysis)**:
   - Creates AI agents based on the extracted definitions
   - Each agent only analyzes its assigned files
   - Uses custom-formatted prompts for each agent's role

### Multi-Provider Flexibility

You can run the system with one or more AI providers:

- **Anthropic-only**: Set all phases to use Claude models
- **OpenAI-only**: Set all phases to use o1, o3-mini, or gpt-4o
- **DeepSeek-only**: Set all phases to use DeepSeek Reasoner
- **Gemini-only**: Set all phases to use Google Gemini models
- **Mix and match**: Use different providers for different phases

### Customizing Prompts

For advanced users, you can modify the prompt templates in the `config/prompts/` directory to customize how agents analyze your code.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**: Create your own fork to work on
2. **Make Your Changes**: Implement your feature or bug fix
3. **Run Tests**: Ensure your changes don't break existing functionality
4. **Submit a Pull Request**: Send us your contributions for review

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

### 🙏 Acknowledgments

**Original Project**: [SlyyCooper's CursorRules Architect](https://github.com/SlyyCooper/cursorrules-architect)  
**Enhanced Fork**: Advanced Context Engineering & Universal Tool Support

Built with 💙 using [Claude-3.7-Sonnet](https://www.anthropic.com/claude), [o1](https://openai.com/), [DeepSeek Reasoner](https://deepseek.com/), and [Google Gemini](https://ai.google.dev/)

**🧠 Context Engineering** • **🎯 Universal AI Tools** • **⚡ Enhanced Analysis**

</div>