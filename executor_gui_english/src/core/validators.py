import os
from pathlib import Path
from typing import Dict, Tuple


class Validators:
    
    @staticmethod
    def validar_campos(campos_dict: Dict[str, str]) -> Tuple[bool, str]:
        for nome, valor in campos_dict.items():
            if not valor or (isinstance(valor, str) and not valor.strip()):
                return False, f"Campo '{nome}' é obrigatório"
        return True, ""
    
    @staticmethod
    def validar_arquivos_existem(arquivos_dict: Dict[str, str]) -> Tuple[bool, str]:
        for nome, caminho in arquivos_dict.items():
            if not os.path.exists(caminho):
                return False, f"Arquivo não encontrado: {nome}\n{caminho}"
        return True, ""
    
    @staticmethod
    def validar_inteiro_positivo(valor: str, nome: str = "valor") -> Tuple[bool, str]:
        try:
            num = int(valor)
            if num <= 0:
                return False, f"{nome} deve ser um número positivo"
            return True, ""
        except ValueError:
            return False, f"{nome} deve ser um número inteiro válido"
    
    @staticmethod
    def validar_arquivo_existe(caminho: str) -> Tuple[bool, str]:
        if not caminho or not caminho.strip():
            return False, "Caminho do arquivo não pode estar vazio"
        if not os.path.exists(caminho):
            return False, f"Arquivo não encontrado: {caminho}"
        return True, ""
    
    @staticmethod
    def validar_pasta_existe(caminho: str) -> Tuple[bool, str]:
        if not caminho or not caminho.strip():
            return False, "Caminho da pasta não pode estar vazio"
        if not os.path.isdir(caminho):
            return False, f"Pasta não encontrada: {caminho}"
        return True, ""
