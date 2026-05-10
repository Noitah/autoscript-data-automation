# Installation Guide

## Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (optional, to clone the repository)

## Verify Python Installation

```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from: https://www.python.org/downloads/

## Windows Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd executor_gui
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m src.main
```

Or use the provided script:

```bash
scripts\run.bat
```

## Linux/macOS Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd executor_gui
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m src.main
```

Or use the provided script:

```bash
bash scripts/run.sh
```

## Troubleshooting

### Error: "python: command not found"

**Solution:** Use `python3` instead of `python`

```bash
python3 -m src.main
```

### Error: "ModuleNotFoundError: No module named 'tkinter'"

**Windows:**
```bash
# Reinstall Python and make sure to check "tcl/tk and IDLE" during installation
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### Error: "No module named 'pandas'"

**Solution:** Reinstall dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Error loading logo

**Solution:** Check if the file `assets/logo.png` exists

```bash
ls assets/logo.png
```

## Build Executable (Windows)

### 1. Install Build Dependencies

```bash
pip install -e ".[build]"
```

### 2. Build

```bash
python scripts/build.py
```

### 3. Generated Executable

The `AutoScript.exe` file will be created in `dist/`

## Update

To update to the latest version:

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## Uninstall

To remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove project folder
rm -rf executor_gui  # Linux/macOS
rmdir /s executor_gui  # Windows
```
