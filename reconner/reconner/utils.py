"""Utility functions for reconner."""

import os
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# Tool paths
TOOL_PATHS = {
    'httpx': '/usr/local/bin/httpx',
    'subfinder': '/usr/local/bin/subfinder',
    'nuclei': '/usr/local/bin/nuclei',
    'gobuster': '/usr/local/bin/gobuster',
    'whatweb': '/usr/local/bin/whatweb',
}

# Known JSON flags for each tool
TOOL_JSON_FLAGS = {
    'httpx': ['-json', '--json'],
    'subfinder': ['-json', '--json', '-oJ'],
    'nuclei': ['-json', '--json', '-jsonl'],
    'gobuster': ['-oJ', '--output-format', 'json'],
    'whatweb': ['--log-json'],
}

# Known version flags
TOOL_VERSION_FLAGS = {
    'httpx': ['-version', '--version'],
    'subfinder': ['-version', '--version'],
    'nuclei': ['-version', '--version'],
    'gobuster': ['-version', '--version'],
    'whatweb': ['--version'],
}


def check_tool_exists(tool_name: str) -> Tuple[bool, Optional[str]]:
    """Check if a tool exists and return its path."""
    if tool_name not in TOOL_PATHS:
        return False, None
    
    path = TOOL_PATHS[tool_name]
    if os.path.exists(path) and os.access(path, os.X_OK):
        return True, path
    
    # Try to find in PATH
    which_path = shutil.which(tool_name)
    if which_path:
        return True, which_path
    
    return False, None


def get_tool_version(tool_name: str) -> Optional[str]:
    """Get version of a tool by running --version."""
    exists, path = check_tool_exists(tool_name)
    if not exists or not path:
        return None
    
    version_flags = TOOL_VERSION_FLAGS.get(tool_name, ['--version'])
    
    for flag in version_flags:
        try:
            result = subprocess.run(
                [path, flag],
                capture_output=True,
                text=True,
                timeout=5,
                stderr=subprocess.STDOUT
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            logger.debug(f"Failed to get version for {tool_name} with {flag}: {e}")
            continue
    
    return None


def detect_json_support(tool_name: str) -> Optional[str]:
    """Detect if a tool supports JSON output and return the flag to use."""
    exists, path = check_tool_exists(tool_name)
    if not exists or not path:
        return None
    
    json_flags = TOOL_JSON_FLAGS.get(tool_name, [])
    
    # Try to check help output
    try:
        result = subprocess.run(
            [path, '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        help_text = result.stdout + result.stderr
        
        for flag in json_flags:
            if flag.lower() in help_text.lower():
                return flag
    except Exception as e:
        logger.debug(f"Could not check help for {tool_name}: {e}")
    
    # Return first known flag if any
    if json_flags:
        return json_flags[0]
    
    return None


def get_all_tool_versions() -> Dict[str, Optional[str]]:
    """Get versions of all tools."""
    versions = {}
    for tool in TOOL_PATHS.keys():
        versions[tool] = get_tool_version(tool)
    return versions


def ensure_output_dir(output_dir: str) -> Path:
    """Ensure output directory exists and create subdirectories."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / 'raw').mkdir(exist_ok=True)
    return output_path


def get_timestamp() -> str:
    """Get current timestamp in format YYYYMMDD-HHMMSS."""
    return datetime.now().strftime('%Y%m%d-%H%M%S')


def normalize_url(url: str) -> str:
    """Normalize URL by adding protocol if missing."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    return url


def read_targets_file(file_path: str) -> List[str]:
    """Read targets from a file, one per line."""
    targets = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                targets.append(normalize_url(line))
    return targets


def setup_logging(verbose: bool = False, quiet: bool = False, log_file: Optional[str] = None):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else (logging.ERROR if quiet else logging.INFO)
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

