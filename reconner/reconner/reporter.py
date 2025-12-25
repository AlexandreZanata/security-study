"""Report generation for reconner."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from jinja2 import Template

logger = logging.getLogger(__name__)


class Reporter:
    """Generates reports from scan results."""
    
    def __init__(self, output_dir: str, tool_versions: Dict[str, Any], target_domain: Optional[str] = None):
        self.output_dir = Path(output_dir)
        self.tool_versions = tool_versions
        self.summary_data = {}
        self.target_domain = target_domain or "Unknown"
    
    def generate_summary_json(self, results: Dict[str, Any]) -> Path:
        """Generate unified summary JSON."""
        summary = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'tool_versions': self.tool_versions,
            },
            'subdomains': {
                'total': len(results.get('subdomains', [])),
                'list': results.get('subdomains', []),
            },
            'live_hosts': {
                'total': len(results.get('live_hosts', [])),
                'list': results.get('live_hosts', []),
            },
            'httpx_results': results.get('httpx_results', []),
            'whatweb_results': results.get('whatweb_results', []),
            'gobuster_results': results.get('gobuster_results', []),
            'nuclei_results': results.get('nuclei_results', []),
            'errors': results.get('errors', []),
        }
        
        # Calculate statistics
        summary['statistics'] = {
            'total_subdomains': len(results.get('subdomains', [])),
            'total_live_hosts': len(results.get('live_hosts', [])),
            'total_technologies': len(self._extract_technologies(results)),
            'total_paths_found': len(results.get('gobuster_results', [])),
            'total_vulnerabilities': len(results.get('nuclei_results', [])),
            'critical_findings': len([r for r in results.get('nuclei_results', []) if r.get('severity') == 'critical']),
            'high_findings': len([r for r in results.get('nuclei_results', []) if r.get('severity') == 'high']),
            'medium_findings': len([r for r in results.get('nuclei_results', []) if r.get('severity') == 'medium']),
        }
        
        summary_path = self.output_dir / 'summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.summary_data = summary
        logger.info(f"Generated summary.json at {summary_path}")
        return summary_path
    
    def _extract_technologies(self, results: Dict[str, Any]) -> List[str]:
        """Extract unique technologies from results."""
        techs = set()
        
        # From httpx
        for r in results.get('httpx_results', []):
            techs.update(r.get('tech', []))
            if r.get('server'):
                techs.add(r['server'])
        
        # From whatweb
        for r in results.get('whatweb_results', []):
            plugins = r.get('plugins', {})
            if isinstance(plugins, dict):
                techs.update(plugins.keys())
        
        return sorted(list(techs))
    
    def generate_highlights(self, results: Dict[str, Any]) -> Path:
        """Generate highlights.txt with quick points."""
        highlights = []
        highlights.append("=" * 80)
        highlights.append("RECONNER SCAN HIGHLIGHTS")
        highlights.append("=" * 80)
        highlights.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        highlights.append("")
        
        # Statistics
        highlights.append("STATISTICS:")
        highlights.append(f"  - Subdomains found: {len(results.get('subdomains', []))}")
        highlights.append(f"  - Live hosts: {len(results.get('live_hosts', []))}")
        highlights.append(f"  - Paths discovered: {len(results.get('gobuster_results', []))}")
        highlights.append("")
        
        # Critical findings
        critical = [r for r in results.get('nuclei_results', []) if r.get('severity') == 'critical']
        if critical:
            highlights.append("CRITICAL FINDINGS:")
            for finding in critical[:10]:  # Top 10
                highlights.append(f"  - {finding.get('name', 'Unknown')} at {finding.get('url', 'N/A')}")
            highlights.append("")
        
        # High findings
        high = [r for r in results.get('nuclei_results', []) if r.get('severity') == 'high']
        if high:
            highlights.append("HIGH SEVERITY FINDINGS:")
            for finding in high[:10]:
                highlights.append(f"  - {finding.get('name', 'Unknown')} at {finding.get('url', 'N/A')}")
            highlights.append("")
        
        # Interesting paths
        interesting_paths = [
            r for r in results.get('gobuster_results', [])
            if any(keyword in r.get('path', '').lower() for keyword in ['admin', 'api', 'backup', 'config', 'test', 'dev'])
        ]
        if interesting_paths:
            highlights.append("INTERESTING PATHS DISCOVERED:")
            for path in interesting_paths[:15]:
                highlights.append(f"  - {path.get('path', 'N/A')} (Status: {path.get('status', 'N/A')})")
            highlights.append("")
        
        highlights.append("=" * 80)
        highlights.append("For detailed information, see summary.json and report.md")
        highlights.append("=" * 80)
        
        highlights_path = self.output_dir / 'highlights.txt'
        highlights_path.write_text('\n'.join(highlights))
        logger.info(f"Generated highlights.txt at {highlights_path}")
        return highlights_path
    
    def generate_markdown_report(self, results: Dict[str, Any]) -> Path:
        """Generate markdown report."""
        template_path = Path(__file__).parent / 'templates' / 'report.md.j2'
        
        if template_path.exists():
            template_content = template_path.read_text()
        else:
            # Fallback template
            template_content = self._get_default_template()
        
        template = Template(template_content)
        
        # Prepare data for template
        report_data = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tool_versions': self.tool_versions,
            'statistics': {
                'subdomains': len(results.get('subdomains', [])),
                'live_hosts': len(results.get('live_hosts', [])),
                'technologies': len(self._extract_technologies(results)),
                'paths': len(results.get('gobuster_results', [])),
                'vulnerabilities': len(results.get('nuclei_results', [])),
                'critical': len([r for r in results.get('nuclei_results', []) if r.get('severity') == 'critical']),
                'high': len([r for r in results.get('nuclei_results', []) if r.get('severity') == 'high']),
                'medium': len([r for r in results.get('nuclei_results', []) if r.get('severity') == 'medium']),
            },
            'subdomains': results.get('subdomains', [])[:50],  # Limit for report
            'live_hosts': results.get('live_hosts', [])[:50],
            'httpx_results': results.get('httpx_results', [])[:100],
            'whatweb_results': results.get('whatweb_results', []),
            'gobuster_results': sorted(
                results.get('gobuster_results', []),
                key=lambda x: x.get('status', 0),
                reverse=True
            )[:100],
            'nuclei_results': sorted(
                results.get('nuclei_results', []),
                key=lambda x: {'critical': 3, 'high': 2, 'medium': 1, 'low': 0, 'info': -1}.get(x.get('severity', 'info'), -1),
                reverse=True
            ),
            'technologies': sorted(self._extract_technologies(results)),
            'errors': results.get('errors', []),
        }
        
        markdown_content = template.render(**report_data)
        
        report_path = self.output_dir / 'report.md'
        report_path.write_text(markdown_content)
        logger.info(f"Generated report.md at {report_path}")
        return report_path
    
    def _get_default_template(self) -> str:
        """Get default markdown template."""
        return """# Reconnaissance Report

**Scan Date:** {{ scan_date }}

## Executive Summary

This report contains the results of an automated security reconnaissance scan.

### Statistics

- **Subdomains Discovered:** {{ statistics.subdomains }}
- **Live Hosts:** {{ statistics.live_hosts }}
- **Technologies Detected:** {{ statistics.technologies }}
- **Paths Discovered:** {{ statistics.paths }}
- **Vulnerabilities Found:** {{ statistics.vulnerabilities }}
  - Critical: {{ statistics.critical }}
  - High: {{ statistics.high }}
  - Medium: {{ statistics.medium }}

## Tool Versions

{% for tool, info in tool_versions.items() %}
- **{{ tool }}:** {{ info.version or 'Unknown' }}
{% endfor %}

## Live Hosts

{% for host in live_hosts %}
- {{ host }}
{% endfor %}

## Critical Findings

{% for finding in nuclei_results %}
{% if finding.severity == 'critical' %}
### {{ finding.name }}

- **URL:** {{ finding.url }}
- **Template ID:** {{ finding.template_id }}
- **Severity:** {{ finding.severity }}
- **Matched At:** {{ finding.matched_at }}

{% endif %}
{% endfor %}

## High Severity Findings

{% for finding in nuclei_results %}
{% if finding.severity == 'high' %}
### {{ finding.name }}

- **URL:** {{ finding.url }}
- **Template ID:** {{ finding.template_id }}
- **Severity:** {{ finding.severity }}

{% endif %}
{% endfor %}

## Interesting Paths

{% for path in gobuster_results[:50] %}
- `{{ path.path }}` - Status: {{ path.status }}, Size: {{ path.size }}
{% endfor %}

## Technologies Detected

{% for tech in technologies %}
- {{ tech }}
{% endfor %}

## Recommendations

1. Review all critical and high severity findings
2. Investigate exposed sensitive paths
3. Update outdated technologies
4. Implement proper access controls

## Legal Notice

This scan was performed for authorized security testing purposes only.
"""
    
    def convert_to_pdf(self, markdown_path: Path) -> Optional[Path]:
        """Convert markdown report to PDF."""
        pdf_path = self.output_dir / 'report.pdf'
        
        # Try weasyprint first
        try:
            from weasyprint import HTML, CSS
            from markdown import markdown
            
            md_content = markdown_path.read_text()
            html_content = markdown(md_content, extensions=['extra', 'codehilite'])
            
            HTML(string=html_content).write_pdf(pdf_path)
            logger.info(f"Generated report.pdf using weasyprint at {pdf_path}")
            return pdf_path
        except ImportError:
            logger.debug("weasyprint not available")
        except Exception as e:
            logger.debug(f"weasyprint failed: {e}")
        
        # Try pandoc
        try:
            import subprocess
            result = subprocess.run(
                ['pandoc', str(markdown_path), '-o', str(pdf_path)],
                capture_output=True,
                timeout=30,
            )
            if result.returncode == 0:
                logger.info(f"Generated report.pdf using pandoc at {pdf_path}")
                return pdf_path
        except FileNotFoundError:
            logger.debug("pandoc not available")
        except Exception as e:
            logger.debug(f"pandoc failed: {e}")
        
        # Fallback to reportlab with improved formatting
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
            from markdown import markdown
            from html import unescape
            import re
            
            md_content = markdown_path.read_text()
            
            # Create document with margins
            doc = SimpleDocTemplate(
                str(pdf_path),
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Define custom styles
            styles = getSampleStyleSheet()
            
            # Title style
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            # Heading styles
            h1_style = ParagraphStyle(
                'CustomH1',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold'
            )
            
            h2_style = ParagraphStyle(
                'CustomH2',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=10,
                spaceBefore=15,
                fontName='Helvetica-Bold'
            )
            
            # Normal text style
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=6,
                leading=14,
                alignment=TA_JUSTIFY
            )
            
            # Code style
            code_style = ParagraphStyle(
                'CustomCode',
                parent=styles['Code'],
                fontSize=9,
                textColor=colors.HexColor('#27ae60'),
                fontName='Courier',
                leftIndent=20,
                rightIndent=20,
                spaceAfter=8,
                backColor=colors.HexColor('#f5f5f5')
            )
            
            # List item style
            list_style = ParagraphStyle(
                'CustomList',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=4,
                leading=14,
                leftIndent=20,
                bulletIndent=10
            )
            
            def clean_html_tags(text):
                """Remove all HTML tags from text, but preserve content."""
                if not isinstance(text, str):
                    text = str(text)
                # Remove ALL HTML tags completely (including nested tags)
                # Use a more aggressive regex that handles multi-line tags
                # First, try to remove tags that span multiple lines
                text = re.sub(r'<[^>]*>', '', text, flags=re.DOTALL)
                # Also handle tags that might be split across lines
                text = re.sub(r'<[^>]*$', '', text, flags=re.MULTILINE)
                text = re.sub(r'^[^<]*>', '', text, flags=re.MULTILINE)
                # Decode HTML entities
                text = text.replace('&amp;', '&')
                text = text.replace('&lt;', '<')
                text = text.replace('&gt;', '>')
                text = text.replace('&quot;', '"')
                text = text.replace('&apos;', "'")
                text = text.replace('&nbsp;', ' ')
                # Remove any remaining HTML-like patterns
                text = re.sub(r'&[a-zA-Z]+;', '', text)
                # Clean up extra whitespace
                text = re.sub(r'\s+', ' ', text)
                return text.strip()
            
            def escape_xml(text):
                """Escape XML special characters for ReportLab, but preserve ReportLab tags."""
                if not isinstance(text, str):
                    text = str(text)
                # Don't escape ReportLab tags - they need to be processed
                # Only escape raw < and > that are not part of ReportLab tags
                # This is a simplified version - ReportLab will handle its own tags
                return text
            
            story = []
            
            # Parse markdown and create PDF elements
            lines = md_content.split('\n')
            i = 0
            in_code_block = False
            code_block_lines = []
            
            while i < len(lines):
                original_line = lines[i]
                line = original_line.strip()
                
                # Code block handling
                if line.startswith('```'):
                    if in_code_block:
                        # End of code block
                        if code_block_lines:
                            # Clean HTML and escape properly for code blocks
                            cleaned_lines = []
                            for c in code_block_lines:
                                cleaned = clean_html_tags(c)
                                cleaned = cleaned.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                                cleaned_lines.append(cleaned)
                            code_text = '<br/>'.join(cleaned_lines)
                            story.append(Paragraph(f"<font face='Courier' size='9' color='#27ae60'>{code_text}</font>", code_style))
                            story.append(Spacer(1, 8))
                        code_block_lines = []
                        in_code_block = False
                    else:
                        # Start of code block
                        in_code_block = True
                    i += 1
                    continue
                
                if in_code_block:
                    code_block_lines.append(original_line)
                    i += 1
                    continue
                
                if not line:
                    story.append(Spacer(1, 4))
                    i += 1
                    continue
                
                # Title (first #)
                if line.startswith('# ') and i < 5:
                    text = clean_html_tags(line[2:].strip())
                    # Escape ampersands
                    text = text.replace('&', '&amp;')
                    story.append(Paragraph(text, title_style))
                    story.append(Spacer(1, 20))
                
                # H1
                elif line.startswith('# '):
                    text = clean_html_tags(line[2:].strip())
                    text = text.replace('&', '&amp;')
                    story.append(Spacer(1, 10))
                    story.append(Paragraph(text, h1_style))
                    story.append(Spacer(1, 8))
                
                # H2
                elif line.startswith('## '):
                    text = clean_html_tags(line[3:].strip())
                    text = text.replace('&', '&amp;')
                    story.append(Spacer(1, 8))
                    story.append(Paragraph(text, h2_style))
                    story.append(Spacer(1, 6))
                
                # H3
                elif line.startswith('### '):
                    text = clean_html_tags(line[4:].strip())
                    text = text.replace('&', '&amp;')
                    story.append(Spacer(1, 6))
                    story.append(Paragraph(f"<b>{text}</b>", normal_style))
                    story.append(Spacer(1, 4))
                
                # H4
                elif line.startswith('#### '):
                    text = clean_html_tags(line[5:].strip())
                    text = text.replace('&', '&amp;')
                    story.append(Spacer(1, 4))
                    story.append(Paragraph(f"<b>{text}</b>", normal_style))
                    story.append(Spacer(1, 3))
                
                # Lists
                elif line.startswith('- ') or line.startswith('* '):
                    # Clean HTML FIRST
                    text = clean_html_tags(line[2:].strip())
                    # Process markdown formatting AFTER cleaning
                    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
                    # Handle inline code - use ReportLab font tags
                    text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="9" color="#27ae60">\1</font>', text)
                    # Escape ampersands that are not part of entities
                    text = re.sub(r'&(?![a-zA-Z]+;)', '&amp;', text)
                    story.append(Paragraph(f"• {text}", list_style))
                    story.append(Spacer(1, 2))
                
                # Numbered lists
                elif re.match(r'^\d+\.\s', line):
                    # Clean HTML FIRST
                    text = clean_html_tags(re.sub(r'^\d+\.\s', '', line))
                    # Process markdown formatting AFTER cleaning
                    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
                    text = re.sub(r'`([^`]+)`', r'<font face="Courier" size="9" color="#27ae60">\1</font>', text)
                    # Escape ampersands that are not part of entities
                    text = re.sub(r'&(?![a-zA-Z]+;)', '&amp;', text)
                    story.append(Paragraph(f"• {text}", list_style))
                    story.append(Spacer(1, 2))
                
                # Tables - skip
                elif '|' in line and i > 0 and '|' in lines[i-1].strip():
                    i += 1
                    continue
                
                # Horizontal rule
                elif line.startswith('---') or line.startswith('==='):
                    story.append(Spacer(1, 10))
                    story.append(Paragraph("_" * 70, normal_style))
                    story.append(Spacer(1, 10))
                
                # Regular text
                else:
                    # Clean HTML tags FIRST - remove ALL existing HTML
                    clean_line = clean_html_tags(line)
                    
                    # Process markdown formatting AFTER cleaning HTML
                    # Bold
                    clean_line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', clean_line)
                    # Italic
                    clean_line = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', clean_line)
                    # Inline code - use ReportLab font tags
                    clean_line = re.sub(r'`([^`]+)`', r'<font face="Courier" size="9" color="#27ae60">\1</font>', clean_line)
                    
                    # Escape ampersands that are not part of HTML entities or ReportLab tags
                    # But preserve ReportLab tags (<b>, <i>, <font>)
                    clean_line = re.sub(r'&(?![a-zA-Z]+;|lt;|gt;|amp;|quot;|apos;)', '&amp;', clean_line)
                    
                    if clean_line.strip():
                        story.append(Paragraph(clean_line, normal_style))
                        story.append(Spacer(1, 3))
                
                i += 1
            
            # Build PDF
            doc.build(story)
            logger.info(f"Generated report.pdf using reportlab at {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    def generate_all_reports(self, results: Dict[str, Any]) -> Dict[str, Path]:
        """Generate all reports."""
        logger.info("Generating all reports...")
        
        reports = {}
        
        # Summary JSON
        reports['summary'] = self.generate_summary_json(results)
        
        # Highlights
        reports['highlights'] = self.generate_highlights(results)
        
        # Markdown report
        reports['markdown'] = self.generate_markdown_report(results)
        
        # PDF report
        pdf = self.convert_to_pdf(reports['markdown'])
        if pdf:
            reports['pdf'] = pdf
        
        return reports

