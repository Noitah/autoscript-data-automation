#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PyInstaller.__main__
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SPEC_FILE = BASE_DIR / 'AutoScript.spec'

print("=" * 60)
print("Starting AutoScript v8.0 build")
print("=" * 60)

os.chdir(str(BASE_DIR))

PyInstaller.__main__.run([str(SPEC_FILE)])

print("\n" + "=" * 60)
print("Build completed successfully!")
print("=" * 60)
print(f"Your .exe file is at: {BASE_DIR / 'dist' / 'AutoScript.exe'}")
print("Version: 8.0")
print("=" * 60)
