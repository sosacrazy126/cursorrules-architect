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
- 🔍 **Deep Project Analysis** - Understands your codebase thoroughly
- 📊 **Tech Stack Detection** - Identifies frameworks and libraries used
- 🎨 **Style Recognition** - Learns your coding style automatically
- 📝 **Comprehensive Documentation** - Generates clear and helpful docs
- 🚀 **Cursor IDE Integration** - Seamless plug-and-play functionality

## 🛠️ Requirements

- Python 3.8+
- OpenAI API key (`o1-preview` access)
- Anthropic API key (`claude-3.5-sonnet` access)
- Cursor IDE

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
   python project_extractor.py -p /path/to/your/project
   ```

## 🔄 How It Works

CursorRules Architect follows a multi-phase analysis flow to generate your `.cursorrules`:

1. **Initial Discovery** (`Claude-3.5-Sonnet`)
   - **Structure Agent**: Analyzes directory and file organization
   - **Dependency Agent**: Examines package dependencies
   - **Tech Stack Agent**: Identifies frameworks and technologies used

2. **Methodical Planning** (`o1-preview`)
   - Processes agent findings
   - Creates a detailed, step-by-step analysis plan
   - Tracks reasoning tokens (unique to `o1-preview`)

3. **Deep Analysis** (`Claude-3.5-Sonnet`)
   - **Code Analysis Agent**: Examines core logic and patterns
   - **Dependency Mapping Agent**: Maps file relationships
   - **Architecture Agent**: Studies design patterns
   - **Documentation Agent**: Generates comprehensive documentation

4. **Synthesis** (`o1-preview`)
   - Reviews and synthesizes deep analysis findings
   - Updates analysis directions
   - Tracks reasoning tokens

5. **Consolidation** (`Claude-3.5-Sonnet`)
   - Combines all findings
   - Prepares comprehensive documentation

6. **Final Analysis** (`o1-preview`)
   - Completes system structure mapping
   - Documents relationships
   - Provides improvement recommendations
   - Tracks reasoning tokens

## ⚠️ Critical Model Notes

**Important:** These models are fixed and must **never** be changed:

- **Claude-3.5-Sonnet-20241022** (Anthropic)
- **o1-preview** (OpenAI)

### Special Note on `o1-preview`

The `o1-preview` model is **contractually bound** and operates differently from standard OpenAI models:

- Must be treated as a dedicated contract
- Cannot be substituted with other OpenAI models
- Has unique reasoning token tracking capabilities
- Specialized for methodical planning and synthesis

## 📝 Example Output

```yaml
PROJECT_NAME: Your Awesome Project
CODING_STYLE: Follows PEP 8 Standards
FRAMEWORK: Your Framework
TEST_FRAMEWORK: Your Test Framework
DOCUMENTATION: Automatically Generated
AI_BEHAVIOR:
  - Write clean and efficient code
  - Adhere to project conventions
  - Ensure scalability and maintainability
```

## 🔒 Security First

Your API keys and project data are secure. We prioritize your privacy and do not store sensitive information.

## 🤝 Contributing

Got ideas? Let's make this even better! Check out the [Contributing Guide](CONTRIBUTING.md).

1. **Fork the Repository**
2. **Create a Feature Branch** (`git checkout -b feature/YourFeature`)
3. **Commit Changes** (`git commit -m 'Add a cool feature'`)
4. **Push to Branch** (`git push origin feature/YourFeature`)
5. **Open a Pull Request**

## 📄 License

This project is licensed under the [MIT License](LICENSE) - feel free to use it!

---

<div align="center">
Built with ❤️ by <a href="https://github.com/SlyyCooper">SlyyCooper</a>
</div> 