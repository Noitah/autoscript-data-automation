#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PyInstaller.__main__
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SPEC_FILE = BASE_DIR / 'AutoScript.spec'

print("=" * 60)
print("Iniciando compilação do AutoScript v7.0")
print("=" * 60)

os.chdir(str(BASE_DIR))

PyInstaller.__main__.run([str(SPEC_FILE)])

print("\n" + "=" * 60)
print("✅ Compilação concluída!")
print("=" * 60)
print(f"Seu arquivo .exe está em: {BASE_DIR / 'dist' / 'AutoScript.exe'}")
print("Versão: 7.0 (Refatorada)")
print("=" * 60)
