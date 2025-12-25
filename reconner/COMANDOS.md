# 🚀 Guia Rápido de Comandos - Reconner

## 📍 Navegação

```bash
# Ir para o diretório do projeto
cd ~/Pentest/projetos-seguraca/security-study/reconner

# Verificar se está no diretório correto
pwd
# Deve mostrar: /home/zanata/Pentest/projetos-seguraca/security-study/reconner

# Listar arquivos
ls -la
```

## 📦 Instalação

```bash
# 1. Navegar para o diretório
cd ~/Pentest/projetos-seguraca/security-study/reconner

# 2. Instalar dependências Python
pip install -r requirements.txt

# OU com pip3
pip3 install -r requirements.txt

# 3. Verificar instalação
python3 -m reconner --help
```

## 🎯 Comandos Básicos

### Ver Ajuda

```bash
python3 -m reconner --help
```

### Scan Básico (Um Alvo)

```bash
python3 -m reconner --target example.com --output-dir ./results
```

### Scan de Múltiplos Alvos (Arquivo)

```bash
# Criar arquivo com targets
echo "example.com" > targets.txt
echo "test.example.com" >> targets.txt

# Executar scan
python3 -m reconner --input-file targets.txt --output-dir ./results
```

## ⚡ Modos de Execução

### Modo Rápido (Fast)

```bash
python3 -m reconner --target example.com --fast --output-dir ./results
```

### Modo Stealth (Discreto)

```bash
python3 -m reconner --target example.com --stealth --threads 10 --output-dir ./results
```

### Com Proxy (Burp/ZAP)

```bash
python3 -m reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results
```

### Apenas Hosts Vivos

```bash
python3 -m reconner --target example.com --only-live --output-dir ./results
```

### Pular Nuclei (Sem Scan de Vulnerabilidades)

```bash
python3 -m reconner --target example.com --skip-nuclei --output-dir ./results
```

## 🔧 Opções Avançadas

### Customizar Threads

```bash
python3 -m reconner --target example.com --threads 50 --output-dir ./results
```

### Customizar Diretório de Wordlists

```bash
python3 -m reconner --target example.com --wordlists-dir /path/to/wordlists --output-dir ./results
```

### Modo Verbose (Mais Detalhes)

```bash
python3 -m reconner --target example.com --verbose --output-dir ./results
```

### Modo Quiet (Menos Output)

```bash
python3 -m reconner --target example.com --quiet --output-dir ./results
```

## 📊 Gerar Relatórios de Scan Existente

```bash
# Se você já tem resultados e quer apenas gerar relatórios
python3 -m reconner --export-only --output-dir ./results
```

## 🎨 Exemplos Completos

### Exemplo 1: Scan Completo Padrão

```bash
python3 -m reconner \
    --target example.com \
    --output-dir ./scan-results \
    --threads 30
```

### Exemplo 2: Scan Completo com Proxy

```bash
python3 -m reconner \
    --target example.com \
    --output-dir ./scan-results \
    --proxy http://127.0.0.1:8080 \
    --threads 20 \
    --verbose
```

### Exemplo 3: Scan Rápido e Discreto

```bash
python3 -m reconner \
    --target example.com \
    --output-dir ./scan-results \
    --fast \
    --stealth \
    --threads 5
```

### Exemplo 4: Scan Múltiplos Alvos

```bash
# Criar arquivo de targets
cat > targets.txt << EOF
example.com
test.example.com
dev.example.com
EOF

# Executar scan
python3 -m reconner \
    --input-file targets.txt \
    --output-dir ./scan-results \
    --threads 20
```

### Exemplo 5: Apenas Reconhecimento (Sem Nuclei)

```bash
python3 -m reconner \
    --target example.com \
    --output-dir ./scan-results \
    --skip-nuclei \
    --threads 30
```

## 📁 Verificar Resultados

```bash
# Ver estrutura de resultados
ls -la ./results/

# Ver resumo JSON
cat ./results/summary.json | jq .

# Ver highlights
cat ./results/highlights.txt

# Ver relatório Markdown
cat ./results/report.md

# Ver PDF (se gerado)
xdg-open ./results/report.pdf
```

## 🔍 Verificar Ferramentas Instaladas

```bash
# Verificar se as ferramentas estão no PATH
which subfinder
which httpx
which whatweb
which gobuster
which nuclei

# Verificar versões
subfinder -version
httpx -version
whatweb --version
gobuster version
nuclei -version
```

## 🐛 Solução de Problemas

### Erro: "No such file or directory"

```bash
# Verificar se está no diretório correto
cd ~/Pentest/projetos-seguraca/security-study/reconner
pwd
```

### Erro: "Module not found"

```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Tool not found"

```bash
# Verificar se as ferramentas estão instaladas
which subfinder httpx whatweb gobuster nuclei

# Se não estiverem, instale-as ou adicione ao PATH
export PATH=$PATH:/usr/local/bin
```

## 📝 Atalhos Úteis

### Criar Alias (Opcional)

Adicione ao `~/.bashrc`:

```bash
alias reconner='cd ~/Pentest/projetos-seguraca/security-study/reconner && python3 -m reconner'
```

Depois execute:
```bash
source ~/.bashrc
```

Agora você pode usar:
```bash
reconner --target example.com --output-dir ./results
```

## 🎯 Checklist Antes de Executar

- [ ] Estou no diretório correto: `~/Pentest/projetos-seguraca/security-study/reconner`
- [ ] Dependências instaladas: `pip install -r requirements.txt`
- [ ] Ferramentas instaladas: subfinder, httpx, whatweb, gobuster, nuclei
- [ ] Tenho autorização para scanear o alvo
- [ ] Diretório de saída especificado: `--output-dir ./results`

## ⚠️ Lembrete Importante

**SEMPRE obtenha autorização antes de escanear qualquer alvo!**

O reconner exibirá um aviso legal no início. Você precisa confirmar que tem autorização.

---

Para mais detalhes, consulte o [README.md](README.md) completo.

