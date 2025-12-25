# 🌐 Instalação Global - Reconner

## Objetivo

Instalar o `reconner` para que possa ser executado de **qualquer lugar** do terminal, não apenas da pasta do projeto.

## 📋 Métodos Disponíveis

### Método 1: Instalação como Pacote Python (Recomendado) ⭐

Este é o método mais profissional e recomendado.

#### Passo 1: Navegar para o Diretório

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
```

#### Passo 2: Instalar em Modo Desenvolvimento

```bash
pip install -e .
```

Ou com `pip3`:

```bash
pip3 install -e .
```

O `-e` significa "editable" - você pode editar o código e as mudanças serão refletidas automaticamente.

#### Passo 3: Verificar Instalação

```bash
# Agora você pode executar de qualquer lugar!
reconner --help

# Ou
python3 -m reconner --help
```

**Pronto!** Agora você pode usar `reconner` de qualquer diretório.

---

### Método 2: Criar Symlink Manual

Se o método 1 não funcionar, você pode criar um symlink.

#### Passo 1: Criar Script Wrapper

```bash
cd ~/Pentest/projetos-seguraca/security-study/reconner

# Criar script executável
cat > /tmp/reconner_wrapper.sh << 'EOF'
#!/bin/bash
cd ~/Pentest/projetos-seguraca/security-study/reconner
python3 -m reconner "$@"
EOF

chmod +x /tmp/reconner_wrapper.sh
```

#### Passo 2: Criar Symlink

```bash
# Criar symlink em /usr/local/bin (requer sudo)
sudo ln -s /tmp/reconner_wrapper.sh /usr/local/bin/reconner

# OU criar em ~/.local/bin (não requer sudo)
mkdir -p ~/.local/bin
ln -s ~/Pentest/projetos-seguraca/security-study/reconner/reconner/cli.py ~/.local/bin/reconner
```

#### Passo 3: Adicionar ao PATH (se necessário)

```bash
# Adicionar ao ~/.bashrc
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

---

### Método 3: Alias no Bash (Mais Simples)

Adicione um alias ao seu `~/.bashrc`:

```bash
# Adicionar ao ~/.bashrc
echo 'alias reconner="cd ~/Pentest/projetos-seguraca/security-study/reconner && python3 -m reconner"' >> ~/.bashrc

# Recarregar
source ~/.bashrc
```

Agora você pode usar:
```bash
reconner --target example.com --output-dir ./results
```

---

## 🎯 Método Recomendado: Instalação como Pacote

Vamos fazer isso agora:

### Passo a Passo Completo

```bash
# 1. Ir para o diretório
cd ~/Pentest/projetos-seguraca/security-study/reconner

# 2. Instalar como pacote
pip install -e .

# 3. Verificar
which reconner
reconner --help

# 4. Testar de outro diretório
cd ~
reconner --help
```

---

## ✅ Verificação

Após a instalação, teste:

```bash
# De qualquer diretório
cd ~
reconner --version

cd /tmp
reconner --help

cd /home
reconner --target example.com --output-dir ./test
```

---

## 🔧 Desinstalar (se necessário)

```bash
pip uninstall reconner
```

---

## 📝 Notas

- O `setup.py` já está configurado com o entry point `reconner=reconner.cli:main`
- Após `pip install -e .`, o comando `reconner` estará disponível globalmente
- O `-e` permite editar o código sem reinstalar
- Se você atualizar o código, as mudanças serão refletidas automaticamente

---

## 🐛 Problemas Comuns

### "comando não encontrado" após instalação

**Solução:**
```bash
# Verificar se está no PATH
echo $PATH

# Verificar onde foi instalado
pip show -f reconner

# Adicionar ao PATH se necessário
export PATH=$PATH:~/.local/bin
```

### "Permission denied"

**Solução:**
```bash
# Usar --user para instalar apenas para o usuário
pip install --user -e .
```

### "Module not found"

**Solução:**
```bash
# Reinstalar dependências
pip install -r requirements.txt
pip install -e .
```

---

## 🎉 Pronto!

Após seguir o Método 1, você poderá usar `reconner` de qualquer lugar!

