# CursorRules Architect V2 - System Architecture Analysis

## Executive Summary

CursorRules Architect V2 is a sophisticated multi-agent AI system that analyzes codebases to generate customized `.cursorrules` and `.cursorignore` files for Cursor IDE. The system employs a six-phase analysis pipeline using multiple AI providers (Anthropic Claude, OpenAI, DeepSeek, Google Gemini) with dynamic agent creation and parallel processing.

## Core Architecture

### System Philosophy
The system follows the **"Plan-then-Execute"** model where:
- **The plan IS the prompt** - Phase 2 creates detailed specifications for subsequent analysis
- **Dynamic Agent Creation** - Specialized AI agents are created based on the specific codebase being analyzed
- **Multi-Provider Flexibility** - Different AI models can be used for different phases based on their strengths

### Technology Stack
- **Python 3.8+** with async/await for concurrent processing
- **Multiple AI Providers**: Anthropic, OpenAI, DeepSeek, Google Gemini
- **Rich Console** for beautiful terminal output
- **Click** for CLI interface
- **Pydantic** for data validation

## Six-Phase Analysis Pipeline

### Phase 1: Initial Discovery
**Purpose**: Concurrent analysis by three specialized agents
- **Structure Agent**: Analyzes directory organization and file patterns
- **Dependency Agent**: Investigates package dependencies and requirements
- **Tech Stack Agent**: Identifies frameworks, libraries, and technologies

**Implementation**:
```python
# Three agents run in parallel using asyncio.gather()
agents = [structure_agent, dependency_agent, tech_stack_agent]
results = await asyncio.gather(*[agent.analyze(context) for agent in agents])
```

### Phase 2: Methodical Planning
**Purpose**: Creates a detailed XML-structured analysis plan
- Defines specialized agents based on Phase 1 findings
- Assigns specific files and responsibilities to each agent
- Creates execution blueprint for Phase 3

**Key Innovation**: Dynamic agent definition in XML format:
```xml
<agents>
  <agent name="Backend API Agent" files="api/, models/, controllers/">
    <responsibilities>
      <responsibility>Analyze REST API endpoints</responsibility>
      <responsibility>Review data models and schemas</responsibility>
    </responsibilities>
  </agent>
</agents>
```

### Phase 3: Deep Analysis (The Heart of the System)
**Purpose**: Execute the plan with dynamically created agents
- **Agent Parser** extracts agent definitions from Phase 2's XML output
- **Dynamic Agent Creation** - Each agent focuses only on assigned files
- **Parallel Execution** - All agents run concurrently for efficiency
- **File Retrieval** - Agents read and analyze actual source code

**Fallback Mechanism**: If parsing fails, uses predefined agent templates

### Phase 4: Synthesis
**Purpose**: Integrate findings into cohesive insights
- Combines all agent analysis results
- Identifies architectural patterns and relationships
- Highlights key technical decisions and patterns

### Phase 5: Consolidation
**Purpose**: Create comprehensive project documentation
- Organizes findings by component/module
- Generates structured reports for each area
- Prepares data for final analysis

### Phase 6: Final Analysis
**Purpose**: Generate Cursor IDE-specific rules and insights
- Creates `.cursorrules` file with project-specific guidelines
- Generates `.cursorignore` file with appropriate exclusion patterns
- Provides high-level architectural recommendations

## AI Model Integration Architecture

### Base Architect Pattern
All AI providers implement the `BaseArchitect` abstract class:

```python
class BaseArchitect(ABC):
    @abstractmethod
    async def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]
    
    @abstractmethod
    async def create_analysis_plan(self, phase1_results: Dict) -> Dict
    
    @abstractmethod 
    async def synthesize_findings(self, phase3_results: Dict) -> Dict
```

### Provider-Specific Implementations
- **AnthropicArchitect**: Uses Claude with reasoning modes
- **OpenAIArchitect**: Supports O1, O3-mini, GPT-4o with different reasoning levels
- **DeepSeekArchitect**: Uses DeepSeek Reasoner model
- **GeminiArchitect**: Supports both standard and thinking-enabled Gemini models

### Reasoning Modes
```python
class ReasoningMode(Enum):
    ENABLED = "enabled"      # For thinking-capable models
    DISABLED = "disabled"    # Standard inference
    LOW = "low"             # OpenAI reasoning levels
    MEDIUM = "medium"       
    HIGH = "high"
    TEMPERATURE = "temperature"  # For temperature-based models
```

## Configuration System

### Dynamic Model Assignment
Each phase can use a different AI model:

```python
MODEL_CONFIG = {
    "phase1": GEMINI_WITH_REASONING,     # Fast initial analysis
    "phase2": GEMINI_WITH_REASONING,     # Planning with reasoning
    "phase3": CLAUDE_WITH_REASONING,     # Deep code analysis
    "phase4": O1_HIGH,                   # Complex synthesis
    "phase5": DEEPSEEK_REASONER,         # Consolidation
    "final": CLAUDE_WITH_REASONING,      # Final insights
}
```

### Exclusion Management
Smart filtering of irrelevant files:
```python
EXCLUDED_DIRS = {'node_modules', '.git', '__pycache__', 'dist'}
EXCLUDED_FILES = {'package-lock.json', '.env', '.DS_Store'}
EXCLUDED_EXTENSIONS = {'.pyc', '.jpg', '.png', '.ico'}
```

## Key Innovations

### 1. Dynamic Agent Creation
Unlike static multi-agent systems, this creates agents based on the specific codebase:
- **Phase 2** analyzes the project and defines optimal agents
- **Agent Parser** extracts these definitions from structured output
- **Phase 3** creates and runs these custom agents

### 2. Multi-Provider AI Orchestration
- Different AI models for different cognitive tasks
- Reasoning vs. speed optimization
- Provider-agnostic architecture

### 3. Async Parallel Processing
- All agents in each phase run concurrently
- Significant performance improvements (3-5x faster than sequential)
- Efficient resource utilization

### 4. Comprehensive Output Generation
```
project/
├── .cursorrules              # Generated Cursor IDE rules
├── .cursorignore            # Generated ignore patterns
└── phases_output/           # Detailed analysis reports
    ├── phase1_discovery.md
    ├── phase2_planning.md
    ├── phase3_analysis.md
    ├── phase4_synthesis.md
    ├── phase5_consolidation.md
    ├── final_analysis.md
    └── metrics.md
```

## Utility System

### File Management
- **Tree Generator**: Creates project structure representations
- **File Retriever**: Efficiently reads source code with exclusion filtering
- **Cursor File Management**: Automatically generates and manages `.cursorrules` and `.cursorignore`

### Analysis Tools
- **Agent Parser**: Extracts agent definitions from XML using BeautifulSoup
- **Model Config Helper**: Manages model selection and configuration
- **Metrics Tracking**: Monitors performance and token usage

## Workflow Execution

1. **Initialization**: Load configuration, initialize AI clients for used providers
2. **Tree Generation**: Create filtered project structure representation
3. **Phase Execution**: Sequential execution of 6 phases with parallel agents within each phase
4. **Output Generation**: Create all output files and reports
5. **Cleanup**: Generate metrics and completion notifications

## Design Principles

### 1. Modularity
- Each phase is a separate class with clear responsibilities
- Agent implementations are provider-agnostic
- Configuration is externalized and easily modifiable

### 2. Extensibility
- New AI providers can be added by implementing `BaseArchitect`
- New analysis phases can be inserted into the pipeline
- Prompt templates are externalized for easy customization

### 3. Resilience
- Fallback mechanisms for agent parsing failures
- Error handling and logging throughout
- Graceful degradation when providers are unavailable

### 4. Performance
- Async processing for I/O operations
- Parallel agent execution
- Smart caching and exclusion filtering

## Use Cases

1. **Code Migration**: Understand large legacy codebases
2. **Team Onboarding**: Generate comprehensive project documentation
3. **Cursor IDE Setup**: Create optimal development environment rules
4. **Architecture Analysis**: Identify patterns and improvement opportunities
5. **Documentation Generation**: Automated project documentation

This system represents a sophisticated approach to AI-powered code analysis, combining the strengths of multiple AI providers with intelligent orchestration and dynamic adaptation to specific codebases.