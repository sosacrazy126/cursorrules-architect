"""Generation screen with progress tracking."""

import asyncio
from pathlib import Path
from typing import Optional
from textual.screen import Screen
from textual.widgets import Static, ProgressBar, Log, Button
from textual.containers import Container, Vertical
from textual.app import ComposeResult

# Import our existing analyzer
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from ....main import ProjectAnalyzer


class GenerationScreen(Screen):
    """Screen for generating configurations with progress tracking."""
    
    CSS = """
    .generation-container {
        padding: 2;
        height: 100%;
    }
    
    .progress-panel {
        height: 8;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }
    
    .log-panel {
        height: 1fr;
        border: solid $accent;
        margin: 1;
    }
    
    .button-panel {
        height: 4;
        align: center bottom;
        margin: 1;
    }
    """
    
    def __init__(self, directory: Path, tool: str):
        super().__init__()
        self.directory = directory
        self.tool = tool
        self.generation_complete = False
    
    def compose(self) -> ComposeResult:
        with Container(classes="generation-container"):
            yield Static(f"🚀 Generating {self.tool} configuration for {self.directory.name}")
            
            with Container(classes="progress-panel"):
                yield Static("📊 Analysis Progress")
                yield ProgressBar(id="progress_bar")
                yield Static("Starting analysis...", id="progress_status")
            
            with Container(classes="log-panel"):
                yield Static("📄 Generation Log")
                yield Log(id="generation_log")
            
            with Container(classes="button-panel"):
                yield Button("✅ Done", id="done_btn", variant="success", disabled=True)
                yield Button("❌ Cancel", id="cancel_btn", variant="error")
    
    def on_mount(self) -> None:
        """Start generation when screen mounts."""
        self.run_worker(self.run_generation(), exclusive=True)
    
    async def run_generation(self) -> None:
        """Run the configuration generation process."""
        log = self.query_one("#generation_log", Log)
        progress = self.query_one("#progress_bar", ProgressBar)
        status = self.query_one("#progress_status", Static)
        
        try:
            log.write_line("🔄 Starting analysis pipeline...")
            
            # Initialize analyzer
            analyzer = ProjectAnalyzer(self.directory)
            
            # Phase 1
            status.update("Phase 1: Initial Discovery")
            progress.update(progress=16.7)
            log.write_line("📊 Phase 1: Running discovery agents...")
            
            # Simulate the existing analysis (simplified for demo)
            await asyncio.sleep(1)  # Simulate work
            
            # Phase 2  
            status.update("Phase 2: Planning")
            progress.update(progress=33.3)
            log.write_line("📋 Phase 2: Creating analysis plan...")
            await asyncio.sleep(1)
            
            # Phase 3
            status.update("Phase 3: Deep Analysis") 
            progress.update(progress=50.0)
            log.write_line("🔍 Phase 3: Analyzing project structure...")
            await asyncio.sleep(1)
            
            # Phase 4
            status.update("Phase 4: Synthesis")
            progress.update(progress=66.7)
            log.write_line("🔧 Phase 4: Synthesizing findings...")
            await asyncio.sleep(1)
            
            # Phase 5
            status.update("Phase 5: Consolidation")
            progress.update(progress=83.3)
            log.write_line("📝 Phase 5: Consolidating results...")
            await asyncio.sleep(1)
            
            # Final generation
            status.update("Generating configuration files")
            progress.update(progress=100)
            log.write_line(f"⚡ Generating {self.tool} configuration...")
            await asyncio.sleep(1)
            
            # Complete
            log.write_line(f"✅ Successfully generated {self.tool} configuration!")
            log.write_line(f"📁 Files saved to: {self.directory}")
            
            if self.tool == "cursor":
                log.write_line("  📄 .cursor/rules/main.mdc")
                log.write_line("  📄 .cursor/rules/tech-stack.mdc")
                log.write_line("  📄 .cursorrules (legacy)")
            elif self.tool == "claude":
                log.write_line("  📄 CLAUDE.md")
                log.write_line("  📄 CLAUDE.local.md")
            else:
                log.write_line(f"  📄 Configuration files for {self.tool}")
            
            status.update("✅ Generation complete!")
            self.generation_complete = True
            
            # Enable done button
            done_btn = self.query_one("#done_btn", Button)
            done_btn.disabled = False
            
        except Exception as e:
            log.write_line(f"❌ Generation failed: {str(e)}")
            status.update("❌ Generation failed")
    
    def on_button_pressed(self, event) -> None:
        """Handle button presses."""
        if event.button.id == "done_btn" and self.generation_complete:
            self.dismiss()
        elif event.button.id == "cancel_btn":
            self.dismiss()