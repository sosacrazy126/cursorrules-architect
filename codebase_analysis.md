# CursorRules Architect V2 - Codebase Analysis

## Project Overview

**CursorRules Architect V2** is a sophisticated multi-agent AI code analysis tool that leverages multiple AI providers (OpenAI, Anthropic, DeepSeek, Google Gemini) to perform comprehensive codebase analysis. The tool generates customized `.cursorrules` and `.cursorignore` files for the Cursor IDE, along with detailed analysis reports.

## Core Architecture

### Multi-Provider AI Integration

The system supports four AI providers through a unified architecture:

- **OpenAI**: o1, o3-mini, gpt-4o models with different reasoning levels
- **Anthropic**: Claude-3.7-Sonnet with optional reasoning capabilities  
- **DeepSeek**: DeepSeek Reasoner with built-in reasoning
- **Google Gemini**: 2.0-flash and 2.5-pro models with thinking capabilities

### Base Architecture Pattern

**Abstract Base Class (`core/agents/base.py`)**
```
BaseArchitect (ABC)
├── AnthropicArchitect
├── OpenAIArchitect  
├── DeepSeekArchitect
└── GeminiArchitect
```

Each architect implements standardized methods:
- `analyze()` - General analysis
- `create_analysis_plan()` - Phase 2 planning
- `synthesize_findings()` - Phase 4 synthesis
- `consolidate_results()` - Phase 5 consolidation
- `final_analysis()` - Final analysis and rule generation

## Analysis Pipeline (6-Phase Process)

### Phase 1: Initial Discovery
**Purpose**: Initial exploration of project structure, dependencies, and technology stack

**Agents**:
- **Structure Agent**: Analyzes directory/file organization and architectural components
- **Dependency Agent**: Investigates packages, libraries, and version requirements
- **Tech Stack Agent**: Identifies frameworks, technologies, and best practices

**Output**: JSON-formatted findings from each agent

### Phase 2: Methodical Planning  
**Purpose**: Creates detailed analysis plan based on Phase 1 findings

**Process**:
- Analyzes Phase 1 results to understand project complexity
- Defines specialized agents with specific responsibilities
- Assigns files to relevant agents based on expertise
- Outputs XML-structured plan for Phase 3

**Key Innovation**: Dynamic agent definition based on project characteristics

### Phase 3: Deep Analysis
**Purpose**: Core analysis phase using dynamically created specialized agents

**Dynamic Agent Creation**:
1. Parses XML output from Phase 2 using `agent_parser.py`
2. Creates specialized agents with specific file assignments
3. Each agent analyzes only their assigned files
4. Falls back to predefined agents if parsing fails

**Parallelization**: Agents run concurrently for efficiency

### Phase 4: Synthesis
**Purpose**: Synthesizes findings from Phase 3 into cohesive insights

**Process**:
- Integrates individual agent findings
- Identifies relationships between components  
- Highlights architectural patterns
- Provides holistic system view

### Phase 5: Consolidation
**Purpose**: Creates comprehensive report from all previous phases

**Output**: 
- Organized findings by component/module
- Comprehensive documentation
- Preparation for final analysis

### Final Analysis
**Purpose**: Generates high-level insights and `.cursorrules` file

**Output**:
- System structure mapping
- Architecture pattern identification  
- Improvement recommendations
- Customized Cursor IDE rules

## Configuration System

### Model Configuration (`config/agents.py`)

**Flexible Model Assignment**:
```python
MODEL_CONFIG = {
    "phase1": GEMINI_WITH_REASONING,
    "phase2": GEMINI_WITH_REASONING, 
    "phase3": CLAUDE_WITH_REASONING,
    "phase4": O1_HIGH,
    "phase5": DEEPSEEK_REASONER,
    "final": CLAUDE_WITH_REASONING,
}
```

**Reasoning Modes**:
- **Anthropic**: ENABLED/DISABLED
- **OpenAI**: LOW/MEDIUM/HIGH (for O1/O3-mini), TEMPERATURE (for GPT-4o)
- **DeepSeek**: Always ENABLED
- **Gemini**: ENABLED (thinking models)/DISABLED

### Exclusion System (`config/exclusions.py`)

**Smart Filtering**:
- Excluded directories: `node_modules`, `.git`, `__pycache__`, etc.
- Excluded files: `package-lock.json`, `.env`, `README.md`, etc.  
- Excluded extensions: `.jpg`, `.pyc`, `.log`, etc.

## Utility Components

### File Management
- **Tree Generator** (`tree_generator.py`): Creates project structure representations
- **File Retriever** (`file_retriever.py`): Extracts and formats file contents
- **Phase Output Manager** (`phases_output.py`): Saves analysis results

### Dynamic Agent System
- **Agent Parser** (`agent_parser.py`): Parses XML agent definitions from Phase 2
- **Model Config Helper**: Manages dynamic model configurations
- **Clean Cursor Rules**: Post-processes generated rules files

## Output Structure

### Generated Files
```
project/
├── .cursorrules              # Main output - Cursor IDE rules
├── .cursorignore            # Cursor IDE ignore patterns  
└── phases_output/           # Detailed analysis reports
    ├── phase1_discovery.md
    ├── phase2_planning.md
    ├── phase3_analysis.md  
    ├── phase4_synthesis.md
    ├── phase5_consolidation.md
    ├── final_analysis.md
    └── metrics.md
```

### Metrics Tracking
- Analysis time measurement
- Token usage for reasoning models
- Per-agent execution times
- Model configuration documentation

## Testing Framework

**Comprehensive Test Suite**:
- Individual phase testing (`tests/phase_*_test/`)
- Test data in `tests/tests_input/`
- Mock project structures for validation
- Output verification and comparison

## Key Technical Features

### 1. Asynchronous Processing
- Concurrent agent execution in Phase 1 and Phase 3
- Non-blocking analysis operations
- Improved performance for large codebases

### 2. Dynamic Agent Creation
- Runtime agent definition based on project analysis
- Specialized agents for specific file types/frameworks
- Fallback mechanisms for robust operation

### 3. Multi-Provider Abstraction
- Unified interface across different AI providers
- Provider-specific optimizations (reasoning modes, temperature)
- Easy switching between models for different phases

### 4. Rich CLI Interface
- Progress tracking with spinners
- Colored output for different phases
- Detailed logging with HTTP request filtering

### 5. Modular Architecture
- Clean separation between phases
- Reusable utility components
- Extensible agent system

## Dependencies & Technology Stack

**Core Dependencies**:
- `anthropic` - Anthropic API integration
- `openai` - OpenAI API integration  
- `google-genai` - Google Gemini API integration
- `rich` - Enhanced terminal output
- `typer` - CLI framework
- `pydantic` - Data validation
- `asyncio` - Async operations

## Configuration Flexibility

**Easy Customization**:
1. **Model Selection**: Change AI providers per phase in `config/agents.py`
2. **Prompt Templates**: Modify prompts in `config/prompts/`
3. **Exclusion Patterns**: Update file filtering in `config/exclusions.py`
4. **Agent Definitions**: Customize agent roles and responsibilities

## Usage Workflow

1. **Setup**: Configure API keys for desired providers
2. **Execution**: Run `python main.py -p /path/to/project`  
3. **Analysis**: Tool performs 6-phase analysis automatically
4. **Output**: Generates `.cursorrules`, analysis reports, and metrics

## Innovation Highlights

### 1. Multi-Model Orchestration
- First tool to seamlessly integrate 4 major AI providers
- Dynamic model selection based on task requirements
- Reasoning mode optimization per provider

### 2. Dynamic Agent Architecture  
- Runtime agent creation based on project characteristics
- Specialized analysis for different code patterns
- Self-adapting analysis strategy

### 3. Comprehensive Analysis Pipeline
- Six-phase approach ensures thorough understanding
- Each phase builds on previous insights
- Synthesis and consolidation for holistic view

### 4. Production-Ready Output
- Direct integration with Cursor IDE
- Immediate usability of generated files
- Professional documentation and metrics

This codebase represents a sophisticated approach to automated code analysis, combining the strengths of multiple AI providers with intelligent orchestration and dynamic adaptation to project characteristics.