import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent.parent

class Config:
    WINDOW_TITLE = "AutoScript - Script Executor v8.0"
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
            'name': 'Excel Data Organizer',
            'icon': 'Organizer',
            'description': 'Reorganizes Excel data into a single column following block patterns',
            'module_name': 'rifa_modulo'
        },
        'conciliacao': {
            'name': 'Financial Reconciliation Engine',
            'icon': 'Reconciliation',
            'description': 'Compares values between Excel files and PDF file names, generating reconciliation reports',
            'module_name': 'conciliacao_modulo'
        },
        'pedidos': {
            'name': 'Smart Order Processor',
            'icon': 'Orders',
            'description': 'Processes orders from Excel files and generates individualized PDFs',
            'module_name': 'processar_pedidos'
        },
        'extrair': {
            'name': 'PDF Data Extractor',
            'icon': 'Extraction',
            'description': 'Advanced extraction with multi-page support and optimized caching',
            'module_name': 'extrair_detalhados_v9'
        },
        'comparacao': {
            'name': 'Data Comparison Tool',
            'icon': 'Comparison',
            'description': 'Compares two text files and generates a report of differences',
            'module_name': 'comparacao_modulo'
        },
        'marcar_usuarios': {
            'name': 'User Activity Marker',
            'icon': 'Users',
            'description': 'Marks users with usage in a retroactive period in Excel file',
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
