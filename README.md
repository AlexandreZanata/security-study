# 🔍 Security Study - Reconner

**Quick Navigation:** [English](#english) | [Português](#português)

---

# English

## ⚠️ Legal Warning

**This tool is designed for AUTHORIZED security testing ONLY.** Only execute against targets you own or have explicit written permission to test. Unauthorized scanning is **ILLEGAL** and may result in criminal charges. You are responsible for ensuring you have proper authorization before running this tool.

---

## 📋 Table of Contents

- [What is Reconner?](#what-is-reconner)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Required Tools](#required-tools)
- [Global Installation](#global-installation)
- [Usage](#usage)
- [Command-Line Options](#command-line-options)
- [Output Files](#output-files)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## What is Reconner?

**Reconner** is a comprehensive security reconnaissance tool orchestrator that automates and coordinates multiple security scanning tools to perform thorough security assessments. It orchestrates tools like `subfinder`, `httpx`, `whatweb`, `gobuster`, and `nuclei` in a logical sequence to provide complete reconnaissance reports.

---

## Features

- ✅ **Automated Tool Orchestration** - Runs multiple security tools in the correct sequence
- ✅ **Subdomain Discovery** - Uses subfinder to discover subdomains
- ✅ **Live Host Detection** - Uses httpx to identify live hosts
- ✅ **Technology Fingerprinting** - Uses whatweb to identify technologies
- ✅ **Directory Enumeration** - Uses gobuster for directory/file brute-forcing
- ✅ **Vulnerability Scanning** - Uses nuclei for vulnerability detection
- ✅ **Comprehensive Reports** - Generates JSON, Markdown, PDF, and text reports
- ✅ **Progress Visualization** - Real-time progress bars and live data display
- ✅ **Organized Output** - Results organized by domain and timestamp
- ✅ **Parallel Execution** - Multi-threaded execution for faster scans

---

## Prerequisites

- Python 3.10 or higher
- Go (for installing security tools)
- Required security tools (see below)

---

## Installation

### Step 1: Navigate to Project Directory

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Install Globally (Optional but Recommended)

```bash
pip install -e .
```

This allows you to use `reconner` from any directory.

---

## Required Tools

You must install these tools before using reconner. They should be accessible in your PATH or at `/usr/local/bin/`:

1. **subfinder** - Subdomain discovery
2. **httpx** - HTTP probing and live host detection
3. **whatweb** - Technology fingerprinting
4. **gobuster** - Directory and file brute-forcing
5. **nuclei** - Vulnerability scanning

### Installation Commands

#### subfinder

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
sudo mv ~/go/bin/subfinder /usr/local/bin/
```

#### httpx

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
sudo mv ~/go/bin/httpx /usr/local/bin/
```

#### whatweb

```bash
# Debian/Ubuntu
sudo apt install whatweb

# Or from source
git clone https://github.com/urbanadventurer/WhatWeb.git
cd WhatWeb
sudo make install
```

#### gobuster

```bash
go install github.com/OJ/gobuster/v3@latest
sudo mv ~/go/bin/gobuster /usr/local/bin/
```

#### nuclei

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
sudo mv ~/go/bin/nuclei /usr/local/bin/
```

#### SecLists (Wordlists - Optional but Recommended)

```bash
# Debian/Ubuntu
sudo apt install seclists

# Or clone from GitHub
sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```

### Verify Installation

```bash
which subfinder
which httpx
which whatweb
which gobuster
which nuclei
```

---

## Global Installation

To use `reconner` from anywhere in your terminal (not just the project directory):

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -e .
```

**Verify installation:**

```bash
which reconner
reconner --version
```

**Test from different directories:**

```bash
cd ~
reconner --help

cd /tmp
reconner --version
```

Now you can use `reconner` from any directory!

---

## Usage

### Basic Scan

```bash
reconner --target example.com --output-dir ./results
```

### Fast Mode

```bash
reconner --target example.com --fast --output-dir ./results
```

### With Proxy

```bash
reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results
```

### Multiple Targets

```bash
# Create targets file
echo "example.com" > targets.txt
echo "test.example.com" >> targets.txt

# Run scan
reconner --input-file targets.txt --output-dir ./results
```

### Export Only (Regenerate Reports)

```bash
reconner --export-only --output-dir ./results
```

### All Options

```bash
reconner --help
```

---

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--target` | `-t` | Single target to scan | Required* |
| `--input-file` | `-i` | File with targets (one per line) | Required* |
| `--output-dir` | `-o` | Output directory | `./results` |
| `--wordlists-dir` | `-w` | Wordlists directory | `/usr/share/seclists` |
| `--threads` | | Number of threads | `20` |
| `--proxy` | | Proxy URL (e.g., http://127.0.0.1:8080) | None |
| `--stealth` | | Stealth mode (slower, less aggressive) | False |
| `--only-live` | | Only process live hosts | False |
| `--skip-nuclei` | | Skip nuclei vulnerability scanning | False |
| `--fast` | | Fast mode (smaller wordlists, fewer nuclei templates) | False |
| `--export-only` | | Only generate reports from existing results | False |
| `--verbose` | `-v` | Verbose output | False |
| `--quiet` | `-q` | Quiet mode (minimal output) | False |

*Either `--target` or `--input-file` is required (unless using `--export-only`)

---

## Output Files

After scanning, results are organized in a folder named after the domain and timestamp:

```
results/
└── example.com - 25_12_2025 - 7_30pm/
    ├── summary.json          # Complete scan data in JSON format
    ├── report.md             # Detailed Markdown report
    ├── report.pdf            # PDF version of the report (professional formatting)
    ├── highlights.txt        # Quick summary
    ├── discoveries.txt       # Key discoveries summary
    ├── reconner.log          # Execution log
    └── raw/                  # Raw outputs from each tool
        ├── subfinder-*.json
        ├── httpx-*.json
        ├── whatweb-*.json
        ├── gobuster-*.txt
        └── nuclei-*.json
```

### File Descriptions

- **`summary.json`** - Complete scan data in JSON format, including all subdomains, live hosts, technologies, paths, and vulnerabilities
- **`report.md`** - Detailed Markdown report with executive summary, statistics, findings, and recommendations
- **`report.pdf`** - Professional PDF version of the report with proper formatting
- **`highlights.txt`** - Quick summary with key statistics and critical findings
- **`discoveries.txt`** - Comprehensive summary of key discoveries, even if no vulnerabilities are found
- **`reconner.log`** - Detailed execution log with timestamps and tool versions
- **`raw/`** - Raw outputs from each tool for detailed analysis

---

## Examples

### Example 1: Basic Scan

```bash
reconner --target example.com --output-dir ./results
```

### Example 2: Fast Mode (Quick Test)

```bash
reconner --target example.com --fast --output-dir ./results
```

### Example 3: With Custom Wordlists

```bash
reconner --target example.com --wordlists-dir /path/to/wordlists --output-dir ./results
```

### Example 4: With Proxy

```bash
reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results
```

### Example 5: Multiple Targets

```bash
# Create targets file
cat > targets.txt << EOF
example.com
test.example.com
demo.example.com
EOF

# Run scan
reconner --input-file targets.txt --output-dir ./results
```

### Example 6: Stealth Mode

```bash
reconner --target example.com --stealth --output-dir ./results
```

### Example 7: Skip Vulnerability Scanning

```bash
reconner --target example.com --skip-nuclei --output-dir ./results
```

### Example 8: Only Live Hosts

```bash
reconner --target example.com --only-live --output-dir ./results
```

---

## Troubleshooting

### "Command not found"

```bash
# Install globally
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -e .
```

### "Tool not found"

```bash
# Check if tools are installed
which subfinder httpx whatweb gobuster nuclei

# Install missing tools (see Required Tools section)
```

### "Module not found"

```bash
# Reinstall dependencies
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -r requirements.txt
```

### "Permission denied"

```bash
# Make sure tools are in PATH or /usr/local/bin/
# Check permissions
ls -la /usr/local/bin/subfinder
ls -la /usr/local/bin/httpx
```

### Scan Taking Too Long

- Use `--fast` mode for quicker scans
- Use `--skip-nuclei` to skip vulnerability scanning
- Reduce `--threads` if system is overloaded
- Use `--only-live` to process only live hosts

---

## Estimated Scan Times

| Tool | Estimated Time | Notes |
|------|---------------|-------|
| subfinder | 1-5 minutes | Depends on domain size |
| httpx | 2-10 minutes | Depends on number of subdomains |
| whatweb | 1-3 minutes | Depends on live hosts |
| gobuster | 5-30 min/host | Depends on wordlist size |
| nuclei | 10-60 minutes | Depends on templates |

**Total:** 20 minutes to 2+ hours (depending on target size and options)

---

## License

MIT License - See [LICENSE](reconner/LICENSE) file

---

## Disclaimer

This tool is for authorized security testing only. The authors and contributors are not responsible for misuse. Always obtain proper authorization before scanning any target.

**Remember: Always get authorization before scanning!** 🛡️

---

# Português

## ⚠️ Aviso Legal

**Esta ferramenta é projetada APENAS para testes de segurança AUTORIZADOS.** Execute apenas contra alvos que você possui ou tem permissão escrita explícita para testar. Varredura não autorizada é **ILEGAL** e pode resultar em acusações criminais. Você é responsável por garantir que tem autorização adequada antes de executar esta ferramenta.

---

## 📋 Índice

- [O que é Reconner?](#o-que-é-reconner)
- [Recursos](#recursos)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação-1)
- [Ferramentas Necessárias](#ferramentas-necessárias)
- [Instalação Global](#instalação-global-1)
- [Uso](#uso)
- [Opções de Linha de Comando](#opções-de-linha-de-comando)
- [Arquivos de Saída](#arquivos-de-saída)
- [Exemplos](#exemplos-1)
- [Solução de Problemas](#solução-de-problemas)
- [Licença](#licença)

---

## O que é Reconner?

**Reconner** é um orquestrador abrangente de ferramentas de reconhecimento de segurança que automatiza e coordena múltiplas ferramentas de varredura para realizar avaliações de segurança completas. Ele orquestra ferramentas como `subfinder`, `httpx`, `whatweb`, `gobuster` e `nuclei` em uma sequência lógica para fornecer relatórios de reconhecimento completos.

---

## Recursos

- ✅ **Orquestração Automatizada de Ferramentas** - Executa múltiplas ferramentas de segurança na sequência correta
- ✅ **Descoberta de Subdomínios** - Usa subfinder para descobrir subdomínios
- ✅ **Detecção de Hosts Vivos** - Usa httpx para identificar hosts vivos
- ✅ **Identificação de Tecnologias** - Usa whatweb para identificar tecnologias
- ✅ **Enumeração de Diretórios** - Usa gobuster para força bruta de diretórios/arquivos
- ✅ **Varredura de Vulnerabilidades** - Usa nuclei para detecção de vulnerabilidades
- ✅ **Relatórios Abrangentes** - Gera relatórios em JSON, Markdown, PDF e texto
- ✅ **Visualização de Progresso** - Barras de progresso em tempo real e exibição de dados ao vivo
- ✅ **Saída Organizada** - Resultados organizados por domínio e timestamp
- ✅ **Execução Paralela** - Execução multi-thread para scans mais rápidos

---

## Pré-requisitos

- Python 3.10 ou superior
- Go (para instalar ferramentas de segurança)
- Ferramentas de segurança necessárias (veja abaixo)

---

## Instalação

### Passo 1: Navegar para o Diretório do Projeto

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

### Passo 2: Instalar Dependências Python

```bash
pip install -r requirements.txt
```

Ou use um ambiente virtual (recomendado):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Passo 3: Instalar Globalmente (Opcional mas Recomendado)

```bash
pip install -e .
```

Isso permite usar `reconner` de qualquer diretório.

---

## Ferramentas Necessárias

Você deve instalar estas ferramentas antes de usar o reconner. Elas devem estar acessíveis no seu PATH ou em `/usr/local/bin/`:

1. **subfinder** - Descoberta de subdomínios
2. **httpx** - Verificação HTTP e detecção de hosts vivos
3. **whatweb** - Identificação de tecnologias
4. **gobuster** - Força bruta de diretórios e arquivos
5. **nuclei** - Varredura de vulnerabilidades

### Comandos de Instalação

#### subfinder

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
sudo mv ~/go/bin/subfinder /usr/local/bin/
```

#### httpx

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
sudo mv ~/go/bin/httpx /usr/local/bin/
```

#### whatweb

```bash
# Debian/Ubuntu
sudo apt install whatweb

# Ou do código fonte
git clone https://github.com/urbanadventurer/WhatWeb.git
cd WhatWeb
sudo make install
```

#### gobuster

```bash
go install github.com/OJ/gobuster/v3@latest
sudo mv ~/go/bin/gobuster /usr/local/bin/
```

#### nuclei

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
sudo mv ~/go/bin/nuclei /usr/local/bin/
```

#### SecLists (Wordlists - Opcional mas Recomendado)

```bash
# Debian/Ubuntu
sudo apt install seclists

# Ou clone do GitHub
sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```

### Verificar Instalação

```bash
which subfinder
which httpx
which whatweb
which gobuster
which nuclei
```

---

## Instalação Global

Para usar `reconner` de qualquer lugar no seu terminal (não apenas no diretório do projeto):

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -e .
```

**Verificar instalação:**

```bash
which reconner
reconner --version
```

**Testar de diferentes diretórios:**

```bash
cd ~
reconner --help

cd /tmp
reconner --version
```

Agora você pode usar `reconner` de qualquer diretório!

---

## Uso

### Scan Básico

```bash
reconner --target example.com --output-dir ./results
```

### Modo Rápido

```bash
reconner --target example.com --fast --output-dir ./results
```

### Com Proxy

```bash
reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results
```

### Múltiplos Alvos

```bash
# Criar arquivo de alvos
echo "example.com" > targets.txt
echo "test.example.com" >> targets.txt

# Executar scan
reconner --input-file targets.txt --output-dir ./results
```

### Apenas Exportar (Regenerar Relatórios)

```bash
reconner --export-only --output-dir ./results
```

### Todas as Opções

```bash
reconner --help
```

---

## Opções de Linha de Comando

| Opção | Curta | Descrição | Padrão |
|-------|-------|-----------|--------|
| `--target` | `-t` | Alvo único para escanear | Obrigatório* |
| `--input-file` | `-i` | Arquivo com alvos (um por linha) | Obrigatório* |
| `--output-dir` | `-o` | Diretório de saída | `./results` |
| `--wordlists-dir` | `-w` | Diretório de wordlists | `/usr/share/seclists` |
| `--threads` | | Número de threads | `20` |
| `--proxy` | | URL do proxy (ex: http://127.0.0.1:8080) | Nenhum |
| `--stealth` | | Modo stealth (mais lento, menos agressivo) | False |
| `--only-live` | | Processar apenas hosts vivos | False |
| `--skip-nuclei` | | Pular varredura de vulnerabilidades do nuclei | False |
| `--fast` | | Modo rápido (wordlists menores, menos templates do nuclei) | False |
| `--export-only` | | Apenas gerar relatórios de resultados existentes | False |
| `--verbose` | `-v` | Saída verbosa | False |
| `--quiet` | `-q` | Modo silencioso (saída mínima) | False |

*Ou `--target` ou `--input-file` é obrigatório (a menos que use `--export-only`)

---

## Arquivos de Saída

Após o scan, os resultados são organizados em uma pasta nomeada após o domínio e timestamp:

```
results/
└── example.com - 25_12_2025 - 7_30pm/
    ├── summary.json          # Dados completos do scan em formato JSON
    ├── report.md             # Relatório detalhado em Markdown
    ├── report.pdf            # Versão PDF do relatório (formatação profissional)
    ├── highlights.txt        # Resumo rápido
    ├── discoveries.txt       # Resumo de descobertas principais
    ├── reconner.log          # Log de execução
    └── raw/                  # Saídas brutas de cada ferramenta
        ├── subfinder-*.json
        ├── httpx-*.json
        ├── whatweb-*.json
        ├── gobuster-*.txt
        └── nuclei-*.json
```

### Descrição dos Arquivos

- **`summary.json`** - Dados completos do scan em formato JSON, incluindo todos os subdomínios, hosts vivos, tecnologias, caminhos e vulnerabilidades
- **`report.md`** - Relatório detalhado em Markdown com resumo executivo, estatísticas, descobertas e recomendações
- **`report.pdf`** - Versão PDF profissional do relatório com formatação adequada
- **`highlights.txt`** - Resumo rápido com estatísticas principais e descobertas críticas
- **`discoveries.txt`** - Resumo abrangente de descobertas principais, mesmo que não haja vulnerabilidades
- **`reconner.log`** - Log detalhado de execução com timestamps e versões das ferramentas
- **`raw/`** - Saídas brutas de cada ferramenta para análise detalhada

---

## Exemplos

### Exemplo 1: Scan Básico

```bash
reconner --target example.com --output-dir ./results
```

### Exemplo 2: Modo Rápido (Teste Rápido)

```bash
reconner --target example.com --fast --output-dir ./results
```

### Exemplo 3: Com Wordlists Personalizadas

```bash
reconner --target example.com --wordlists-dir /caminho/para/wordlists --output-dir ./results
```

### Exemplo 4: Com Proxy

```bash
reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results
```

### Exemplo 5: Múltiplos Alvos

```bash
# Criar arquivo de alvos
cat > targets.txt << EOF
example.com
test.example.com
demo.example.com
EOF

# Executar scan
reconner --input-file targets.txt --output-dir ./results
```

### Exemplo 6: Modo Stealth

```bash
reconner --target example.com --stealth --output-dir ./results
```

### Exemplo 7: Pular Varredura de Vulnerabilidades

```bash
reconner --target example.com --skip-nuclei --output-dir ./results
```

### Exemplo 8: Apenas Hosts Vivos

```bash
reconner --target example.com --only-live --output-dir ./results
```

---

## Solução de Problemas

### "Comando não encontrado"

```bash
# Instalar globalmente
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -e .
```

### "Ferramenta não encontrada"

```bash
# Verificar se as ferramentas estão instaladas
which subfinder httpx whatweb gobuster nuclei

# Instalar ferramentas faltantes (veja seção Ferramentas Necessárias)
```

### "Módulo não encontrado"

```bash
# Reinstalar dependências
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -r requirements.txt
```

### "Permissão negada"

```bash
# Certifique-se de que as ferramentas estão no PATH ou /usr/local/bin/
# Verificar permissões
ls -la /usr/local/bin/subfinder
ls -la /usr/local/bin/httpx
```

### Scan Demorando Muito

- Use modo `--fast` para scans mais rápidos
- Use `--skip-nuclei` para pular varredura de vulnerabilidades
- Reduza `--threads` se o sistema estiver sobrecarregado
- Use `--only-live` para processar apenas hosts vivos

---

## Tempos Estimados de Scan

| Ferramenta | Tempo Estimado | Observações |
|------------|----------------|-------------|
| subfinder | 1-5 minutos | Depende do tamanho do domínio |
| httpx | 2-10 minutos | Depende do número de subdomínios |
| whatweb | 1-3 minutos | Depende dos hosts vivos |
| gobuster | 5-30 min/host | Depende do tamanho da wordlist |
| nuclei | 10-60 minutos | Depende dos templates |

**Total:** 20 minutos a 2+ horas (dependendo do tamanho do alvo e opções)

---

## Licença

MIT License - Veja arquivo [LICENSE](reconner/LICENSE)

---

## Aviso

Esta ferramenta é apenas para testes de segurança autorizados. Os autores e colaboradores não são responsáveis pelo uso indevido. Sempre obtenha autorização adequada antes de escanear qualquer alvo.

**Lembre-se: Sempre obtenha autorização antes de escanear!** 🛡️

