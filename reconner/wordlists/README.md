# Wordlists Directory

This directory is for storing custom wordlists used by reconner (specifically gobuster).

## Default Location

By default, reconner looks for wordlists in `/usr/share/seclists`. You can override this with the `--wordlists-dir` option.

## Recommended Wordlists

### For Directory Enumeration

Place wordlists in: `wordlists/Discovery/Web-Content/`

Recommended wordlists:
- `common.txt` - Common directories (small, fast)
- `directory-list-2.3-medium.txt` - Medium-sized list
- `directory-list-2.3-big.txt` - Large comprehensive list
- `raft-small-files.txt` - Sensitive files
- `raft-small-directories.txt` - Common directories

### For Subdomain Discovery

Place wordlists in: `wordlists/Discovery/DNS/`

Recommended wordlists:
- `subdomains-top1million-5000.txt` - Top 5000 subdomains
- `subdomains-top1million-110000.txt` - Comprehensive list

## Installing SecLists

To install SecLists (recommended):

```bash
# Debian/Ubuntu
sudo apt install seclists

# Or clone from GitHub
git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```

## Custom Wordlists

You can create custom wordlists and place them in this directory. When using `--wordlists-dir`, specify the path to this directory or your custom wordlist location.

## Usage Example

```bash
# Use default SecLists location
reconner --target example.com

# Use custom wordlist directory
reconner --target example.com --wordlists-dir ./wordlists
```

