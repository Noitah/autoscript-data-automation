import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import Optional


class DescriptionLabel(ttk.Label):
    
    def __init__(self, parent, text: str, **kwargs):
        super().__init__(
            parent,
            text=text,
            wraplength=800,
            justify=tk.LEFT,
            **kwargs
        )


class LogFrame(ttk.LabelFrame):
    
    def __init__(self, parent, title: str = "Execution Log", height: int = 10, **kwargs):
        super().__init__(parent, text=title, padding="5", **kwargs)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        from tkinter import scrolledtext
        self.log_text = scrolledtext.ScrolledText(
            self,
            height=height,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED,
            background="#1e1e1e",
            foreground="#d4d4d4",
            insertbackground="#ffffff",
            selectbackground="#264f78",
            selectforeground="#ffffff"
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text.tag_configure("timestamp", foreground="#6a9955")
        self.log_text.tag_configure("success", foreground="#4ec9b0")
        self.log_text.tag_configure("error", foreground="#f44747")
        self.log_text.tag_configure("info", foreground="#d4d4d4")
        
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=1, column=0, pady=(5, 0), sticky=tk.W)
        
        ttk.Button(btn_frame, text="Clear Log", command=self.clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Copy", command=self.copy_all).pack(side=tk.LEFT, padx=5)
    
    def append(self, message: str) -> None:
        def _insert():
            self.log_text.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime("[%H:%M:%S] ")
            self.log_text.insert(tk.END, timestamp, "timestamp")
            
            if message.startswith("✓") or "success" in message.lower() or "completed" in message.lower():
                tag = "success"
            elif message.startswith("✗") or "error" in message.lower():
                tag = "error"
            else:
                tag = "info"
            
            self.log_text.insert(tk.END, message + "\n", tag)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        
        try:
            self.log_text.after(0, _insert)
        except Exception:
            pass
    
    def clear(self) -> None:
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def copy_all(self) -> None:
        self.log_text.config(state=tk.NORMAL)
        content = self.log_text.get(1.0, tk.END)
        self.log_text.clipboard_clear()
        self.log_text.clipboard_append(content)
        self.log_text.config(state=tk.DISABLED)


class StatusBar(ttk.Frame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        
        self.var = tk.StringVar(value="Ready")
        
        self.label = ttk.Label(
            self,
            textvariable=self.var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        )
        self.label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.progress = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=150
        )
        self.progress.grid(row=0, column=1, padx=(10, 0))
        self.progress.grid_remove()
    
    def set_status(self, message: str) -> None:
        self.var.set(message)
    
    def set_ready(self) -> None:
        self.var.set("Ready")
        self.progress.stop()
        self.progress.grid_remove()
    
    def set_running(self, message: str = "Running...") -> None:
        self.var.set(message)
        self.progress.grid()
        self.progress.start(15)
    
    def set_error(self, message: str = "Error") -> None:
        self.var.set(f"Error: {message}")
        self.progress.stop()
        self.progress.grid_remove()
    
    def set_success(self, message: str = "Completed") -> None:
        self.var.set(f"Completed: {message}")
        self.progress.stop()
        self.progress.grid_remove()


class FileField(ttk.Frame):
    
    def __init__(self, parent, label: str, browse_command, is_folder: bool = False, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(1, weight=1)
        
        self.var = tk.StringVar()
        
        ttk.Label(self, text=label).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.entry = ttk.Entry(self, textvariable=self.var)
        self.entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self._browse_command = browse_command
        ttk.Button(self, text="Browse...", command=self._on_browse, width=12).grid(row=0, column=2)
    
    def _on_browse(self):
        self._browse_command()
    
    def get(self) -> str:
        return self.var.get()
    
    def set(self, value: str) -> None:
        self.var.set(value)
    
    def config(self, **kwargs):
        if 'textvariable' in kwargs:
            self.var = kwargs['textvariable']
            self.entry.config(textvariable=self.var)
        else:
            super().config(**kwargs)
