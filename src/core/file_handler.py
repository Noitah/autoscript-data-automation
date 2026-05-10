from tkinter import filedialog
from typing import Optional, List, Tuple


class FileHandler:
    
    @staticmethod
    def selecionar_arquivo(titulo: str, tipos_arquivo: List[Tuple[str, str]]) -> Optional[str]:
        arquivo = filedialog.askopenfilename(title=titulo, filetypes=tipos_arquivo)
        return arquivo if arquivo else None
    
    @staticmethod
    def selecionar_pasta(titulo: str) -> Optional[str]:
        pasta = filedialog.askdirectory(title=titulo)
        return pasta if pasta else None
    
    @staticmethod
    def salvar_arquivo(titulo: str, extensao_padrao: str, tipos_arquivo: List[Tuple[str, str]]) -> Optional[str]:
        arquivo = filedialog.asksaveasfilename(
            title=titulo,
            defaultextension=extensao_padrao,
            filetypes=tipos_arquivo
        )
        return arquivo if arquivo else None
