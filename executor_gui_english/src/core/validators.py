import os
from pathlib import Path
from typing import Dict, Tuple


class Validators:
    
    @staticmethod
    def validate_fields(fields_dict: Dict[str, str]) -> Tuple[bool, str]:
        for name, value in fields_dict.items():
            if not value or (isinstance(value, str) and not value.strip()):
                return False, f"Field '{name}' is required"
        return True, ""
    
    @staticmethod
    def validate_files_exist(files_dict: Dict[str, str]) -> Tuple[bool, str]:
        for name, path in files_dict.items():
            if not os.path.exists(path):
                return False, f"File not found: {name}\n{path}"
        return True, ""
    
    @staticmethod
    def validate_positive_integer(value: str, name: str = "value") -> Tuple[bool, str]:
        try:
            num = int(value)
            if num <= 0:
                return False, f"{name} must be a positive number"
            return True, ""
        except ValueError:
            return False, f"{name} must be a valid integer"
    
    @staticmethod
    def validate_file(path: str) -> bool:
        if not path or not path.strip():
            return False
        return os.path.exists(path)
    
    @staticmethod
    def validate_folder(path: str) -> bool:
        if not path or not path.strip():
            return False
        return os.path.isdir(path)
    
    @staticmethod
    def validate_integer(value: str, min_val: int = 1, max_val: int = 9999) -> bool:
        try:
            num = int(value)
            return min_val <= num <= max_val
        except (ValueError, TypeError):
            return False
