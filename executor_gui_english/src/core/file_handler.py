from tkinter import filedialog
from typing import Optional, List, Tuple


class FileHandler:
    
    @staticmethod
    def select_file(title: str, file_types: List[Tuple[str, str]]) -> Optional[str]:
        file = filedialog.askopenfilename(title=title, filetypes=file_types)
        return file if file else None
    
    @staticmethod
    def select_folder(title: str) -> Optional[str]:
        folder = filedialog.askdirectory(title=title)
        return folder if folder else None
    
    @staticmethod
    def save_file(title: str, default_extension: str, file_types: List[Tuple[str, str]]) -> Optional[str]:
        file = filedialog.asksaveasfilename(
            title=title,
            defaultextension=default_extension,
            filetypes=file_types
        )
        return file if file else None
