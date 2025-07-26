# CursorRules Architect - Architecture Guide

## 🏗️ System Architecture

CursorRules Architect follows a sophisticated multi-phase analysis approach with a modular, extensible design.

## 📂 Project Structure

```
cursorrules-architect/
├── src/cursorrules_architect/       # Main package
│   ├── __init__.py                  # Package initialization
│   ├── __main__.py                  # Module execution entry point
│   ├── main.py                      # Main analysis engine
│   ├── modern_cli.py                # Alternative CLI
│   ├── demo_blueprint.py            # Demo script
│   ├── cli/                         # CLI components
│   │   ├── app.py                   # Main CLI application
│   │   ├── main.py                  # CLI entry point
│   │   ├── commands/                # CLI command implementations
│   │   │   ├── generate.py          # Multi-tool configuration generator
│   │   │   ├── list_tools.py        # List supported AI tools
│   │   │   └── validate.py          # Validate generated configurations
│   │   ├── formatters/              # Tool-specific formatters
│   │   │   ├── base.py              # Base formatter interface
│   │   │   ├── cursor.py            # Cursor IDE formatter
│   │   │   ├── windsurf.py          # Windsurf agentic IDE formatter
│   │   │   ├── cline.py             # Cline VS Code extension formatter
│   │   │   ├── roo.py               # Roo Code AI team formatter
│   │   │   └── claude.py            # Claude Code CLI formatter
│   │   └── interactive/             # Interactive CLI components
│   │       ├── main_app.py          # Main interactive application
│   │       └── screens/             # TUI screens
│   ├── config/                      # Configuration settings
│   │   ├── __init__.py              # Config package exports
│   │   ├── agents.py                # Model and agent configuration
│   │   ├── analysis_config.py       # Analysis configuration classes
│   │   ├── exclusions.py            # Exclusion patterns for analysis
│   │   └── prompts/                 # Centralized prompt templates
│   │       ├── final_analysis_prompt.py # CRS-1 compliant final analysis
│   │       ├── phase_1_prompts.py   # Phase 1 agent prompts
│   │       ├── phase_2_prompts.py   # Phase 2 planning prompts
│   │       ├── phase_3_prompts.py   # Phase 3 deep analysis prompts
│   │       ├── phase_4_prompts.py   # Phase 4 synthesis prompts
│   │       └── phase_5_prompts.py   # Phase 5 consolidation prompts
│   ├── core/                        # Core functionality
│   │   ├── agents/                  # Agent implementations
│   │   │   ├── __init__.py          # Agent package exports
│   │   │   ├── anthropic.py         # Anthropic agent implementation
│   │   │   ├── base.py              # Base architect abstract class
│   │   │   ├── deepseek.py          # DeepSeek agent implementation
│   │   │   ├── gemini.py            # Google Gemini agent implementation
│   │   │   └── openai.py            # OpenAI agent implementation
│   │   ├── analysis/                # Analysis phase implementations
│   │   │   ├── __init__.py          # Analysis package exports
│   │   │   ├── final_analysis.py    # Final Analysis phase
│   │   │   ├── phase_1.py           # Initial Discovery phase
│   │   │   ├── phase_2.py           # Methodical Planning phase
│   │   │   ├── phase_3.py           # Deep Analysis phase
│   │   │   ├── phase_4.py           # Synthesis phase
│   │   │   ├── phase_5.py           # Consolidation phase
│   │   │   └── result.py            # Analysis result classes
│   │   ├── context_engineering/     # Context Engineering System
│   │   │   ├── neural_field_manager.py     # Neural field dynamics
│   │   │   ├── protocol_shell_engine.py    # Pareto-lang protocol execution
│   │   │   └── neural_field_config.yaml    # Field configuration
│   │   ├── context/                 # Context Field Integration
│   │   │   ├── analysis_context_integration.py # Context field dynamics
│   │   │   └── context_field_engine.py         # Field processing engine
│   │   ├── protocol/                # Protocol Integration
│   │   │   ├── phase2_protocol_integration.py # Collaborative protocols
│   │   │   └── protocol_engine.py             # Protocol execution engine
│   │   ├── blueprint/               # Blueprint generation
│   │   │   ├── generator.py         # Blueprint generator
│   │   │   └── integration.py       # Blueprint integration
│   │   ├── types/                   # Type definitions
│   │   │   └── agent_config.py      # Agent configuration types
│   │   └── utils/                   # Utility functions and tools
│   │       ├── file_creation/       # File creation utilities
│   │       │   ├── cursorignore.py  # .cursorignore management
│   │       │   ├── cursorrules.py   # .cursorrules management
│   │       │   └── phases_output.py # Phase output saving
│   │       └── tools/               # Tool utilities
│   │           ├── agent_parser.py  # Parser for Phase 2 output
│   │           ├── file_retriever.py # File content retrieval
│   │           ├── tree_generator.py # Directory tree generation
│   │           ├── clean_cursorrules.py # Rules cleaning utility
│   │           └── model_config_helper.py # Model config utilities
├── tests/                           # Test suite
│   ├── conftest.py                  # Test configuration
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   └── fixtures/                    # Test fixtures
├── docs/                            # Documentation
│   ├── README.md                    # Documentation index
│   ├── DETAILED_GUIDE.md            # Comprehensive guide
│   ├── ARCHITECTURE.md              # This file
│   ├── CLI_README.md                # CLI documentation
│   └── [other documentation files]
├── scripts/                         # Build and utility scripts
│   ├── Makefile                     # Build commands
│   └── fix_imports.py               # Import fixing utility
├── PROMPTS/                         # Application data
├── phases_output/                   # Output directory
├── README.md                        # Root documentation
├── LICENSE                          # License file
├── pyproject.toml                   # Python project configuration
├── Makefile                         # Convenience wrapper
├── .cursorrules                     # Tool configuration
└── .cursorignore                    # Tool configuration
```

## 🔧 Base Architecture

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

## 📊 Analysis Pipeline

### Phase 1: Initial Discovery
Performs initial exploration of the project structure, dependencies, and technology stack using specialized agents:
- **Structure Agent**: Analyzes directory and file organization
- **Dependency Agent**: Investigates package dependencies
- **Tech Stack Agent**: Identifies frameworks and technologies

### Phase 2: Methodical Planning
Creates a detailed analysis plan using findings from Phase 1:
- Defines specialized agents with specific responsibilities
- Assigns files to relevant agents based on expertise
- Provides detailed instructions for deeper analysis
- Outputs an XML-structured plan that guides Phase 3

### Phase 3: Deep Analysis
The heart of the system - dynamically creates specialized agents based on Phase 2's output:
- Each agent focuses on its assigned files and responsibilities
- Agents run in parallel for efficiency
- Performs in-depth analysis of code patterns, architecture, and dependencies
- Falls back to predefined agents if Phase 2 doesn't provide valid definitions

### Phase 4: Synthesis
Synthesizes findings from Phase 3 into cohesive insights:
- Integrates agent findings into a holistic view
- Identifies relationships between components
- Highlights key architectural patterns
- Updates analysis directions

### Phase 5: Consolidation
Consolidates results from all previous phases into a comprehensive report:
- Organizes findings by component/module
- Creates comprehensive documentation
- Prepares data for final analysis

### Final Analysis
Provides high-level insights and recommendations:
- System structure mapping
- Architecture pattern identification
- Relationship documentation
- Improvement recommendations

## 🧠 Reasoning Modes

The system supports different reasoning modes depending on the model:

### Anthropic Models
- `ENABLED` - Use extended thinking capability
- `DISABLED` - Standard inference

### OpenAI Models
- **For O1 and O3-mini**:
  - `LOW`/`MEDIUM`/`HIGH` - Different reasoning effort levels
- **For GPT-4o**:
  - `TEMPERATURE` - Use temperature-based sampling

### DeepSeek Models
- Always uses `ENABLED` reasoning mode
  
### Gemini Models
- `ENABLED` - Uses the thinking-enabled experimental model variant
- `DISABLED` - Standard inference

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

For advanced users, you can modify the prompt templates in the `src/cursorrules_architect/config/prompts/` directory to customize how agents analyze your code.

## 🔌 Extension Points

The architecture is designed for extensibility:

### Adding New AI Providers
1. Create a new agent class inheriting from `BaseArchitect`
2. Implement required abstract methods
3. Add provider configuration to `ModelProvider` enum
4. Update `get_architect_for_phase()` function

### Adding New Output Formats
1. Create a new formatter class inheriting from `BaseFormatter`
2. Implement format-specific generation logic
3. Register formatter in CLI commands

### Adding New Analysis Phases
1. Create new phase class following existing patterns
2. Add phase configuration to `MODEL_CONFIG`
3. Update main analysis pipeline

## 🧪 Testing Architecture

The test suite is organized to mirror the source structure:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Fixtures**: Reusable test data and configurations
- **Configuration**: Shared test setup and utilities

## 📦 Package Structure

The project follows Python packaging best practices:

- **src/ layout**: Proper package isolation
- **Entry points**: CLI accessible via `python -m cursorrules_architect`
- **Relative imports**: Clean internal import structure
- **Configuration**: Centralized in `pyproject.toml`
