"""Progress visualization for reconner."""

import time
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskID
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    from rich.layout import Layout
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class ProgressManager:
    """Manages progress visualization for tools."""
    
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        if RICH_AVAILABLE and not quiet:
            self.console = Console()
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=self.console
            )
        else:
            self.console = None
            self.progress = None
    
    def show_tool_start(self, tool_name: str, step: int, total: int, description: str = ""):
        """Show tool start message."""
        if not self.console or self.quiet:
            return
        
        emoji_map = {
            'subfinder': '🔍',
            'httpx': '🌐',
            'whatweb': '🔧',
            'gobuster': '📁',
            'nuclei': '🔬',
        }
        emoji = emoji_map.get(tool_name, '⚙️')
        
        self.console.print(f"\n[bold cyan]{emoji} [{step}/{total}] Starting {tool_name}...[/bold cyan]")
        if description:
            self.console.print(f"[dim]{description}[/dim]")
    
    def show_tool_progress(self, tool_name: str, current: int, total: Optional[int] = None, status: str = ""):
        """Show tool progress."""
        if not self.console or self.quiet:
            return
        
        if total:
            percentage = (current / total) * 100
            self.console.print(f"[yellow]  {tool_name}: {current}/{total} ({percentage:.1f}%)[/yellow] {status}", end="\r")
        else:
            self.console.print(f"[yellow]  {tool_name}: {current} items found...[/yellow] {status}", end="\r")
    
    def show_tool_complete(self, tool_name: str, results: Any, result_type: str = "items"):
        """Show tool completion message."""
        if not self.console or self.quiet:
            return
        
        count = len(results) if isinstance(results, (list, dict)) else results
        self.console.print(f"\n[bold green]✅ {tool_name} completed:[/bold green] [bold]{count} {result_type}[/bold]")
    
    def show_live_results(self, tool_name: str, results: List[Dict[str, Any]], max_display: int = 10):
        """Show live results table."""
        if not self.console or self.quiet or not results:
            return
        
        try:
            if tool_name == 'subfinder':
                table = Table(
                    title=f"🔍 Discovered Subdomains (showing {min(len(results), max_display)}/{len(results)})",
                    box=box.SIMPLE,
                    show_header=True
                )
                table.add_column("#", style="dim", width=4)
                table.add_column("Subdomain", style="cyan")
                
                for idx, item in enumerate(results[:max_display], 1):
                    subdomain = item.get('subdomain', str(item)) if isinstance(item, dict) else str(item)
                    table.add_row(str(idx), subdomain)
                
                if len(results) > max_display:
                    table.add_row("...", f"[dim]... and {len(results) - max_display} more[/dim]", style="dim")
                
                self.console.print(table)
            
            elif tool_name == 'httpx':
                table = Table(
                    title=f"🌐 Live Hosts (showing {min(len(results), max_display)}/{len(results)})",
                    box=box.SIMPLE,
                    show_header=True
                )
                table.add_column("#", style="dim", width=4)
                table.add_column("URL", style="green", overflow="fold")
                table.add_column("Status", style="yellow", width=6)
                table.add_column("Title", style="blue", overflow="fold")
                
                for idx, result in enumerate(results[:max_display], 1):
                    url = result.get('url', '')[:60]
                    status = str(result.get('status_code', ''))
                    title = result.get('title', '')[:40]
                    table.add_row(str(idx), url, status, title)
                
                if len(results) > max_display:
                    table.add_row("...", f"[dim]... and {len(results) - max_display} more[/dim]", "", "", style="dim")
                
                self.console.print(table)
            
            elif tool_name == 'nuclei':
                table = Table(
                    title=f"🔬 Vulnerabilities Found (showing {min(len(results), max_display)}/{len(results)})",
                    box=box.SIMPLE,
                    show_header=True
                )
                table.add_column("#", style="dim", width=4)
                table.add_column("Severity", style="red")
                table.add_column("Name", style="cyan", overflow="fold")
                table.add_column("URL", style="green", overflow="fold")
                
                for idx, result in enumerate(results[:max_display], 1):
                    severity = result.get('severity', 'info').upper()
                    name = result.get('name', 'Unknown')[:40]
                    url = result.get('url', '')[:50]
                    table.add_row(str(idx), severity, name, url)
                
                if len(results) > max_display:
                    table.add_row("...", f"[dim]... and {len(results) - max_display} more[/dim]", "", "", style="dim")
                
                self.console.print(table)
        
        except Exception as e:
            # Silently fail if there's an error displaying
            pass
    
    def monitor_file_and_show_results(
        self,
        tool_name: str,
        output_file: Path,
        parser_func,
        update_interval: float = 5.0,
        max_display: int = 10
    ):
        """Monitor file growth and show results as they come in."""
        if not self.console or self.quiet:
            return
        
        last_size = 0
        last_count = 0
        start_time = time.time()
        
        while True:
            try:
                if not output_file.exists():
                    time.sleep(1)
                    continue
                
                current_size = output_file.stat().st_size
                
                # If file is growing, parse and show results
                if current_size > last_size:
                    try:
                        content = output_file.read_text()
                        if content.strip():
                            parsed = parser_func(content)
                            current_count = len(parsed) if isinstance(parsed, list) else 0
                            
                            # Show progress
                            elapsed = int(time.time() - start_time)
                            self.show_tool_progress(
                                tool_name,
                                current_count,
                                None,
                                f"[dim]({elapsed}s elapsed)[/dim]"
                            )
                            
                            # Show results table every 10 seconds or when count changes significantly
                            if current_count > last_count and (current_count - last_count >= 5 or elapsed % 10 == 0):
                                self.show_live_results(tool_name, parsed, max_display)
                                last_count = current_count
                            
                            last_size = current_size
                    except Exception:
                        pass
                
                time.sleep(update_interval)
                
            except KeyboardInterrupt:
                break
            except Exception:
                time.sleep(update_interval)

