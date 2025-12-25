"""CLI interface for reconner."""

import sys
import click
import logging
from pathlib import Path
from typing import List

from .utils import (
    setup_logging, read_targets_file, normalize_url,
    ensure_output_dir, get_all_tool_versions, check_tool_exists,
    create_organized_output_dir
)
from .runner import ToolRunner
from .reporter import Reporter

# Legal warning
LEGAL_WARNING = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ⚠️  LEGAL WARNING  ⚠️                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  This tool is designed for AUTHORIZED security testing ONLY.                 ║
║                                                                              ║
║  ⚠️  ONLY execute against targets you own or have explicit written          ║
║      permission to test.                                                    ║
║                                                                              ║
║  ⚠️  Unauthorized scanning is ILLEGAL and may result in criminal charges.   ║
║                                                                              ║
║  ⚠️  You are RESPONSIBLE for ensuring you have proper authorization         ║
║      before running this tool.                                               ║
║                                                                              ║
║  ⚠️  The authors and contributors are NOT responsible for misuse.          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


@click.command()
@click.option(
    '--target',
    '-t',
    help='Single target to scan (e.g., https://example.com or example.com)',
    type=str,
)
@click.option(
    '--input-file',
    '-i',
    help='File containing targets (one per line)',
    type=click.Path(exists=True),
)
@click.option(
    '--output-dir',
    '-o',
    default='./results',
    help='Output directory for results (default: ./results)',
    type=click.Path(),
)
@click.option(
    '--wordlists-dir',
    '-w',
    default='/usr/share/seclists',
    help='Directory containing wordlists (default: /usr/share/seclists)',
    type=click.Path(),
)
@click.option(
    '--threads',
    default=20,
    help='Number of threads to use (default: 20)',
    type=int,
)
@click.option(
    '--proxy',
    help='Proxy URL (e.g., http://127.0.0.1:8080)',
    type=str,
)
@click.option(
    '--stealth',
    is_flag=True,
    help='Enable stealth mode (slower, less aggressive)',
)
@click.option(
    '--only-live',
    is_flag=True,
    help='Only process live hosts',
)
@click.option(
    '--skip-nuclei',
    is_flag=True,
    help='Skip nuclei vulnerability scanning',
)
@click.option(
    '--fast',
    is_flag=True,
    help='Fast mode (smaller wordlists, fewer nuclei templates)',
)
@click.option(
    '--export-only',
    is_flag=True,
    help='Only generate reports from existing results (no scanning)',
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Verbose output',
)
@click.option(
    '--quiet',
    '-q',
    is_flag=True,
    help='Quiet mode (minimal output)',
)
@click.version_option(version='1.0.0')
def main(
    target: str,
    input_file: str,
    output_dir: str,
    wordlists_dir: str,
    threads: int,
    proxy: str,
    stealth: bool,
    only_live: bool,
    skip_nuclei: bool,
    fast: bool,
    export_only: bool,
    verbose: bool,
    quiet: bool,
):
    """Reconner - Security reconnaissance tool orchestrator.
    
    Orchestrates multiple security tools (subfinder, httpx, whatweb, gobuster, nuclei)
    to perform comprehensive security reconnaissance.
    """
    # Display legal warning
    if not quiet:
        click.echo(click.style(LEGAL_WARNING, fg='red', bold=True))
        if not click.confirm('\nDo you have authorization to scan the target(s)?', default=False):
            click.echo(click.style('Scan cancelled. Exiting.', fg='yellow'))
            sys.exit(1)
        click.echo()
    
    # Setup logging
    log_file = None
    if output_dir:
        ensure_output_dir(output_dir)
        log_file = str(Path(output_dir) / 'reconner.log')
    setup_logging(verbose=verbose, quiet=quiet, log_file=log_file)
    
    logger = logging.getLogger(__name__)
    
    # Validate inputs
    if not target and not input_file and not export_only:
        click.echo(click.style('Error: --target or --input-file is required', fg='red'))
        sys.exit(1)
    
    if target and input_file:
        click.echo(click.style('Error: Use either --target or --input-file, not both', fg='red'))
        sys.exit(1)
    
    # Get targets
    targets: List[str] = []
    primary_target = None
    if target:
        normalized = normalize_url(target)
        targets.append(normalized)
        primary_target = normalized.replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]
    elif input_file:
        targets = read_targets_file(input_file)
        if targets:
            primary_target = targets[0].replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]
    
    if not targets and not export_only:
        click.echo(click.style('Error: No valid targets found', fg='red'))
        sys.exit(1)
    
    # Check tools
    if not export_only:
        logger.info("Checking for required tools...")
        missing_tools = []
        for tool_name in ['subfinder', 'httpx', 'whatweb', 'gobuster', 'nuclei']:
            exists, _ = check_tool_exists(tool_name)
            if not exists:
                missing_tools.append(tool_name)
        
        if missing_tools:
            logger.warning(f"Some tools not found: {', '.join(missing_tools)}")
            if not quiet:
                click.echo(click.style(
                    f'Warning: Some tools not found: {", ".join(missing_tools)}',
                    fg='yellow'
                ))
    
    # Create organized output directory
    if not export_only and primary_target:
        output_path = create_organized_output_dir(output_dir, primary_target)
        if not quiet:
            click.echo(f'📁 Results will be saved to: {output_path}')
    else:
        output_path = ensure_output_dir(output_dir)
    
    # Get tool versions
    tool_versions = get_all_tool_versions()
    
    if export_only:
        # Load existing results
        summary_file = output_path / 'summary.json'
        if not summary_file.exists():
            click.echo(click.style('Error: summary.json not found. Run a scan first.', fg='red'))
            sys.exit(1)
        
        import json
        with open(summary_file) as f:
            results = json.load(f)
        
        # Reconstruct results dict
        results_dict = {
            'subdomains': results.get('subdomains', {}).get('list', []),
            'live_hosts': results.get('live_hosts', {}).get('list', []),
            'httpx_results': results.get('httpx_results', []),
            'whatweb_results': results.get('whatweb_results', []),
            'gobuster_results': results.get('gobuster_results', []),
            'nuclei_results': results.get('nuclei_results', []),
            'errors': results.get('errors', []),
        }
        
        # Generate reports
        reporter = Reporter(str(output_path), tool_versions)
        reports = reporter.generate_all_reports(results_dict)
        
        if not quiet:
            click.echo(click.style('\n✅ Reports generated successfully!', fg='green'))
            for name, path in reports.items():
                click.echo(f'  - {name}: {path}')
        
        sys.exit(0)
    
    # Run scan
    if not quiet:
        click.echo(click.style(f'\n🚀 Starting reconnaissance scan...', fg='cyan', bold=True))
        click.echo(f'  Targets: {len(targets)}')
        click.echo(f'  Output: {output_dir}')
        click.echo(f'  Threads: {threads}')
        if proxy:
            click.echo(f'  Proxy: {proxy}')
        if stealth:
            click.echo('  Mode: Stealth')
        if fast:
            click.echo('  Mode: Fast')
        click.echo()
    
    runner = ToolRunner(
        output_dir=str(output_path),
        threads=threads,
        proxy=proxy,
        stealth=stealth,
        only_live=only_live,
        skip_nuclei=skip_nuclei,
        wordlists_dir=wordlists_dir,
        fast_mode=fast,
    )
    runner.quiet = quiet  # Set quiet mode
    
    try:
        results = runner.run_full_scan(targets)
    except KeyboardInterrupt:
        logger.warning("Scan interrupted by user")
        if not quiet:
            click.echo(click.style('\n⚠️  Scan interrupted', fg='yellow'))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        if not quiet:
            click.echo(click.style(f'\n❌ Scan failed: {e}', fg='red'))
        sys.exit(1)
    
    # Generate reports
    if not quiet:
        click.echo(click.style('\n📊 Generating reports...', fg='cyan'))
    
    # Extract primary target domain for reporter
    target_domain = primary_target if primary_target else "Unknown"
    reporter = Reporter(str(output_path), runner.tool_versions, target_domain=target_domain)
    reports = reporter.generate_all_reports(results)
    
    # Summary
    if not quiet:
        click.echo(click.style('\n✅ Scan completed successfully!', fg='green', bold=True))
        click.echo('\n📄 Generated Reports:')
        for name, path in reports.items():
            click.echo(f'  ✓ {name}: {path}')
        
        click.echo('\n📊 Summary:')
        click.echo(f'  - Subdomains: {len(results.get("subdomains", []))}')
        click.echo(f'  - Live Hosts: {len(results.get("live_hosts", []))}')
        click.echo(f'  - Vulnerabilities: {len(results.get("nuclei_results", []))}')
        click.echo(f'  - Paths Found: {len(results.get("gobuster_results", []))}')
        
        if results.get('errors'):
            click.echo(click.style(f'\n⚠️  Errors: {len(results["errors"])}', fg='yellow'))
    
    logger.info("Scan completed successfully")


if __name__ == '__main__':
    main()

