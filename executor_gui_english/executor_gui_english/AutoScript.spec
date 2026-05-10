# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(Path.cwd() / 'src')],
    binaries=[],
    datas=[
        ('assets/logo.png', 'assets'),
        ('src/modules/rifa', 'src/modules/rifa'),
        ('src/modules/conciliacao', 'src/modules/conciliacao'),
        ('src/modules/pedidos', 'src/modules/pedidos'),
        ('src/modules/comparacao', 'src/modules/comparacao'),
        ('src/modules/marcar_usuarios', 'src/modules/marcar_usuarios'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'ui',
        'ui.main_window',
        'ui.widgets',
        'ui.tabs',
        'core',
        'core.validators',
        'core.file_handler',
        'core.module_loader',
        'config',
        'rifa_modulo',
        'conciliacao_modulo',
        'processar_pedidos',
        'extrair_detalhados_v9',
        'comparacao_modulo',
        'marcar_usuarios_modulo',
        'pandas',
        'numpy',
        'openpyxl',
        'fitz',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AutoScript',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
