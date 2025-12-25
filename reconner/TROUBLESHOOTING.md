# 🔧 Troubleshooting - Reconner

## ⏱️ O Scan Está Demorando - Isso é Normal!

### Por que demora?

O reconner executa **5 ferramentas em sequência**, e cada uma pode levar tempo:

1. **subfinder** - Descobre subdomínios (pode levar 1-5 minutos)
2. **httpx** - Verifica quais estão vivos (pode levar 2-10 minutos)
3. **whatweb** - Identifica tecnologias (pode levar 1-3 minutos)
4. **gobuster** - Enumera diretórios (pode levar 5-30 minutos por host)
5. **nuclei** - Scan de vulnerabilidades (pode levar 10-60 minutos)

**Tempo total estimado:** 20 minutos a 2 horas (dependendo do tamanho do alvo)

### Como Verificar se Está Funcionando

#### 1. Verificar Processos Ativos

```bash
# Ver quais ferramentas estão rodando
ps aux | grep -E "subfinder|httpx|whatweb|gobuster|nuclei" | grep -v grep
```

#### 2. Verificar Arquivos Sendo Criados

```bash
# Ver arquivos de saída sendo criados
ls -lh results/raw/

# Monitorar em tempo real
watch -n 2 'ls -lh results/raw/'
```

#### 3. Verificar Tamanho dos Arquivos

```bash
# Ver se os arquivos estão crescendo (significa que está funcionando)
du -sh results/raw/*
```

#### 4. Ver Logs

```bash
# Ver o log do reconner
tail -f results/reconner.log

# Ou se estiver usando verbose
python3 -m reconner --target example.com --verbose --output-dir ./results
```

## 🐛 Problemas Comuns

### Problema: "Nada acontece" / Scan parece travado

**Solução:**
1. Verifique se os processos estão rodando (comando acima)
2. O subfinder pode levar até 5 minutos para começar a mostrar resultados
3. Use `--verbose` para ver mais detalhes:
   ```bash
   python3 -m reconner --target example.com --verbose --output-dir ./results
   ```

### Problema: Timeout / Processo morre

**Solução:**
- Aumente o timeout no código (se necessário)
- Use `--stealth` para scans mais lentos e estáveis
- Reduza `--threads` para menos carga

### Problema: Ferramenta não encontrada

**Solução:**
```bash
# Verificar se está instalada
which subfinder
which httpx
which whatweb
which gobuster
which nuclei

# Se não estiver, instale ou adicione ao PATH
export PATH=$PATH:/usr/local/bin
```

### Problema: Wordlist não encontrada

**Solução:**
```bash
# Verificar se SecLists está instalado
ls /usr/share/seclists/Discovery/Web-Content/common.txt

# Ou especificar diretório customizado
python3 -m reconner --target example.com --wordlists-dir /path/to/wordlists --output-dir ./results
```

### Problema: Permissão negada

**Solução:**
```bash
# Dar permissão de execução
chmod +x /usr/local/bin/subfinder
chmod +x /usr/local/bin/httpx
chmod +x /usr/local/bin/whatweb
chmod +x /usr/local/bin/gobuster
chmod +x /usr/local/bin/nuclei
```

## 📊 Monitorar Progresso

### Modo Verbose (Recomendado)

```bash
python3 -m reconner --target example.com --verbose --output-dir ./results
```

Isso mostra:
- Quando cada ferramenta inicia
- Progresso em tempo real
- Erros detalhados
- Estatísticas

### Verificar Resultados Parciais

```bash
# Ver subdomínios encontrados até agora
cat results/raw/subfinder-*.json | jq .

# Ver hosts vivos encontrados
cat results/raw/httpx-*.json | jq '.url'

# Ver paths encontrados pelo gobuster
cat results/raw/gobuster-*.txt
```

### Interromper e Continuar Depois

Se você interromper o scan (Ctrl+C), os resultados parciais estarão em `results/raw/`.

Para gerar relatórios dos resultados parciais:
```bash
python3 -m reconner --export-only --output-dir ./results
```

## ⚡ Dicas para Scans Mais Rápidos

### 1. Usar Modo Fast

```bash
python3 -m reconner --target example.com --fast --output-dir ./results
```

Isso:
- Usa wordlists menores
- Executa menos templates do nuclei
- Pula alguns scans opcionais

### 2. Pular Ferramentas Lentas

```bash
# Pular nuclei (mais lento)
python3 -m reconner --target example.com --skip-nuclei --output-dir ./results

# Pular gobuster (pode ser muito lento)
# (Não há flag para isso, mas você pode editar o código)
```

### 3. Limitar Escopo

```bash
# Apenas hosts vivos
python3 -m reconner --target example.com --only-live --output-dir ./results
```

## 🔍 Verificar se Está Funcionando Agora

Execute estes comandos em outro terminal:

```bash
# 1. Ver processos
ps aux | grep -E "subfinder|httpx|whatweb|gobuster|nuclei" | grep -v grep

# 2. Ver arquivos
ls -lh ~/Pentest/projetos-seguraca/security-study/reconner/results/raw/

# 3. Ver tamanho dos arquivos (se estão crescendo)
du -sh ~/Pentest/projetos-seguraca/security-study/reconner/results/raw/*
```

## 📝 Exemplo de Saída Esperada

Quando está funcionando corretamente, você verá:

```
🚀 Starting Full Reconnaissance Scan
============================================================

🔍 [1/5] Running subfinder for example.com...
✅ [1/5] subfinder completed: Found 15 subdomains

🌐 [2/5] Running httpx for 15 targets...
✅ [2/5] httpx completed: Found 8 live hosts

🔧 [3/5] Running whatweb for 8 URLs...
✅ [3/5] whatweb completed: Processed 8 URLs

📁 [4/5] Running gobuster for 8 hosts...
✅ [4/5] gobuster completed: Found 45 total paths

🔬 [5/5] Running nuclei for 8 targets...
✅ [5/5] nuclei completed: Found 12 findings

============================================================
✅ Full Scan Completed!
============================================================
```

## ⏰ Tempos Estimados por Ferramenta

| Ferramenta | Tempo Estimado | Pode Variar |
|------------|---------------|-------------|
| subfinder  | 1-5 min       | Depende do tamanho do domínio |
| httpx      | 2-10 min      | Depende do número de subdomínios |
| whatweb    | 1-3 min       | Depende do número de hosts vivos |
| gobuster   | 5-30 min/host | Depende do tamanho da wordlist |
| nuclei     | 10-60 min     | Depende do número de templates |

**Total:** 20 minutos a 2+ horas

## 💡 Dica Final

**Se o scan parece travado, provavelmente está funcionando!** As ferramentas de segurança podem ser lentas. Use `--verbose` para ver o progresso em tempo real.

