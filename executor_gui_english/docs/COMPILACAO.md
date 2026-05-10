# Executable Build Guide

This guide explains how to compile the Executor GUI application into a Windows executable (.exe).

## Prerequisites

- Python 3.8+
- PyInstaller installed
- All project dependencies

## Step 1: Prepare the Environment

### 1.1 Create Virtual Environment

```bash
python -m venv venv
```

### 1.2 Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
pip install PyInstaller>=5.0
```

## Step 2: Build

### Option 1: Use Build Script (Recommended)

```bash
python scripts/build.py
```

### Option 2: Build Manually

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

## Step 3: Locate the Executable

After building, the `AutoScript.exe` file will be at:

```
dist/AutoScript.exe
```

## Step 4: Test the Executable

```bash
dist/AutoScript.exe
```

## Optimizations

### Reduce Executable Size

To create a smaller executable, use:

```bash
python scripts/build.py --optimize=2
```

### Remove Debug Files

```bash
python scripts/build.py --strip
```

## Troubleshooting

### Error: "PyInstaller not found"

```bash
pip install PyInstaller
```

### Error: "No module named 'src'"

Make sure you are in the project root directory:

```bash
cd executor_gui
python scripts/build.py
```

### Error: "Cannot find data file"

Check if the files exist:

```bash
ls assets/logo.png
ls -r src/modules/
```

### Executable doesn't start

1. Check the log file:
   ```bash
   type build/AutoScript/warn-AutoScript.txt
   ```

2. Try building in console mode:
   ```bash
   pyinstaller --onefile --console src/main.py
   ```

## Distribution

### Prepare for Distribution

1. Create distribution folder:
   ```bash
   mkdir AutoScript_v8.0
   cp dist/AutoScript.exe AutoScript_v8.0/
   cp docs/README.md AutoScript_v8.0/
   cp docs/INSTALACAO.md AutoScript_v8.0/
   ```

2. Compress:
   ```bash
   tar -czf AutoScript_v8.0.tar.gz AutoScript_v8.0/
   # or
   zip -r AutoScript_v8.0.zip AutoScript_v8.0/
   ```

## Cleanup

To remove build files:

```bash
rm -rf build dist *.spec
```

## Important Notes

- The build process may take a few minutes
- The generated executable will be larger than the source code (includes Python runtime)
- Always test the executable before distributing
- Keep the virtual environment active during the build
