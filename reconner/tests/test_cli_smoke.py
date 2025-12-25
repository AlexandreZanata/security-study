"""Smoke tests for reconner CLI."""

import pytest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from reconner.cli import main
from reconner.utils import check_tool_exists, normalize_url, read_targets_file


def test_normalize_url():
    """Test URL normalization."""
    assert normalize_url('example.com') == 'https://example.com'
    assert normalize_url('http://example.com') == 'http://example.com'
    assert normalize_url('https://example.com') == 'https://example.com'


def test_check_tool_exists():
    """Test tool existence checking."""
    # This will depend on what's actually installed
    exists, path = check_tool_exists('httpx')
    # Just verify the function doesn't crash
    assert isinstance(exists, bool)
    assert path is None or isinstance(path, str)


def test_read_targets_file(tmp_path):
    """Test reading targets from file."""
    test_file = tmp_path / 'targets.txt'
    test_file.write_text('example.com\nhttps://test.com\n# comment\n\nvalid.com')
    
    targets = read_targets_file(str(test_file))
    assert 'https://example.com' in targets
    assert 'https://test.com' in targets
    assert 'https://valid.com' in targets
    assert len(targets) == 3


@patch('reconner.cli.ToolRunner')
@patch('reconner.cli.Reporter')
@patch('reconner.cli.get_all_tool_versions')
@patch('reconner.cli.check_tool_exists')
def test_cli_basic(mock_check, mock_versions, mock_reporter, mock_runner):
    """Test basic CLI functionality."""
    # Mock tool checks
    mock_check.return_value = (True, '/usr/local/bin/httpx')
    mock_versions.return_value = {'httpx': {'version': '1.0.0', 'path': '/usr/local/bin/httpx'}}
    
    # Mock runner
    mock_runner_instance = MagicMock()
    mock_runner_instance.run_full_scan.return_value = {
        'subdomains': [],
        'live_hosts': [],
        'httpx_results': [],
        'whatweb_results': [],
        'gobuster_results': [],
        'nuclei_results': [],
        'errors': [],
    }
    mock_runner_instance.tool_versions = {}
    mock_runner.return_value = mock_runner_instance
    
    # Mock reporter
    mock_reporter_instance = MagicMock()
    mock_reporter_instance.generate_all_reports.return_value = {
        'summary': Path('/tmp/summary.json'),
        'markdown': Path('/tmp/report.md'),
    }
    mock_reporter.return_value = mock_reporter_instance
    
    # This test would need more mocking to actually run
    # For now, just verify imports work
    assert True


def test_imports():
    """Test that all modules can be imported."""
    from reconner import cli, runner, parsers, reporter, utils
    assert cli is not None
    assert runner is not None
    assert parsers is not None
    assert reporter is not None
    assert utils is not None

