# AutoScript - Script Executor v8.0

Graphical interface for data processing automation with multiple specialized modules.

## 📋 Features

- **Excel Data Organizer**: Reorganizes Excel data into a single column following block patterns
- **Financial Reconciliation Engine**: Compares values between Excel files and PDF file names
- **Smart Order Processor**: Processes orders and generates individualized PDFs
- **PDF Data Extractor**: Advanced extraction with multi-page support
- **Data Comparison Tool**: Compares two text files and generates a report of differences
- **User Activity Marker**: Marks users with usage in a retroactive period

## 🚀 Quick Start

### Requirements
- Python 3.8+
- pip or conda

### Installation

```bash
pip install -r requirements.txt
```

### Execution

**Linux/macOS:**
```bash
bash scripts/run.sh
```

**Windows:**
```bash
scripts\run.bat
```

**Or directly with Python:**
```bash
python -m src.main
```

## 📁 Project Structure

```
executor_gui/
├── src/
│   ├── main.py                 # Entry point
│   ├── config.py               # Centralized configuration
│   ├── ui/                     # Graphical interface
│   │   ├── main_window.py      # Main window
│   │   ├── tabs.py             # Tab creation
│   │   └── widgets.py          # Reusable components
│   ├── core/                   # Core logic
│   │   ├── validators.py       # Data validation
│   │   ├── file_handler.py     # File selection/saving
│   │   └── module_loader.py    # Dynamic loading
│   └── modules/                # Processing modules
│       ├── rifa/
│       ├── conciliacao/
│       ├── pedidos/
│       ├── comparacao/
│       └── marcar_usuarios/
├── assets/                     # Resources (images, etc)
├── docs/                       # Documentation
├── scripts/                    # Build and execution scripts
├── requirements.txt            # Dependencies
└── pyproject.toml             # Project configuration
```

## 🔧 Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
```

### Type Checking

```bash
mypy src/
```

## 📦 Build Executable

### Install Build Dependencies

```bash
pip install -e ".[build]"
```

### Build

```bash
python scripts/build.py
```

The executable will be generated at `dist/AutoScript.exe`

## 🎨 Improvements Made

### Organization
- ✅ Clear and well-defined modular structure
- ✅ Separation of concerns
- ✅ Reusable code

### Quality
- ✅ Type hints throughout the code
- ✅ Robust data validation
- ✅ Improved error handling
- ✅ Structured logging

### Maintainability
- ✅ Reduced code duplication
- ✅ Smaller and more focused methods
- ✅ Centralized configuration
- ✅ Clear documentation

### Performance
- ✅ Optimized module caching
- ✅ Efficient dynamic loading
- ✅ Reduced executable size

## 📝 Release Notes

### v8.0.0
- Full English translation
- Multi-page order support
- Improved UI/UX

## 📧 Support

Author: João Victor Cotrim - joaocotrimprofi@gmail.com

## 📄 License

MIT License - See LICENSE for details.
