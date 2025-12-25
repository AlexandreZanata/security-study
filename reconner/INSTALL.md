# 📦 Guia de Instalação - Reconner

## Passo a Passo Completo

### 1. Navegar para o Diretório Correto

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

Ou se você estiver em outro diretório:

```bash
cd /home/zanata/Pentest/projetos-seguraca/security-study/reconner
```

**Verificar se está no diretório correto:**
```bash
pwd
# Deve mostrar: /home/zanata/Pentest/projetos-seguraca/security-study/reconner

ls -la requirements.txt
# Deve mostrar o arquivo requirements.txt
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Você verá (venv) no início do prompt
```

### 3. Instalar Dependências Python

```bash
# Com ambiente virtual ativado
pip install -r requirements.txt

# OU sem ambiente virtual (instalação global)
pip3 install -r requirements.txt
```

**Dependências instaladas:**
- click
- jinja2
- reportlab
- markdown
- rich

### 4. Verificar Instalação

```bash
python3 -m reconner --help
```

Se funcionar, você verá a mensagem de ajuda do reconner.

### 5. (Opcional) Instalar como Pacote

```bash
pip install -e .
```

Isso permite executar `reconner` de qualquer lugar.

## Instalação das Ferramentas de Segurança

### Verificar se as Ferramentas Estão Instaladas

```bash
which subfinder
which httpx
which whatweb
which gobuster
which nuclei
```

### Instalar Ferramentas (se necessário)

#### Subfinder
```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
sudo mv ~/go/bin/subfinder /usr/local/bin/
```

#### HTTPx
```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
sudo mv ~/go/bin/httpx /usr/local/bin/
```

#### WhatWeb
```bash
sudo apt install whatweb
# ou
git clone https://github.com/urbanadventurer/WhatWeb.git
cd WhatWeb
sudo make install
```

#### Gobuster
```bash
go install github.com/OJ/gobuster/v3@latest
sudo mv ~/go/bin/gobuster /usr/local/bin/
```

#### Nuclei
```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
sudo mv ~/go/bin/nuclei /usr/local/bin/
```

### Instalar SecLists (Wordlists)

```bash
# Debian/Ubuntu
sudo apt install seclists

# Ou clonar do GitHub
sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```

## Teste Rápido

```bash
# Verificar se tudo está funcionando
python3 -m reconner --help

# Teste básico (substitua example.com por um alvo autorizado)
python3 -m reconner --target example.com --output-dir ./test-results
```

## Solução de Problemas

### Erro: "No module named 'click'"
**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Tool not found"
**Solução:** Instale as ferramentas ou adicione ao PATH:
```bash
# Verificar se está no PATH
echo $PATH

# Adicionar ao PATH (temporário)
export PATH=$PATH:/usr/local/bin

# Adicionar ao PATH (permanente - adicione ao ~/.bashrc)
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Erro: "Permission denied"
**Solução:** Dar permissão de execução:
```bash
chmod +x /usr/local/bin/subfinder
chmod +x /usr/local/bin/httpx
chmod +x /usr/local/bin/whatweb
chmod +x /usr/local/bin/gobuster
chmod +x /usr/local/bin/nuclei
```

## Estrutura de Diretórios Esperada

```
reconner/
├── reconner/          # Código fonte
├── requirements.txt   # Dependências Python
├── README.md          # Documentação
├── setup.py          # Instalação
└── tests/            # Testes
```

## Próximos Passos

Após a instalação, consulte o [README.md](README.md) para exemplos de uso.

