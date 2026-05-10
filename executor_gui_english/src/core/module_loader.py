import sys
import importlib
from pathlib import Path
from typing import Any, Dict


class ModuleLoader:
    
    def __init__(self, modules_dir: Path):
        self.modules_dir = Path(modules_dir)
        self.cache: Dict[str, Any] = {}
        self._setup_paths()
    
    def _setup_paths(self) -> None:
        if self.modules_dir.exists():
            for module_dir in self.modules_dir.iterdir():
                if module_dir.is_dir() and not module_dir.name.startswith('_'):
                    module_path = str(module_dir)
                    if module_path not in sys.path:
                        sys.path.insert(0, module_path)
    
    def load(self, module_name: str) -> Any:
        if module_name in self.cache:
            return self.cache[module_name]
        
        try:
            module = importlib.import_module(module_name)
            self.cache[module_name] = module
            return module
        except ImportError as e:
            raise ImportError(f"Error importing module {module_name}: {e}")
    
    def load_module(self, module_name: str) -> Any:
        return self.load(module_name)
    
    def clear_cache(self) -> None:
        self.cache.clear()
