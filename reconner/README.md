# 🔍 Reconner

**Reconner** is a comprehensive security reconnaissance tool orchestrator that automates and coordinates multiple security scanning tools to perform thorough security assessments.

**Reconner** é um orquestrador abrangente de ferramentas de reconhecimento de segurança que automatiza e coordena múltiplas ferramentas de varredura para realizar avaliações de segurança completas.

---

## ⚠️ Legal Warning / Aviso Legal

**ENGLISH:** This tool is designed for **AUTHORIZED security testing ONLY**. Only execute against targets you own or have explicit written permission to test. Unauthorized scanning is **ILLEGAL** and may result in criminal charges.

**PORTUGUÊS:** Esta ferramenta é projetada **APENAS para testes de segurança AUTORIZADOS**. Execute apenas contra alvos que você possui ou tem permissão escrita explícita para testar. Varredura não autorizada é **ILEGAL** e pode resultar em acusações criminais.

---

## 📋 Table of Contents / Índice

- [Quick Start / Início Rápido](#quick-start--início-rápido)
- [Installation / Instalação](#installation--instalação)
- [Required Tools / Ferramentas Necessárias](#required-tools--ferramentas-necessárias)
- [Global Installation / Instalação Global](#global-installation--instalação-global)
- [Usage / Uso](#usage--uso)
- [Output Files / Arquivos de Saída](#output-files--arquivos-de-saída)

---

## 🚀 Quick Start / Início Rápido

### English

1. **Install required tools** (see below)
2. **Install Python dependencies:**
   ```bash
   cd ~/Pentest/projetos-seguraca/security-study/reconner
   pip install -r requirements.txt
   ```
3. **Install globally:**
   ```bash
   pip install -e .
   ```
4. **Run a scan:**
   ```bash
   reconner --target example.com --output-dir ./results
   ```

### Português

1. **Instale as ferramentas necessárias** (veja abaixo)
2. **Instale dependências Python:**
   ```bash
   cd ~/Pentest/projetos-seguraca/security-study/reconner
   pip install -r requirements.txt
   ```
3. **Instale globalmente:**
   ```bash
   pip install -e .
   ```
4. **Execute um scan:**
   ```bash
   reconner --target example.com --output-dir ./results
   ```

---

## 📦 Installation / Instalação

### English

#### Step 1: Navigate to Project Directory

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

#### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 3: Install Required Security Tools

See [Required Tools](#required-tools--ferramentas-necessárias) section below.

### Português

#### Passo 1: Navegar para o Diretório do Projeto

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

#### Passo 2: Instalar Dependências Python

```bash
pip install -r requirements.txt
```

Ou use um ambiente virtual (recomendado):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Passo 3: Instalar Ferramentas de Segurança Necessárias

Veja a seção [Ferramentas Necessárias](#required-tools--ferramentas-necessárias) abaixo.

---

## 🛠️ Required Tools / Ferramentas Necessárias

### English

You must install these tools before using reconner. They should be accessible in your PATH or at `/usr/local/bin/`:

1. **subfinder** - Subdomain discovery
2. **httpx** - HTTP probing and live host detection
3. **whatweb** - Technology fingerprinting
4. **gobuster** - Directory and file brute-forcing
5. **nuclei** - Vulnerability scanning

### Installation Commands / Comandos de Instalação

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

### Português

Você deve instalar estas ferramentas antes de usar o reconner. Elas devem estar acessíveis no seu PATH ou em `/usr/local/bin/`:

1. **subfinder** - Descoberta de subdomínios
2. **httpx** - Verificação HTTP e detecção de hosts vivos
3. **whatweb** - Identificação de tecnologias
4. **gobuster** - Força bruta de diretórios e arquivos
5. **nuclei** - Varredura de vulnerabilidades

### Verificar Instalação / Check Installation

```bash
# English: Check if tools are installed
# Português: Verificar se as ferramentas estão instaladas

which subfinder
which httpx
which whatweb
which gobuster
which nuclei
```

---

## 🌐 Global Installation / Instalação Global

### English

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

### Português

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

## 🎯 Usage / Uso

### English

#### Basic Scan

```bash
reconner --target example.com --output-dir ./results
```

#### Fast Mode

```bash
reconner --target example.com --fast --output-dir ./results
```

#### With Proxy

```bash
reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results
```

#### Multiple Targets

```bash
# Create targets file
echo "example.com" > targets.txt
echo "test.example.com" >> targets.txt

# Run scan
reconner --input-file targets.txt --output-dir ./results
```

#### All Options

```bash
reconner --help
```

### Português

#### Scan Básico

```bash
reconner --target example.com --output-dir ./results
```

#### Modo Rápido

```bash
reconner --target example.com --fast --output-dir ./results
```

#### Com Proxy

```bash
reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results
```

#### Múltiplos Alvos

```bash
# Criar arquivo de alvos
echo "example.com" > targets.txt
echo "test.example.com" >> targets.txt

# Executar scan
reconner --input-file targets.txt --output-dir ./results
```

#### Todas as Opções

```bash
reconner --help
```

---

## 📊 Output Files / Arquivos de Saída

### English

After scanning, you'll find these files in the output directory:

- **`summary.json`** - Complete scan data in JSON format
- **`report.md`** - Detailed Markdown report
- **`report.pdf`** - PDF version of the report
- **`highlights.txt`** - Quick summary
- **`raw/`** - Raw outputs from each tool

### Português

Após o scan, você encontrará estes arquivos no diretório de saída:

- **`summary.json`** - Dados completos do scan em formato JSON
- **`report.md`** - Relatório detalhado em Markdown
- **`report.pdf`** - Versão PDF do relatório
- **`highlights.txt`** - Resumo rápido
- **`raw/`** - Saídas brutas de cada ferramenta

---

## 🔧 Command-Line Options / Opções de Linha de Comando

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--target` | `-t` | Single target to scan | Required* |
| `--input-file` | `-i` | File with targets (one per line) | Required* |
| `--output-dir` | `-o` | Output directory | `./results` |
| `--wordlists-dir` | `-w` | Wordlists directory | `/usr/share/seclists` |
| `--threads` | | Number of threads | `20` |
| `--proxy` | | Proxy URL | None |
| `--stealth` | | Stealth mode (slower) | False |
| `--only-live` | | Only process live hosts | False |
| `--skip-nuclei` | | Skip vulnerability scanning | False |
| `--fast` | | Fast mode | False |
| `--verbose` | `-v` | Verbose output | False |
| `--quiet` | `-q` | Quiet mode | False |

*Either `--target` or `--input-file` is required (unless using `--export-only`)

---

## ⏱️ Estimated Scan Times / Tempos Estimados de Scan

### English

| Tool | Estimated Time | Notes |
|------|---------------|-------|
| subfinder | 1-5 minutes | Depends on domain size |
| httpx | 2-10 minutes | Depends on number of subdomains |
| whatweb | 1-3 minutes | Depends on live hosts |
| gobuster | 5-30 min/host | Depends on wordlist size |
| nuclei | 10-60 minutes | Depends on templates |

**Total:** 20 minutes to 2+ hours

### Português

| Ferramenta | Tempo Estimado | Observações |
|------------|----------------|-------------|
| subfinder | 1-5 minutos | Depende do tamanho do domínio |
| httpx | 2-10 minutos | Depende do número de subdomínios |
| whatweb | 1-3 minutos | Depende dos hosts vivos |
| gobuster | 5-30 min/host | Depende do tamanho da wordlist |
| nuclei | 10-60 minutos | Depende dos templates |

**Total:** 20 minutos a 2+ horas

---

## 🐛 Troubleshooting / Solução de Problemas

### English

#### "Command not found"

```bash
# Install globally
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -e .
```

#### "Tool not found"

```bash
# Check if tools are installed
which subfinder httpx whatweb gobuster nuclei

# Install missing tools (see Required Tools section)
```

#### "Module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Português

#### "Comando não encontrado"

```bash
# Instalar globalmente
cd ~/Pentest/projetos-seguraca/security-study/reconner
pip install -e .
```

#### "Ferramenta não encontrada"

```bash
# Verificar se as ferramentas estão instaladas
which subfinder httpx whatweb gobuster nuclei

# Instalar ferramentas faltantes (veja seção Ferramentas Necessárias)
```

#### "Módulo não encontrado"

```bash
# Reinstalar dependências
pip install -r requirements.txt
```

---

## 📚 Additional Resources / Recursos Adicionais

### English

- **TROUBLESHOOTING.md** - Detailed troubleshooting guide
- **COMANDOS.md** - All commands and examples
- **INSTALACAO_GLOBAL.md** - Global installation guide

### Português

- **TROUBLESHOOTING.md** - Guia detalhado de solução de problemas
- **COMANDOS.md** - Todos os comandos e exemplos
- **INSTALACAO_GLOBAL.md** - Guia de instalação global

---

## 📄 License / Licença

MIT License - See [LICENSE](LICENSE) file

---

## ⚠️ Disclaimer / Aviso

**ENGLISH:** This tool is for authorized security testing only. The authors are not responsible for misuse.

**PORTUGUÊS:** Esta ferramenta é apenas para testes de segurança autorizados. Os autores não são responsáveis pelo uso indevido.

---

**Remember / Lembre-se: Always get authorization before scanning! / Sempre obtenha autorização antes de escanear!** 🛡️
