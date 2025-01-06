# 🦊 CursorRules Architect

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-o1--preview-blue.svg)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-claude--3.5--sonnet-purple.svg)](https://www.anthropic.com/)
[![Built By](https://img.shields.io/badge/Built%20By-SlyyCooper-orange.svg)](https://github.com/SlyyCooper)

**Automate Your .cursorrules Like a Pro 🚀**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

## 🌟 What's This About?

Tired of manually writing `.cursorrules` files? Look no further! CursorRules Architect automates the creation of `.cursorrules` by analyzing your project's structure, tech stack, and coding patterns. It's like having a smart AI assistant that knows exactly how you want your code to look and feel.

## ✨ Features

- 🤖 **Intelligent Rule Generation** - Creates `.cursorrules` files tailored to your project
- 🔍 **Deep Project Analysis** - Understands your codebase thoroughly using multi-phase analysis
- 📊 **Tech Stack Detection** - Identifies frameworks and libraries used
- 🎨 **Style Recognition** - Learns your coding style automatically
- 📝 **Comprehensive Documentation** - Generates clear and helpful docs
- 🚀 **Cursor IDE Integration** - Seamless plug-and-play functionality
- 🔄 **Async Processing** - Parallel agent execution for faster analysis
- 📑 **Detailed Phase Outputs** - Separate markdown files for each analysis phase
- 📈 **Performance Metrics** - Track analysis time and token usage

## 🛠️ Requirements

- Python 3.8+
- OpenAI API key (`o1-preview` access)
- Anthropic API key (`claude-3.5-sonnet` access)
- Cursor IDE
- `rich` library for beautiful terminal output
- `typer` for CLI interface
- `watchdog` for file monitoring
- `asyncio` for async operations

## ⚡ Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/slyycooper/cursorrules-architect.git
   cd cursorrules-architect
   pip install -r requirements.txt
   ```

2. **Set Up Your API Keys**
   ```bash
   # Linux/macOS
   export OPENAI_API_KEY='your-openai-api-key'
   export ANTHROPIC_API_KEY='your-anthropic-api-key'

   # Windows
   set OPENAI_API_KEY=your-openai-api-key
   set ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

3. **Run the Tool**
   ```bash
   python main.py -p /path/to/your/project
   ```

## 🔄 How It Works

CursorRules Architect uses a sophisticated multi-phase analysis system that alternates between Claude-3.5-Sonnet and o1-preview models:

### Phase 1: Initial Discovery (Claude-3.5-Sonnet)
- Runs three parallel agents using `asyncio`:
  1. **Structure Agent**: Analyzes directory/file organization
  2. **Dependency Agent**: Investigates packages and libraries
  3. **Tech Stack Agent**: Identifies frameworks and technologies

### Phase 2: Methodical Planning (o1-preview)
- Takes findings from Phase 1 agents
- Creates detailed analysis plan
- Tracks reasoning tokens
- Plans next phase execution

### Phase 3: Deep Analysis (Claude-3.5-Sonnet)
- Runs four specialized agents:
  1. **Code Analysis Agent**: Examines logic patterns
  2. **Dependency Mapping Agent**: Maps file relationships
  3. **Architecture Agent**: Studies design patterns
  4. **Documentation Agent**: Creates documentation

### Phase 4: Synthesis (o1-preview)
- Reviews and synthesizes Phase 3 findings
- Updates analysis directions
- Identifies areas needing deeper investigation
- Tracks reasoning tokens

### Phase 5: Consolidation (Claude-3.5-Sonnet)
- Final consolidation of all findings
- Creates comprehensive documentation
- Prepares final report

### Final Analysis (o1-preview)
- Complete system structure mapping
- Documents relationships
- Provides improvement recommendations
- Tracks reasoning tokens

## 📂 Output Structure

The tool generates multiple output files:

```
your-project/
├── phases_output/
│   ├── phase1_discovery.md      # Initial agent findings
│   ├── phase2_planning.md       # Planning document
│   ├── phase3_analysis.md       # Deep analysis results
│   ├── phase4_synthesis.md      # Synthesized findings
│   ├── phase5_consolidation.md  # Consolidated report
│   ├── final_analysis.md        # Final recommendations
│   └── complete_report.md       # Overview with metrics
├── your-project_analysis.txt    # Complete analysis output
└── .cursorrules                 # Generated rules file
```

## 🔍 Analysis Details

### Parallel Processing
- Phase 1 runs multiple agents simultaneously using `asyncio.gather`
- Each agent makes independent API calls
- Results are combined before proceeding to next phase

### Token Tracking
- Monitors token usage for o1-preview phases
- Tracks reasoning tokens separately
- Provides detailed metrics in final report

### Performance Metrics
- Total analysis time
- Per-phase token usage
- Agent execution times
- API call statistics

## 🛠️ Advanced Usage

### Custom Exclusions
```bash
python main.py -p /path/to/project --exclude "node_modules,dist,build"
```

### Output Directory
```bash
python main.py -p /path/to/project -o custom_output.txt
```

### Monitoring Mode
```bash
python monitoring-cursorrules.py -p /path/to/project
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.