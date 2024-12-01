#!/usr/bin/env python3

from pathlib import Path
import logging
from rich.console import Console
from rich.logging import RichHandler
from typing import List, Dict
import json
from datetime import datetime
from anthropic import Anthropic
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
import argparse
from rich import print as rprint
import questionary
from questionary import Style
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging and clients
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)]
)
logger = logging.getLogger("cursor_monitor")
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MONITORED_EXTENSIONS = {
    '.py', '.ts', '.tsx', '.json', '.js', '.jsx',
    '.txt', '.env', '.env.local', '.env.development',
    '.env.production', '.firestore'
}

# Add custom questionary style
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),     # token in front of the question
    ('question', 'bold'),             # question text
    ('answer', 'fg:#f44336 bold'),    # submitted answer text
    ('pointer', 'fg:#673ab7 bold'),   # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#673ab7 bold'),# pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),       # style for a selected item of a checkbox
    ('separator', 'fg:#6C6C6C'),      # separator in lists
    ('instruction', 'fg:#808080'),    # user instructions for select, rawselect, checkbox
    ('text', ''),                     # plain text
    ('disabled', 'fg:#858585 italic') # disabled choices for select and checkbox prompts
])

def interactive_cli() -> dict:
    """Interactive CLI interface"""
    answers = {}
    
    # Ask for command
    answers['command'] = questionary.select(
        "What would you like to do?",
        choices=[
            {
                'name': 'Watch directory for changes',
                'value': 'watch'
            },
            {
                'name': 'Run one-time analysis',
                'value': 'analyze'
            }
        ],
        style=custom_style
    ).ask()

    # Get directory path and convert to absolute path
    path = questionary.path(
        "Enter the directory path:",
        only_directories=True,
        style=custom_style
    ).ask()
    answers['path'] = str(Path(path).resolve())  # Convert to absolute path

    # If watch command selected, get additional options
    if answers['command'] == 'watch':
        # Ask for file extensions
        if questionary.confirm(
            "Would you like to specify which file extensions to monitor?",
            default=False,
            style=custom_style
        ).ask():
            extensions = questionary.text(
                "Enter file extensions to monitor (comma-separated, e.g., py,ts,tsx):",
                style=custom_style
            ).ask()
            answers['include'] = extensions if extensions else None

        # Ask for cooldown period
        answers['cooldown'] = questionary.text(
            "Enter cooldown period in seconds (default: 5):",
            default="5",
            validate=lambda text: text.isdigit() and int(text) > 0,
            style=custom_style
        ).ask()
        answers['cooldown'] = int(answers['cooldown'])

        # Ask for excluded directories
        if questionary.confirm(
            "Would you like to specify directories to exclude?",
            default=False,
            style=custom_style
        ).ask():
            excluded = questionary.text(
                "Enter directories to exclude (comma-separated, e.g., node_modules,dist):",
                style=custom_style
            ).ask()
            answers['exclude'] = excluded if excluded else None

    return answers

class Args:
    """Simple class to mimic argparse.Namespace"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, analyzer, monitored_extensions=None, cooldown=5):
        self.analyzer = analyzer
        self.last_run = 0
        self.cooldown = cooldown
        self.monitored_extensions = monitored_extensions or MONITORED_EXTENSIONS

    def on_any_event(self, event):
        if event.is_directory:
            return
        
        # Check if file extension should be monitored
        file_path = Path(event.src_path)
        if file_path.suffix not in self.monitored_extensions:
            return

        # Handle file events with cooldown
        current_time = time.time()
        if current_time - self.last_run >= self.cooldown:
            if event.type in ['created', 'deleted']:
                logger.info(f"File {event.type}: {event.src_path}")
                asyncio.run(self.analyzer.analyze())
                self.last_run = current_time

class ProjectAnalyzer:
    def __init__(self, directory: Path):
        self.directory = directory
        self.project_type = self._detect_project_type()
        self.env_vars = self._parse_env_files()
        self.system_prompt = self._get_system_prompt()
    
    def _detect_project_type(self) -> dict:
        """Detect project types and tech stack based on files and structure"""
        stack = {
            'frontend': set(),
            'backend': set(),
            'services': set(),
            'deployment': set()
        }
        
        # Frontend Detection
        if any((self.directory / path).exists() for path in ['next.config.js', 'next.config.mjs']):
            stack['frontend'].add('nextjs')
        if (self.directory / 'package.json').exists():
            with open(self.directory / 'package.json') as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                if 'react' in deps:
                    stack['frontend'].add('react')
                if '@chakra-ui/react' in deps:
                    stack['frontend'].add('chakra-ui')
                if 'tailwindcss' in deps:
                    stack['frontend'].add('tailwind')
                if 'framer-motion' in deps:
                    stack['frontend'].add('framer-motion')
                if '@emotion/react' in deps:
                    stack['frontend'].add('emotion')

        # Backend Detection
        requirements_files = ['requirements.txt', 'pyproject.toml', 'Pipfile']
        for req_file in requirements_files:
            if (self.directory / req_file).exists():
                with open(self.directory / req_file) as f:
                    content = f.read().lower()
                    if 'fastapi' in content:
                        stack['backend'].add('fastapi')
                    if 'pydantic' in content:
                        stack['backend'].add('pydantic')
                    if 'uvicorn' in content:
                        stack['backend'].add('uvicorn')

        # Service Integrations
        if any((self.directory / path).exists() for path in ['.firebaserc', 'firebase.json']):
            stack['services'].add('firebase')
        if any('stripe' in f.name.lower() for f in self.directory.rglob('*')):
            stack['services'].add('stripe')
        if any('openapi' in f.name.lower() for f in self.directory.rglob('*')):
            stack['services'].add('openapi')

        # Environment Files
        env_files = ['.env', '.env.local', '.env.development', '.env.production']
        for env_file in env_files:
            if (self.directory / env_file).exists():
                with open(self.directory / env_file) as f:
                    content = f.read().lower()
                    if 'firebase' in content:
                        stack['services'].add('firebase')
                    if 'stripe' in content:
                        stack['services'].add('stripe')
                    if 'openai' in content:
                        stack['services'].add('openai')

        return stack

    def _get_system_prompt(self) -> str:
        """Get appropriate system prompt based on detected tech stack"""
        prompts = []
        
        if 'nextjs' in self.project_type['frontend']:
            prompts.append("""
            # Frontend Analysis (Next.js)
            1. Project Structure
               - App Router organization (/app directory)
               - Component hierarchy and reusability
               - API routes and endpoints
               - Environment configuration

            2. Key Features
               - Server/Client components usage
               - Data fetching patterns
               - Authentication flow
               - State management
               - UI component library integration
            """)
            
        if 'fastapi' in self.project_type['backend']:
            prompts.append("""
            # Backend Analysis (FastAPI)
            1. API Structure
               - Route organization
               - Endpoint definitions
               - Request/Response models
               - Middleware configuration

            2. Core Features
               - Authentication system
               - Database integration
               - File handling
               - Service integrations
               - Environment configuration
            """)
            
        if 'firebase' in self.project_type['services']:
            prompts.append("""
            # Firebase Integration
            1. Services Used
               - Authentication
               - Firestore
               - Storage
               - Hosting
               - Security Rules
            """)

        if 'stripe' in self.project_type['services']:
            prompts.append("""
            # Payment Integration
            1. Stripe Setup
               - Payment flows
               - Subscription handling
               - Webhook configuration
               - Product/Price IDs
            """)

        base_prompt = """# Project Overview
1. Directory Structure
2. Tech Stack
3. Key Components
4. Configuration
5. Dependencies
6. Environment Setup
7. Deployment
"""
        
        return base_prompt + "\n".join(prompts)

    def _generate_tree(self, startpath: Path, exclude_patterns: List[str] = None) -> str:
        """Generate ASCII tree structure of the project"""
        if exclude_patterns is None:
            exclude_patterns = [
                # Directories to exclude
                'node_modules', '__pycache__', '.git', '.next', 'venv',
                # Common repository files
                '.DS_Store', '.cursorignore', '.cursorrules', 'LICENSE',
                'README.md', 'citation.cff', '__init__.py',
                # Binary and cache files
                '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
                # Package files
                'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                # Media files
                '.svg', '.png', '.jpg', '.jpeg', '.gif',
                # Editor files
                '.vscode', '.idea', '.vs'
            ]
            
        # Ensure startpath is a Path object
        startpath = Path(startpath)
        
        tree = []
        for root, dirs, files in os.walk(startpath):
            # Convert root to Path for relative_to
            root_path = Path(root)
            
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
            
            try:
                level = root_path.relative_to(startpath).parts
                indent = '│   ' * (len(level))
                if level:
                    dirname = os.path.basename(root)
                    # Skip if directory name matches exclude patterns
                    if not any(pattern in dirname.lower() for pattern in exclude_patterns):
                        tree.append(f"{indent[:-4]}├── {dirname}/")
                
                # Filter and sort files
                visible_files = []
                for file in sorted(files):
                    # Skip files matching exclude patterns
                    if not any(pattern in file.lower() for pattern in exclude_patterns):
                        visible_files.append(file)
                
                # Add files to tree
                for file in visible_files:
                    tree.append(f"{indent}├── {file}")
                    
            except ValueError as e:
                logger.error(f"Error processing path {root}: {e}")
                continue
                
        return "\n".join(tree)

    def _parse_env_files(self) -> dict:
        """Parse and categorize environment variables from .env files"""
        env_files = ['.env', '.env.local', '.env.development', '.env.production']
        env_vars = {
            'client': {
                'firebase': [],
                'api': [],
                'stripe': [],
                'other': []
            },
            'server': {
                'firebase': [],
                'openai': [],
                'stripe': [],
                'database': [],
                'auth': [],
                'api': [],
                'other': []
            }
        }

        for env_file in env_files:
            env_path = self.directory / env_file
            if env_path.exists():
                try:
                    with open(env_path) as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key = line.split('=')[0].strip()
                                value = line.split('=')[1].strip() if len(line.split('=')) > 1 else ''
                                
                                # Categorize the variable
                                if key.startswith('NEXT_PUBLIC_'):
                                    if 'FIREBASE' in key:
                                        env_vars['client']['firebase'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    elif 'API' in key:
                                        env_vars['client']['api'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    elif 'STRIPE' in key:
                                        env_vars['client']['stripe'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    else:
                                        env_vars['client']['other'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                else:
                                    if 'FIREBASE' in key or 'FB_' in key:
                                        env_vars['server']['firebase'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    elif 'OPENAI' in key or 'GPT' in key:
                                        env_vars['server']['openai'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    elif 'STRIPE' in key:
                                        env_vars['server']['stripe'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    elif 'DB_' in key or 'DATABASE' in key:
                                        env_vars['server']['database'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    elif 'AUTH' in key or 'JWT' in key:
                                        env_vars['server']['auth'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    elif 'API' in key:
                                        env_vars['server']['api'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                                    else:
                                        env_vars['server']['other'].append({
                                            'key': key,
                                            'source': env_file,
                                            'description': self._get_env_var_description(key)
                                        })
                except Exception as e:
                    logger.error(f"Error reading {env_file}: {e}")

        return env_vars

    def _get_env_var_description(self, key: str) -> str:
        """Get description for environment variables based on common patterns"""
        descriptions = {
            # Firebase Client
            'NEXT_PUBLIC_FIREBASE_API_KEY': 'Firebase Web API Key for client-side initialization',
            'NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN': 'Firebase Auth domain for client-side auth',
            'NEXT_PUBLIC_FIREBASE_PROJECT_ID': 'Firebase project ID for client-side initialization',
            'NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET': 'Firebase storage bucket for client-side file operations',
            'NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID': 'Firebase messaging sender ID for client-side notifications',
            'NEXT_PUBLIC_FIREBASE_APP_ID': 'Firebase app ID for client-side initialization',
            
            # Firebase Server
            'FIREBASE_PRIVATE_KEY': 'Firebase Admin SDK private key for server-side operations',
            'FIREBASE_CLIENT_EMAIL': 'Firebase Admin SDK client email for server-side auth',
            'FIREBASE_PROJECT_ID': 'Firebase project ID for server-side initialization',
            
            # Stripe
            'NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY': 'Stripe publishable key for client-side payments',
            'STRIPE_SECRET_KEY': 'Stripe secret key for server-side payment processing',
            'STRIPE_WEBHOOK_SECRET': 'Stripe webhook secret for server-side event handling',
            
            # OpenAI
            'OPENAI_API_KEY': 'OpenAI API key for server-side AI operations',
            
            # API
            'NEXT_PUBLIC_API_URL': 'Base API URL for client-side requests',
            'API_URL': 'Base API URL for server-side operations',
            
            # Auth
            'JWT_SECRET': 'Secret key for JWT token signing',
            'AUTH_SECRET': 'Secret key for authentication',
            
            # Database
            'DATABASE_URL': 'Database connection string',
            'DB_HOST': 'Database host address',
            'DB_PORT': 'Database port number',
            'DB_NAME': 'Database name',
            'DB_USER': 'Database user',
            'DB_PASSWORD': 'Database password'
        }
        
        return descriptions.get(key, 'Configuration variable')

    async def analyze(self) -> str:
        """Generate .cursorrules content and save to file"""
        try:
            # Generate project structure
            tree = self._generate_tree(self.directory)
            
            # Analyze tech stack
            tech_analysis = []
            for category, items in self.project_type.items():
                if items:
                    tech_analysis.append(f"# {category.title()} Stack")
                    for item in sorted(items):
                        tech_analysis.append(f"- {item}")
            
            # Generate environment variables section
            env_sections = []
            
            # Client-side variables
            env_sections.append("\n# Client-Side Environment Variables")
            for category, vars in self.env_vars['client'].items():
                if vars:
                    env_sections.append(f"\n## {category.title()}")
                    for var in vars:
                        env_sections.append(f"- {var['key']}")
                        env_sections.append(f"  - Source: {var['source']}")
                        env_sections.append(f"  - Description: {var['description']}")
            
            # Server-side variables
            env_sections.append("\n# Server-Side Environment Variables")
            for category, vars in self.env_vars['server'].items():
                if vars:
                    env_sections.append(f"\n## {category.title()}")
                    for var in vars:
                        env_sections.append(f"- {var['key']}")
                        env_sections.append(f"  - Source: {var['source']}")
                        env_sections.append(f"  - Description: {var['description']}")
            
            # Combine all sections
            content = [
                "# Project Structure",
                "```",
                tree,
                "```\n",
                *tech_analysis,
                *env_sections
            ]
            
            # Convert content to string
            output = "\n".join(content)
            
            # Save to .cursorrules file
            cursorrules_path = self.directory / '.cursorrules'
            try:
                with open(cursorrules_path, 'w', encoding='utf-8') as f:
                    f.write(output)
                logger.info(f"Successfully saved .cursorrules file to: {cursorrules_path}")
                return f"Analysis complete! .cursorrules file saved to: {cursorrules_path}\n\nContent Preview:\n{output[:500]}..."
            except Exception as e:
                logger.error(f"Error saving .cursorrules file: {e}")
                return f"Error saving .cursorrules file: {str(e)}"
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return f"Error during analysis: {str(e)}"

async def monitor_directory(args: Args):
    """Monitor directory for changes and update .cursorrules file"""
    try:
        # Convert directory path to Path object
        directory = Path(args.path)
        if not directory.exists():
            logger.error(f"Directory not found: {args.path}")
            return

        analyzer = ProjectAnalyzer(directory)
        
        if args.command == 'watch':
            logger.info(f"Monitoring directory: {directory}")
            event_handler = FileChangeHandler(
                analyzer=analyzer,
                monitored_extensions=set(args.include.split(',')) if args.include else None,
                cooldown=args.cooldown
            )
            observer = Observer()
            observer.schedule(event_handler, str(directory), recursive=True)
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                observer.join()
        else:
            logger.info(f"Analyzing directory: {directory}")
            result = await analyzer.analyze()
            logger.info(f"\nAnalysis complete! Results saved to: {result}")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")

async def analyze_directory(args: argparse.Namespace):
    """Run one-time analysis"""
    try:
        directory = Path(args.path).resolve()
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Invalid directory path: {args.path}")
            return

        analyzer = ProjectAnalyzer(directory)
        rprint(f"\n[bold green]Analyzing directory:[/] {directory}")
        result = await analyzer.analyze()
        rprint(f"\n[bold green]Analysis complete![/] Results saved to: {result}\n")

    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == '__main__':
    try:
        # Get answers from interactive CLI
        answers = interactive_cli()
        
        # Convert answers to Args object with defaults
        args = Args(
            path=answers['path'],
            command=answers['command'],
            include=answers.get('include'),
            cooldown=answers.get('cooldown', 5),
            exclude=answers.get('exclude')
        )
        
        if args.command == 'watch':
            rprint("\n[bold blue]Starting directory monitor...[/]")
            asyncio.run(monitor_directory(args))
        elif args.command == 'analyze':
            rprint("\n[bold blue]Starting analysis...[/]")
            asyncio.run(analyze_directory(args))
            
    except KeyboardInterrupt:
        rprint("\n[bold red]Operation cancelled by user[/]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
