"""Tool runner for executing security tools."""

import os
import subprocess
import logging
import json
import time
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskID
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .utils import (
    check_tool_exists, detect_json_support, get_tool_version,
    get_timestamp, normalize_url
)
from .parsers import parse_tool_output

logger = logging.getLogger(__name__)


class ToolRunner:
    """Orchestrates execution of security tools."""
    
    def __init__(
        self,
        output_dir: str,
        threads: int = 20,
        proxy: Optional[str] = None,
        stealth: bool = False,
        only_live: bool = False,
        skip_nuclei: bool = False,
        wordlists_dir: Optional[str] = None,
        fast_mode: bool = False,
    ):
        self.output_dir = Path(output_dir)
        self.raw_dir = self.output_dir / 'raw'
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.threads = threads
        self.proxy = proxy
        self.stealth = stealth
        self.only_live = only_live
        self.skip_nuclei = skip_nuclei
        self.wordlists_dir = wordlists_dir or '/usr/share/seclists'
        self.fast_mode = fast_mode
        self.quiet = False  # Will be set from CLI
        
        self.tool_versions = {}
        self.results = {
            'subdomains': [],
            'live_hosts': [],
            'httpx_results': [],
            'whatweb_results': [],
            'gobuster_results': [],
            'nuclei_results': [],
            'errors': [],
        }
        
        # Initialize progress manager
        try:
            from .progress import ProgressManager
            self.progress = ProgressManager(quiet=self.quiet)
        except ImportError:
            self.progress = None
        
        # Check and record tool versions
        self._check_tools()
    
    def _check_tools(self):
        """Check if all tools exist and record versions."""
        for tool_name in ['subfinder', 'httpx', 'whatweb', 'gobuster', 'nuclei']:
            exists, path = check_tool_exists(tool_name)
            if not exists:
                logger.warning(f"Tool {tool_name} not found at expected path")
                self.results['errors'].append({
                    'tool': tool_name,
                    'error': 'Tool not found',
                    'timestamp': datetime.now().isoformat(),
                })
            else:
                version = get_tool_version(tool_name)
                self.tool_versions[tool_name] = {
                    'path': path,
                    'version': version,
                }
                logger.info(f"Found {tool_name} at {path} (version: {version})")
    
    def _monitor_file_growth(self, file_path: Path, task_id: TaskID, last_size: int = 0):
        """Monitor file growth and update progress."""
        if not self.progress or not RICH_AVAILABLE:
            return
        
        try:
            current_size = file_path.stat().st_size if file_path.exists() else 0
            if current_size > last_size:
                # Estimate progress based on file growth (rough estimate)
                # We don't know total, so we'll use a spinner approach
                self.progress.update(task_id, advance=1)
                return current_size
        except Exception:
            pass
        return last_size
    
    def _show_live_results(self, tool_name: str, output_file: Path, max_display: int = 10):
        """Show live results as they come in."""
        if not self.console or not RICH_AVAILABLE or self.quiet:
            return
        
        try:
            if not output_file.exists():
                return
            
            content = output_file.read_text()
            if not content.strip():
                return
            
            # Parse and show partial results
            parsed = parse_tool_output(tool_name, content)
            
            if tool_name == 'subfinder':
                subdomains = [item.get('subdomain', '') for item in parsed if 'subdomain' in item]
                if subdomains:
                    table = Table(title=f"🔍 {tool_name} - Discovered Subdomains (showing {min(len(subdomains), max_display)})", box=box.SIMPLE)
                    table.add_column("Subdomain", style="cyan")
                    for subdomain in subdomains[:max_display]:
                        table.add_row(subdomain)
                    if len(subdomains) > max_display:
                        table.add_row(f"... and {len(subdomains) - max_display} more", style="dim")
                    self.console.print(table)
            
            elif tool_name == 'httpx':
                results = parsed[:max_display]
                if results:
                    table = Table(title=f"🌐 {tool_name} - Live Hosts (showing {min(len(parsed), max_display)})", box=box.SIMPLE)
                    table.add_column("URL", style="green")
                    table.add_column("Status", style="yellow")
                    table.add_column("Title", style="blue")
                    for r in results:
                        url = r.get('url', '')[:50]
                        status = str(r.get('status_code', ''))
                        title = r.get('title', '')[:30]
                        table.add_row(url, status, title)
                    if len(parsed) > max_display:
                        table.add_row(f"... and {len(parsed) - max_display} more", "", "", style="dim")
                    self.console.print(table)
        except Exception as e:
            logger.debug(f"Error showing live results: {e}")
    
    def run_subfinder(self, target: str) -> List[str]:
        """Run subfinder to discover subdomains."""
        logger.info(f"Running subfinder for {target}")
        
        exists, path = check_tool_exists('subfinder')
        if not exists:
            logger.error("subfinder not found")
            if self.progress:
                self.progress.console.print("[red]❌ subfinder not found![/red]")
            elif not self.quiet:
                print("❌ subfinder not found!", flush=True)
            return []
        
        json_flag = detect_json_support('subfinder')
        timestamp = get_timestamp()
        output_file = self.raw_dir / f'subfinder-{timestamp}.json'
        
        cmd = [path, '-d', target]
        if json_flag:
            cmd.append(json_flag)
        if self.proxy:
            cmd.extend(['-proxy', self.proxy])
        if self.stealth:
            cmd.extend(['-silent'])
        
        # Show start message
        if self.progress:
            self.progress.show_tool_start('subfinder', 1, 5, f"Discovering subdomains for {target}")
        
        # Start monitoring thread
        monitor_thread = None
        if self.progress and not self.quiet:
            def monitor():
                last_count = 0
                while True:
                    try:
                        if output_file.exists():
                            content = output_file.read_text()
                            if content.strip():
                                parsed = parse_tool_output('subfinder', content)
                                subdomains = [item.get('subdomain', '') for item in parsed if 'subdomain' in item]
                                current_count = len(subdomains)
                                
                                if current_count > last_count:
                                    self.progress.show_tool_progress('subfinder', current_count, None, "subdomains found")
                                    if current_count - last_count >= 10:  # Show table every 10 new subdomains
                                        self.progress.show_live_results('subfinder', [{'subdomain': s} for s in subdomains[:20]])
                                    last_count = current_count
                        time.sleep(3)
                    except (KeyboardInterrupt, Exception):
                        break
            
            monitor_thread = threading.Thread(target=monitor, daemon=True)
            monitor_thread.start()
        
        try:
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300,
                )
            
            # Wait a bit for monitor to catch up
            if monitor_thread:
                time.sleep(2)
            
            if result.returncode != 0:
                logger.warning(f"subfinder returned non-zero: {result.stderr}")
            
            # Parse output
            content = output_file.read_text()
            parsed = parse_tool_output('subfinder', content)
            subdomains = [item['subdomain'] for item in parsed if 'subdomain' in item]
            
            # Add original target
            subdomains.append(target)
            subdomains = list(set(subdomains))
            
            self.results['subdomains'] = subdomains
            logger.info(f"Found {len(subdomains)} subdomains")
            
            # Show completion
            if self.progress:
                self.progress.show_tool_complete('subfinder', subdomains, "subdomains")
                self.progress.show_live_results('subfinder', [{'subdomain': s} for s in subdomains[:20]])
            elif not self.quiet:
                print(f"✅ [1/5] subfinder completed: Found {len(subdomains)} subdomains", flush=True)
            
            return subdomains
            
        except subprocess.TimeoutExpired:
            logger.error("subfinder timed out")
            if self.progress:
                self.progress.console.print("[red]⏱️  subfinder timed out[/red]")
            elif not self.quiet:
                print("⏱️  subfinder timed out", flush=True)
            self.results['errors'].append({
                'tool': 'subfinder',
                'error': 'Timeout',
                'timestamp': datetime.now().isoformat(),
            })
            return []
        except Exception as e:
            logger.error(f"subfinder failed: {e}")
            if self.progress:
                self.progress.console.print(f"[red]❌ subfinder failed: {e}[/red]")
            elif not self.quiet:
                print(f"❌ subfinder failed: {e}", flush=True)
            self.results['errors'].append({
                'tool': 'subfinder',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            })
            return []
    
    def run_httpx(self, targets: List[str]) -> List[Dict[str, Any]]:
        """Run httpx to check live hosts."""
        logger.info(f"Running httpx for {len(targets)} targets")
        
        if self.progress:
            self.progress.show_tool_start('httpx', 2, 5, f"Checking {len(targets)} targets for live hosts")
        elif not self.quiet:
            print(f"🌐 [2/5] Running httpx for {len(targets)} targets...", flush=True)
        
        exists, path = check_tool_exists('httpx')
        if not exists:
            logger.error("httpx not found")
            if self.progress:
                self.progress.console.print("[red]❌ httpx not found![/red]")
            return []
        
        json_flag = detect_json_support('httpx')
        timestamp = get_timestamp()
        output_file = self.raw_dir / f'httpx-{timestamp}.json'
        
        # Write targets to temp file
        temp_file = self.raw_dir / f'httpx-targets-{timestamp}.txt'
        temp_file.write_text('\n'.join(targets))
        
        cmd = [path, '-l', str(temp_file)]
        if json_flag:
            cmd.append(json_flag)
        cmd.extend(['-title', '-status-code', '-tech-detect', '-content-length'])
        if self.proxy:
            cmd.extend(['-proxy', self.proxy])
        if self.stealth:
            cmd.extend(['-silent', '-rate-limit', '10'])
        
        try:
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=600,
                )
            
            if result.returncode != 0:
                logger.warning(f"httpx returned non-zero: {result.stderr}")
            
            # Parse output
            content = output_file.read_text()
            parsed = parse_tool_output('httpx', content)
            
            # Filter live hosts if requested
            if self.only_live:
                parsed = [r for r in parsed if r.get('status_code', 0) in [200, 201, 202, 204, 301, 302, 307, 308]]
            
            self.results['httpx_results'] = parsed
            self.results['live_hosts'] = [r['url'] for r in parsed]
            logger.info(f"Found {len(parsed)} live hosts")
            
            if self.progress:
                self.progress.show_tool_complete('httpx', parsed, "live hosts")
                self.progress.show_live_results('httpx', parsed[:20])
            elif not self.quiet:
                print(f"✅ [2/5] httpx completed: Found {len(parsed)} live hosts", flush=True)
            
            return parsed
            
        except subprocess.TimeoutExpired:
            logger.error("httpx timed out")
            self.results['errors'].append({
                'tool': 'httpx',
                'error': 'Timeout',
                'timestamp': datetime.now().isoformat(),
            })
            return []
        except Exception as e:
            logger.error(f"httpx failed: {e}")
            self.results['errors'].append({
                'tool': 'httpx',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            })
            return []
    
    def run_whatweb(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Run whatweb for technology fingerprinting."""
        if not urls:
            return []
        
        logger.info(f"Running whatweb for {len(urls)} URLs")
        
        if self.progress:
            self.progress.show_tool_start('whatweb', 3, 5, f"Fingerprinting technologies on {len(urls)} URLs")
        elif not self.quiet:
            print(f"🔧 [3/5] Running whatweb for {len(urls)} URLs...", flush=True)
        
        exists, path = check_tool_exists('whatweb')
        if not exists:
            logger.warning("whatweb not found, skipping")
            return []
        
        json_flag = detect_json_support('whatweb')
        timestamp = get_timestamp()
        output_file = self.raw_dir / f'whatweb-{timestamp}.json'
        
        cmd = [path]
        if json_flag:
            cmd.append(json_flag)
        if self.proxy:
            cmd.extend(['--proxy', self.proxy])
        cmd.extend(urls[:50])  # Limit to 50 URLs at a time
        
        try:
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300,
                )
            
            # Parse output
            content = output_file.read_text()
            parsed = parse_tool_output('whatweb', content)
            self.results['whatweb_results'] = parsed
            logger.info(f"whatweb processed {len(parsed)} URLs")
            
            if self.progress:
                self.progress.show_tool_complete('whatweb', parsed, "URLs processed")
            elif not self.quiet:
                print(f"✅ [3/5] whatweb completed: Processed {len(parsed)} URLs", flush=True)
            
            return parsed
            
        except Exception as e:
            logger.error(f"whatweb failed: {e}")
            self.results['errors'].append({
                'tool': 'whatweb',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            })
            return []
    
    def run_gobuster(self, url: str, wordlist: str = 'common.txt') -> List[Dict[str, Any]]:
        """Run gobuster for directory brute-forcing."""
        logger.info(f"Running gobuster for {url}")
        print(f"📁 Running gobuster for {url}...", flush=True)
        exists, path = check_tool_exists('gobuster')
        if not exists:
            logger.warning("gobuster not found, skipping")
            return []
        
        # Determine wordlist path
        wordlist_path = Path(self.wordlists_dir) / 'Discovery' / 'Web-Content' / wordlist
        if not wordlist_path.exists():
            # Try alternative locations
            alt_paths = [
                Path('/usr/share/wordlists') / wordlist,
                Path(self.wordlists_dir) / wordlist,
            ]
            for alt in alt_paths:
                if alt.exists():
                    wordlist_path = alt
                    break
            else:
                logger.warning(f"Wordlist {wordlist} not found, skipping gobuster")
                return []
        
        timestamp = get_timestamp()
        host_safe = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        output_file = self.raw_dir / f'gobuster-{host_safe}-{timestamp}.txt'
        
        cmd = [path, 'dir', '-u', url, '-w', str(wordlist_path)]
        cmd.extend(['-t', str(min(self.threads, 50))])
        
        if self.fast_mode:
            cmd.extend(['-x', 'php,html,txt'])
        else:
            cmd.extend(['-x', 'php,html,txt,js,bak,old,zip,tar.gz,sql'])
        
        if self.proxy:
            cmd.extend(['--proxy', self.proxy])
        if self.stealth:
            cmd.extend(['-t', '5', '-r', '-k'])
        
        try:
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=600,
                )
            
            # Parse output
            content = output_file.read_text()
            parsed = parse_tool_output('gobuster', content)
            logger.info(f"gobuster found {len(parsed)} paths for {url}")
            print(f"✅ gobuster completed for {url}: Found {len(parsed)} paths", flush=True)
            return parsed
            
        except subprocess.TimeoutExpired:
            logger.warning(f"gobuster timed out for {url}")
            return []
        except Exception as e:
            logger.error(f"gobuster failed for {url}: {e}")
            return []
    
    def run_gobuster_parallel(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Run gobuster in parallel for multiple URLs."""
        if not urls:
            return []
        
        print(f"📁 [4/5] Running gobuster for {len(urls)} hosts...", flush=True)
        wordlist = 'common.txt' if self.fast_mode else 'directory-list-2.3-medium.txt'
        all_results = []
        
        with ThreadPoolExecutor(max_workers=min(self.threads, 5)) as executor:
            futures = {executor.submit(self.run_gobuster, url, wordlist): url for url in urls}
            
            for future in as_completed(futures):
                url = futures[future]
                try:
                    results = future.result()
                    for r in results:
                        r['target_url'] = url
                    all_results.extend(results)
                except Exception as e:
                    logger.error(f"gobuster future failed for {url}: {e}")
        
        self.results['gobuster_results'] = all_results
        print(f"✅ [4/5] gobuster completed: Found {len(all_results)} total paths", flush=True)
        return all_results
    
    def run_nuclei(self, targets: List[str]) -> List[Dict[str, Any]]:
        """Run nuclei for vulnerability scanning."""
        if self.skip_nuclei:
            logger.info("Skipping nuclei as requested")
            if self.progress:
                self.progress.console.print("[yellow]⏭️  [5/5] Skipping nuclei (--skip-nuclei)[/yellow]")
            elif not self.quiet:
                print("⏭️  [5/5] Skipping nuclei (--skip-nuclei)", flush=True)
            return []
        
        logger.info(f"Running nuclei for {len(targets)} targets")
        
        if self.progress:
            self.progress.show_tool_start('nuclei', 5, 5, f"Scanning {len(targets)} targets for vulnerabilities")
        elif not self.quiet:
            print(f"🔬 [5/5] Running nuclei for {len(targets)} targets...", flush=True)
        
        exists, path = check_tool_exists('nuclei')
        if not exists:
            logger.warning("nuclei not found, skipping")
            return []
        
        json_flag = detect_json_support('nuclei')
        timestamp = get_timestamp()
        output_file = self.raw_dir / f'nuclei-{timestamp}.json'
        
        # Write targets to temp file
        temp_file = self.raw_dir / f'nuclei-targets-{timestamp}.txt'
        temp_file.write_text('\n'.join(targets))
        
        cmd = [path, '-l', str(temp_file)]
        if json_flag:
            cmd.append(json_flag)
        
        if self.fast_mode:
            cmd.extend(['-severity', 'critical,high'])
        else:
            cmd.extend(['-severity', 'critical,high,medium'])
        
        if self.proxy:
            cmd.extend(['-proxy', self.proxy])
        if self.stealth:
            cmd.extend(['-rate-limit', '10'])
        
        cmd.extend(['-t', str(self.threads)])
        
        try:
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=1800,  # 30 minutes
                )
            
            # Parse output
            content = output_file.read_text()
            parsed = parse_tool_output('nuclei', content)
            self.results['nuclei_results'] = parsed
            logger.info(f"nuclei found {len(parsed)} findings")
            
            if self.progress:
                self.progress.show_tool_complete('nuclei', parsed, "findings")
                if parsed:
                    self.progress.show_live_results('nuclei', parsed[:20])
            elif not self.quiet:
                print(f"✅ [5/5] nuclei completed: Found {len(parsed)} findings", flush=True)
            
            return parsed
            
        except subprocess.TimeoutExpired:
            logger.warning("nuclei timed out")
            self.results['errors'].append({
                'tool': 'nuclei',
                'error': 'Timeout',
                'timestamp': datetime.now().isoformat(),
            })
            return []
        except Exception as e:
            logger.error(f"nuclei failed: {e}")
            self.results['errors'].append({
                'tool': 'nuclei',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            })
            return []
    
    def run_full_scan(self, targets: List[str]) -> Dict[str, Any]:
        """Run full reconnaissance scan."""
        logger.info("Starting full reconnaissance scan")
        
        if self.progress and not self.quiet:
            self.progress.console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
            self.progress.console.print("[bold cyan]🚀 Starting Full Reconnaissance Scan[/bold cyan]")
            self.progress.console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
        elif not self.quiet:
            print("\n" + "="*60, flush=True)
            print("🚀 Starting Full Reconnaissance Scan", flush=True)
            print("="*60 + "\n", flush=True)
        
        # Step 1: Subdomain discovery
        all_targets = set()
        for target in targets:
            subdomains = self.run_subfinder(target.replace('https://', '').replace('http://', '').split('/')[0])
            all_targets.update(subdomains)
        
        # Normalize targets
        normalized_targets = [normalize_url(t) for t in all_targets]
        
        # Step 2: Check live hosts
        httpx_results = self.run_httpx(normalized_targets)
        live_urls = [r['url'] for r in httpx_results]
        
        if not live_urls:
            logger.warning("No live hosts found")
            return self.results
        
        # Step 3: Technology fingerprinting
        self.run_whatweb(live_urls[:50])  # Limit to 50
        
        # Step 4: Directory brute-forcing
        if not self.fast_mode:
            self.run_gobuster_parallel(live_urls[:10])  # Limit to 10 hosts
        else:
            print("⏭️  [4/5] Skipping gobuster (fast mode)", flush=True)
        
        # Step 5: Vulnerability scanning
        self.run_nuclei(live_urls)
        
        logger.info("Full scan completed")
        
        if self.progress and not self.quiet:
            self.progress.console.print("\n[bold green]" + "="*60 + "[/bold green]")
            self.progress.console.print("[bold green]✅ Full Scan Completed![/bold green]")
            self.progress.console.print("[bold green]" + "="*60 + "[/bold green]\n")
        elif not self.quiet:
            print("\n" + "="*60, flush=True)
            print("✅ Full Scan Completed!", flush=True)
            print("="*60 + "\n", flush=True)
        
        return self.results

