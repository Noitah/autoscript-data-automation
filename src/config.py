import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent.parent

class Config:
    WINDOW_TITLE = "AutoScript - Executor de Scripts v8.0"
    WINDOW_WIDTH = 950
    WINDOW_HEIGHT = 780
    MIN_WIDTH = 750
    MIN_HEIGHT = 600
    
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#3498db',
        'success': '#27ae60',
        'error': '#e74c3c',
        'warning': '#f39c12',
        'bg_dark': '#1e1e1e',
        'fg_light': '#d4d4d4',
        'accent': '#0078d4'
    }
    
    THEME = 'clam'
    
    LOGO_PATH = BASE_DIR / 'assets' / 'logo.png'
    LOGO_WIDTH = 80
    
    MODULES_DIR = BASE_DIR / 'src' / 'modules'
    
    MODULES_CONFIG = {
        'rifa': {
            'name': 'Organizador de Rifa',
            'icon': 'Rifa',
            'description': 'Reorganiza dados de arquivos Excel em uma unica coluna seguindo padrao de blocos',
            'module_name': 'rifa_modulo'
        },
        'conciliacao': {
            'name': 'Conciliacao Financeira',
            'icon': 'Conciliacao',
            'description': 'Compara valores entre arquivo Excel e nomes de arquivos PDF, gerando relatorio de conciliacao',
            'module_name': 'conciliacao_modulo'
        },
        'pedidos': {
            'name': 'Processamento de Pedidos',
            'icon': 'Pedidos',
            'description': 'Processa pedidos de arquivos Excel e gera PDFs individualizados',
            'module_name': 'processar_pedidos'
        },
        'extrair': {
            'name': 'Extracao Detalhada',
            'icon': 'Extracao',
            'description': 'Extracao avancada com suporte a multiplas paginas e cache otimizado',
            'module_name': 'extrair_detalhados_v9'
        },
        'comparacao': {
            'name': 'Comparacao de Arquivos',
            'icon': 'Comparacao',
            'description': 'Compara dois arquivos de texto e gera relatorio de diferencas entre nomes',
            'module_name': 'comparacao_modulo'
        },
        'marcar_usuarios': {
            'name': 'Marcar Usuarios',
            'icon': 'Usuarios',
            'description': 'Marca usuarios com uso em um periodo retroativo em arquivo Excel',
            'module_name': 'marcar_usuarios_modulo'
        }
    }
    
    FILE_TYPES = {
        'excel': [('Excel files', '*.xlsx *.xls'), ('All files', '*.*')],
        'pdf': [('PDF files', '*.pdf'), ('All files', '*.*')],
        'text': [('Text files', '*.txt *.csv'), ('All files', '*.*')],
        'all': [('All files', '*.*')]
    }
    
    LOG_HEIGHT = 10
    LOG_FONT = ('Consolas', 9)
    TITLE_FONT = ('Segoe UI', 16, 'bold')
    SUBTITLE_FONT = ('Segoe UI', 10)
    LABEL_FONT = ('Segoe UI', 9)
