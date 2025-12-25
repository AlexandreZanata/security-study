"""Parsers for tool outputs."""

import json
import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_subfinder_json(content: str) -> List[str]:
    """Parse subfinder JSON output and extract subdomains."""
    subdomains = []
    try:
        # Try parsing as JSONL (one JSON per line)
        for line in content.strip().split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    host = data.get('host') or data.get('subdomain') or data.get('domain')
                    if host:
                        subdomains.append(host)
            except json.JSONDecodeError:
                continue
    except Exception as e:
        logger.debug(f"Failed to parse subfinder JSON: {e}")
    
    # Fallback to regex if JSON parsing fails
    if not subdomains:
        pattern = r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}'
        subdomains = re.findall(pattern, content)
        subdomains = [s[0] if isinstance(s, tuple) else s for s in subdomains]
    
    return list(set(subdomains))


def parse_httpx_json(content: str) -> List[Dict[str, Any]]:
    """Parse httpx JSON output."""
    results = []
    try:
        for line in content.strip().split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    results.append({
                        'url': data.get('url', ''),
                        'status_code': data.get('status_code', 0),
                        'title': data.get('title', ''),
                        'content_length': data.get('content_length', 0),
                        'server': data.get('server', ''),
                        'tech': data.get('tech', []),
                        'headers': data.get('headers', {}),
                        'host': data.get('host', ''),
                    })
            except json.JSONDecodeError:
                continue
    except Exception as e:
        logger.debug(f"Failed to parse httpx JSON: {e}")
    
    # Fallback to regex parsing
    if not results:
        url_pattern = r'https?://[^\s]+'
        status_pattern = r'\[(\d{3})\]'
        urls = re.findall(url_pattern, content)
        statuses = re.findall(status_pattern, content)
        
        for i, url in enumerate(urls):
            status = int(statuses[i]) if i < len(statuses) else 0
            results.append({
                'url': url,
                'status_code': status,
                'title': '',
                'content_length': 0,
                'server': '',
                'tech': [],
                'headers': {},
                'host': '',
            })
    
    return results


def parse_whatweb_json(content: str) -> List[Dict[str, Any]]:
    """Parse whatweb JSON output."""
    results = []
    try:
        # WhatWeb outputs JSON per target
        data = json.loads(content)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    results.append({
                        'url': item.get('target', ''),
                        'plugins': item.get('plugins', {}),
                        'http_status': item.get('http_status', 0),
                    })
        elif isinstance(data, dict):
            results.append({
                'url': data.get('target', ''),
                'plugins': data.get('plugins', {}),
                'http_status': data.get('http_status', 0),
            })
    except json.JSONDecodeError:
        # Try JSONL
        for line in content.strip().split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    results.append({
                        'url': data.get('target', ''),
                        'plugins': data.get('plugins', {}),
                        'http_status': data.get('http_status', 0),
                    })
            except json.JSONDecodeError:
                continue
    except Exception as e:
        logger.debug(f"Failed to parse whatweb JSON: {e}")
    
    return results


def parse_gobuster_output(content: str) -> List[Dict[str, Any]]:
    """Parse gobuster output (text or JSON)."""
    results = []
    
    # Try JSON first
    try:
        for line in content.strip().split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    results.append({
                        'path': data.get('Path', data.get('path', '')),
                        'status': data.get('Status', data.get('status', 0)),
                        'size': data.get('Size', data.get('size', 0)),
                        'url': data.get('URL', data.get('url', '')),
                    })
            except json.JSONDecodeError:
                continue
    except Exception:
        pass
    
    # Fallback to text parsing
    if not results:
        # Gobuster text format: /path (Status: 200) [Size: 1234]
        pattern = r'([/\w\-\.]+)\s+\(Status:\s+(\d+)\)\s+\[Size:\s+(\d+)\]'
        matches = re.findall(pattern, content)
        for match in matches:
            results.append({
                'path': match[0],
                'status': int(match[1]),
                'size': int(match[2]),
                'url': '',
            })
    
    return results


def parse_nuclei_json(content: str) -> List[Dict[str, Any]]:
    """Parse nuclei JSON/JSONL output."""
    results = []
    try:
        for line in content.strip().split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    results.append({
                        'template_id': data.get('template-id', data.get('template_id', '')),
                        'name': data.get('name', ''),
                        'severity': data.get('severity', 'info').lower(),
                        'matched_at': data.get('matched-at', data.get('matched_at', '')),
                        'url': data.get('url', ''),
                        'host': data.get('host', ''),
                        'info': data.get('info', {}),
                        'extracted_results': data.get('extracted-results', []),
                    })
            except json.JSONDecodeError:
                continue
    except Exception as e:
        logger.debug(f"Failed to parse nuclei JSON: {e}")
    
    return results


def parse_tool_output(tool_name: str, content: str, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Parse output from any tool."""
    if file_path:
        content = Path(file_path).read_text()
    
    parsers = {
        'subfinder': lambda c: [{'subdomain': s} for s in parse_subfinder_json(c)],
        'httpx': parse_httpx_json,
        'whatweb': parse_whatweb_json,
        'gobuster': parse_gobuster_output,
        'nuclei': parse_nuclei_json,
    }
    
    parser = parsers.get(tool_name)
    if parser:
        return parser(content)
    
    return []

