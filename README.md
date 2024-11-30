# CursorRules Architect 🚀

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-o1--preview-blue.svg)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-claude--3-purple.svg)](https://anthropic.com/)

**Automate Your .cursorrules Creation with AI-Powered Intelligence**

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

## 🌟 Overview

CursorRules Architect is your AI-powered assistant for creating and managing `.cursorrules` files. Say goodbye to tedious manual configuration! Our tool analyzes your project structure, tech stack, and coding patterns to automatically generate the perfect `.cursorrules` file that aligns with your project's needs and coding standards.

## ✨ Features

- 🤖 **Smart Rules Generation** - Automatically creates optimal `.cursorrules` files
- 🔍 **Project Analysis** - Deep understanding of your codebase and requirements
- 📊 **Tech Stack Detection** - Identifies frameworks and coding patterns
- 🎨 **Style Inference** - Learns your coding style and conventions
- 📝 **Documentation Rules** - Sets up documentation standards automatically
- 🚀 **Easy Integration** - Works seamlessly with Cursor IDE

## 🛠️ Prerequisites

- Python 3.8+
- OpenAI API key (o1-preview access)
- Anthropic API key (claude-3-5-sonnet access)
- Cursor IDE installed (recommended)

## ⚡ Quick Start

1. **Install**
```bash
git clone https://github.com/slyycooper/cursorrules-architect.git
cd cursorrules-architect
pip install -r requirements.txt
```

2. **Configure API Keys**
```bash
# Linux/macOS
export OPENAI_API_KEY='your-openai-api-key'
export ANTHROPIC_API_KEY='your-anthropic-api-key'

# Windows (PowerShell)
$env:OPENAI_API_KEY='your-openai-api-key'
$env:ANTHROPIC_API_KEY='your-anthropic-api-key'
```

3. **Generate Rules**
```bash
python project_extractor.py -p /path/to/project
```

## 🔄 How It Works

1. **Project Analysis** `Claude-3-5-sonnet`
   - Scans project structure
   - Identifies coding patterns
   - Detects tech stack and dependencies

2. **Rules Planning** `o1-preview`
   - Determines optimal rules
   - Plans configuration strategy

3. **Rules Generation** `Claude-3-5-sonnet`
   - Creates `.cursorrules` file
   - Sets up style guidelines
   - Configures AI behavior

4. **Validation** `o1-preview`
   - Verifies rules effectiveness
   - Ensures compatibility

5. **Documentation** `Claude-3-5-sonnet`
   - Explains rule choices
   - Provides usage guidance

## 📝 Example .cursorrules

```plaintext
PROJECT_NAME: My Awesome Project
CODING_STYLE: Google
FRAMEWORK: React
TEST_FRAMEWORK: Jest
DOCUMENTATION: JSDoc
AI_BEHAVIOR:
  - Prefer functional components
  - Use TypeScript types
  - Follow React best practices
```

## 🔒 Security

We prioritize security. API keys are handled safely and no sensitive project information is stored or transmitted.

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

[MIT License](LICENSE) - feel free to use this project for your own purposes!

---

<div align="center">
Made with ❤️ by the CursorRules Team
</div> 