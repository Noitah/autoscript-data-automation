#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ui.main_window import ExecutorGUI


def main():
    root = tk.Tk()
    app = ExecutorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
