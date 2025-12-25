# ⚡ Quick Start - Reconner

## 🚀 Início Rápido em 3 Passos

### Passo 1: Navegar para o Diretório

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Executar Scan

```bash
python3 -m reconner --target example.com --output-dir ./results
```

**Pronto!** Os resultados estarão em `./results/`

---

## 📋 Comandos Mais Usados

```bash
# Scan básico
python3 -m reconner --target example.com --output-dir ./results

# Scan rápido
python3 -m reconner --target example.com --fast --output-dir ./results

# Com proxy
python3 -m reconner --target example.com --proxy http://127.0.0.1:8080 --output-dir ./results

# Múltiplos alvos
python3 -m reconner --input-file targets.txt --output-dir ./results
```

---

## 📁 Onde Estão os Resultados?

Após o scan, você encontrará:

- `results/summary.json` - Dados completos em JSON
- `results/report.md` - Relatório em Markdown
- `results/report.pdf` - Relatório em PDF
- `results/highlights.txt` - Resumo rápido
- `results/raw/` - Saídas brutas das ferramentas

---

## ❓ Problemas?

### "No such file or directory"
```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Tool not found"
Instale as ferramentas: subfinder, httpx, whatweb, gobuster, nuclei

---

## 📚 Mais Informações

- [README.md](README.md) - Documentação completa
- [COMANDOS.md](COMANDOS.md) - Todos os comandos
- [INSTALL.md](INSTALL.md) - Guia de instalação detalhado

---

**⚠️ Lembrete: Sempre obtenha autorização antes de escanear!**

