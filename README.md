# 🦊 CursorRules Architect

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-o1--preview-blue.svg)](https://openai.com/)
[![Anthropic](https://img.shields.io/badge/Anthropic-claude--3-purple.svg)](https://anthropic.com/)
[![Built By](https://img.shields.io/badge/Built%20By-SlyyCooper-orange.svg)](https://github.com/SlyyCooper)

**Automate Your .cursorrules Like a Boss 🚀**

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

## 🌟 What's This About?

Tired of manually writing `.cursorrules` files? Say no more fam! I built this tool to automatically generate perfect `.cursorrules` files by analyzing your project's DNA. It's like having a smart AI assistant that knows exactly how you want your code to look and feel.

## ✨ Features That Slap

- 🤖 **Smart AF Generation** - Creates `.cursorrules` files that just work
- 🔍 **Deep Project Analysis** - Understands your code like it wrote it
- 📊 **Tech Stack Detection** - Knows your tools before you tell it
- 🎨 **Style Reading** - Learns your coding style automatically
- 📝 **Documentation Setup** - Because who likes writing docs?
- 🚀 **Cursor IDE Ready** - Plug and play, no hassle

## 🛠️ What You Need

- Python 3.8+
- OpenAI API key (o1-preview access)
- Anthropic API key (claude-3-5-sonnet access)
- Cursor IDE (you know you want it)

## ⚡ Let's Get This Party Started

1. **Grab the Code**
```bash
git clone https://github.com/slyycooper/cursorrules-architect.git
cd cursorrules-architect
pip install -r requirements.txt
```

2. **Set Up Your Keys**
```bash
# Linux/macOS Gang
export OPENAI_API_KEY='your-openai-api-key'
export ANTHROPIC_API_KEY='your-anthropic-api-key'

# Windows Squad
$env:OPENAI_API_KEY='your-openai-api-key'
$env:ANTHROPIC_API_KEY='your-anthropic-api-key'
```

3. **Generate Some Rules**
```bash
python project_extractor.py -p /path/to/your/awesome/project
```

## 🔄 How This Bad Boy Works

1. **Project Analysis** `Claude-3-5-sonnet`
   - Scans your project like a boss
   - Spots those coding patterns
   - Figures out your tech stack

2. **Rules Planning** `o1-preview`
   - Plans the perfect rules
   - Makes sure everything fits

3. **Rules Generation** `Claude-3-5-sonnet`
   - Drops that `.cursorrules` file
   - Sets up your style guide
   - Configures AI just right

4. **Quality Check** `o1-preview`
   - Makes sure everything's tight
   - Keeps it all compatible

5. **Documentation** `Claude-3-5-sonnet`
   - Explains what's what
   - Keeps it clean and clear

## 📝 Example Output

```yaml
PROJECT_NAME: Your Dope Project
CODING_STYLE: Whatever Flows
FRAMEWORK: Your Choice
TEST_FRAMEWORK: Pick Your Poison
DOCUMENTATION: Keep It Clean
AI_BEHAVIOR:
  - Write code that slaps
  - Keep it maintainable
  - Make it scale
```

## 🔒 Security First

Your keys and project data are safe with me. No sketchy business here.

## 🤝 Want to Help?

Got ideas? Let's make this even better! Check out the [Contributing Guide](CONTRIBUTING.md).

1. Fork it
2. Make it better
3. Show me what you got
4. Let's merge it

## 📄 License

[MIT License](LICENSE) - Do your thing with it!

---

<div align="center">
Built with 🦊 by <a href="https://github.com/SlyyCooper">SlyyCooper</a>
</div> 