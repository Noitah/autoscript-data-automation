# Guia de Compilação para Executável

Este guia explica como compilar a aplicação Executor GUI em um executável Windows (.exe).

## Pré-requisitos

- Python 3.8+
- PyInstaller instalado
- Todas as dependências do projeto

## Passo 1: Preparar o Ambiente

### 1.1 Criar Ambiente Virtual

```bash
python -m venv venv
```

### 1.2 Ativar Ambiente Virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 1.3 Instalar Dependências

```bash
pip install -r requirements.txt
pip install PyInstaller>=5.0
```

## Passo 2: Compilar

### Opção 1: Usar Script de Build (Recomendado)

```bash
python scripts/build.py
```

### Opção 2: Compilar Manualmente

```bash
pyinstaller --onefile --windowed \
  --name=AutoScript \
  --add-data="assets/logo.png:assets" \
  --add-data="src/modules/rifa:src/modules/rifa" \
  --add-data="src/modules/conciliacao:src/modules/conciliacao" \
  --add-data="src/modules/pedidos:src/modules/pedidos" \
  --add-data="src/modules/comparacao:src/modules/comparacao" \
  --add-data="src/modules/marcar_usuarios:src/modules/marcar_usuarios" \
  --hidden-import=rifa_modulo \
  --hidden-import=conciliacao_modulo \
  --hidden-import=processar_pedidos \
  --hidden-import=extrair_detalhados_v9 \
  --hidden-import=comparacao_modulo \
  --hidden-import=marcar_usuarios_modulo \
  --hidden-import=pandas \
  --hidden-import=numpy \
  --hidden-import=openpyxl \
  --hidden-import=fitz \
  --hidden-import=PIL \
  src/main.py
```

## Passo 3: Localizar o Executável

Após a compilação, o arquivo `AutoScript.exe` estará em:

```
dist/AutoScript.exe
```

## Passo 4: Testar o Executável

```bash
dist/AutoScript.exe
```

## Otimizações

### Reduzir Tamanho do Executável

Para criar um executável menor, use:

```bash
python scripts/build.py --optimize=2
```

### Remover Arquivos de Debug

```bash
python scripts/build.py --strip
```

## Solução de Problemas

### Erro: "PyInstaller not found"

```bash
pip install PyInstaller
```

### Erro: "No module named 'src'"

Certifique-se de estar no diretório raiz do projeto:

```bash
cd executor_gui
python scripts/build.py
```

### Erro: "Cannot find data file"

Verifique se os arquivos existem:

```bash
ls assets/logo.png
ls -r src/modules/
```

### Executável não inicia

1. Verifique o arquivo de log:
   ```bash
   type build/AutoScript/warn-AutoScript.txt
   ```

2. Tente compilar com modo debug:
   ```bash
   pyinstaller --onefile --console src/main.py
   ```

## Distribuição

### Preparar para Distribuição

1. Criar pasta de distribuição:
   ```bash
   mkdir AutoScript_v8.0
   cp dist/AutoScript.exe AutoScript_v8.0/
   cp docs/README.md AutoScript_v8.0/
   cp docs/INSTALACAO.md AutoScript_v8.0/
   ```

2. Compactar:
   ```bash
   tar -czf AutoScript_v8.0.tar.gz AutoScript_v8.0/
   # ou
   zip -r AutoScript_v8.0.zip AutoScript_v8.0/
   ```

## Limpeza

Para remover arquivos de build:

```bash
rm -rf build dist *.spec
```

## Notas Importantes

- A compilação pode levar alguns minutos
- O executável gerado será maior que o código-fonte (inclui Python runtime)
- Sempre teste o executável antes de distribuir
- Mantenha o ambiente virtual ativo durante a compilação
