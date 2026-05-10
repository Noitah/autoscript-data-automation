# Development Guide

Instructions for contributors who want to extend or modify the application.

## Architecture

### Layer Structure

```
UI Layer (tkinter)
    ↓
Core Layer (validation, file handling, modules)
    ↓
Modules Layer (business logic)
    ↓
External (pandas, PIL, etc)
```

### Main Components

1. **config.py**: Centralized configuration
2. **ui/**: Graphical interface (widgets, tabs, main_window)
3. **core/**: Core logic (validators, file_handler, module_loader)
4. **modules/**: Specific processing modules

## Adding a New Module

### 1. Create Directory Structure

```bash
mkdir -p src/modules/new_module
touch src/modules/new_module/__init__.py
touch src/modules/new_module/new_module.py
```

### 2. Implement the Module

**src/modules/new_module/new_module.py:**

```python
def execute_new_module(input_file: str, callback=None) -> tuple:
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    try:
        log("Starting new module...")
        # Your logic here
        return True, "Success!", {}
    except Exception as e:
        return False, f"Error: {e}", {}
```

### 3. Add Configuration

**src/config.py:**

```python
MODULES_CONFIG = {
    # ... existing modules ...
    'new_module': {
        'name': 'New Module Name',
        'icon': '🎯',
        'description': 'Module description',
        'module_name': 'new_module'
    }
}
```

### 4. Add Tab in UI

**src/ui/main_window.py:**

```python
def _create_new_module_tab(self) -> None:
    config = Config.MODULES_CONFIG['new_module']
    
    fields = {
        'file': {
            'type': 'file',
            'label': 'Input file:',
            'browse_command': lambda: self._select_and_update(
                self.new_module_file_var,
                'Select file',
                Config.FILE_TYPES['excel']
            )
        }
    }
    
    tab = TabFactory.create_simple_tab(
        self.notebook,
        config['name'],
        config['description'],
        fields,
        self.execute_new_module,
        "Execute"
    )
    
    self.new_module_tab = tab
    self.new_module_fields = tab.field_widgets

def _create_tabs(self) -> None:
    # ... existing tabs ...
    self._create_new_module_tab()

def execute_new_module(self) -> None:
    if self.running:
        messagebox.showwarning("Warning", "An execution is already in progress")
        return
    
    file_path = self.new_module_fields['file'].get()
    
    if not Validators.validate_file(file_path):
        messagebox.showerror("Error", "Invalid file")
        return
    
    def execute():
        try:
            self._set_running(True)
            self.log(f"File: {file_path}")
            
            new_module = self.module_loader.load('new_module')
            success, message, _ = new_module.execute_new_module(
                file_path, callback=self.log
            )
            
            if success:
                self.log(message)
                self.log("✓ Completed successfully!")
                messagebox.showinfo("Success", message)
            else:
                self.log(f"✗ Error: {message}")
                messagebox.showerror("Error", message)
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Execution error:\n{str(e)}")
        finally:
            self._set_running(False)
    
    thread = threading.Thread(target=execute, daemon=True)
    thread.start()
```

### 5. Update build.py

**scripts/build.py:**

```python
f'--add-data={SRC_DIR / "modules" / "new_module"}:src/modules/new_module',
'--hidden-import=new_module',
```

## Adding a New Widget

**src/ui/widgets.py:**

```python
class MyWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # Implement widget
    
    def get(self):
        # Return value
        pass
    
    def set(self, value):
        # Set value
        pass
```

## Adding Validation

**src/core/validators.py:**

```python
@staticmethod
def validate_email(email: str) -> Tuple[bool, str]:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    return False, "Invalid email"
```

## Code Standards

### Type Hints

```python
from typing import Dict, List, Tuple, Optional

def function(param1: str, param2: int) -> Tuple[bool, str]:
    return True, "success"
```

### Error Handling

```python
try:
    # code
except ValueError as e:
    self.log(f"Validation error: {e}")
except Exception as e:
    self.log(f"Unexpected error: {e}")
```

### Logging

```python
def log(msg: str) -> None:
    self.log_frame.append(msg)
```

## Testing

### Test Structure

```bash
mkdir -p tests
touch tests/__init__.py
touch tests/test_validators.py
```

### Test Example

**tests/test_validators.py:**

```python
import pytest
from src.core.validators import Validators

def test_validate_positive_integer():
    success, msg = Validators.validate_positive_integer("5")
    assert success is True
    
    success, msg = Validators.validate_positive_integer("-5")
    assert success is False
```

### Run Tests

```bash
pytest
```

## Code Formatting

### Black

```bash
black src/
```

### Flake8

```bash
flake8 src/
```

### MyPy

```bash
mypy src/
```

## Documentation

Add docstrings to all functions:

```python
def my_function(param1: str) -> str:
    """
    Brief description of the function.
    
    Args:
        param1: Parameter description
    
    Returns:
        Return description
    
    Raises:
        ValueError: When something is invalid
    """
    pass
```

## Debugging

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Breakpoints

```python
import pdb
pdb.set_trace()
```

## Performance

### Profiling

```python
import cProfile
cProfile.run('my_function()')
```

### Memory Profiling

```bash
pip install memory-profiler
python -m memory_profiler script.py
```

## Contribution Checklist

- [ ] Code follows PEP 8 standard
- [ ] Type hints added
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No unused imports
- [ ] No hardcoded values
- [ ] Proper error handling
- [ ] Clear execution log

## Useful Resources

- [Python Docs](https://docs.python.org/3/)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints](https://docs.python.org/3/library/typing.html)
