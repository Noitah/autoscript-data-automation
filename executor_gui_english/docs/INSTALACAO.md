# Guia de Instalação

## Pré-requisitos

- **Python 3.8 ou superior**
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar o repositório)

## Verificar Instalação do Python

```bash
python --version
# ou
python3 --version
```

Se o Python não estiver instalado, baixe em: https://www.python.org/downloads/

## Instalação em Windows

### 1. Clonar ou Baixar o Projeto

```bash
git clone <url-do-repositorio>
cd executor_gui
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

```bash
python -m src.main
```

Ou use o script fornecido:

```bash
scripts\run.bat
```

## Instalação em Linux/macOS

### 1. Clonar ou Baixar o Projeto

```bash
git clone <url-do-repositorio>
cd executor_gui
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

```bash
python -m src.main
```

Ou use o script fornecido:

```bash
bash scripts/run.sh
```

## Solução de Problemas

### Erro: "python: command not found"

**Solução:** Use `python3` em vez de `python`

```bash
python3 -m src.main
```

### Erro: "ModuleNotFoundError: No module named 'tkinter'"

**Windows:**
```bash
# Reinstale Python e certifique-se de marcar "tcl/tk and IDLE" na instalação
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### Erro: "No module named 'pandas'"

**Solução:** Reinstale as dependências

```bash
pip install --upgrade -r requirements.txt
```

### Erro ao carregar logo

**Solução:** Verifique se o arquivo `assets/logo.png` existe

```bash
ls assets/logo.png
```

## Compilação para Executável (Windows)

### 1. Instalar Dependências de Build

```bash
pip install -e ".[build]"
```

### 2. Compilar

```bash
python scripts/build.py
```

### 3. Executável Gerado

O arquivo `AutoScript.exe` será criado em `dist/`

## Atualização

Para atualizar para a versão mais recente:

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## Desinstalação

Para remover a aplicação:

```bash
# Desativar ambiente virtual
deactivate

# Remover pasta do projeto
rm -rf executor_gui  # Linux/macOS
rmdir /s executor_gui  # Windows
```
