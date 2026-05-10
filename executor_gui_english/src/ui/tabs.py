import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any
from .widgets import DescriptionLabel


class TabFactory:
    
    @staticmethod
    def create_simple_tab(
        notebook: ttk.Notebook,
        tab_name: str,
        description: str,
        fields: Dict[str, Dict[str, Any]],
        execute_command: Callable,
        execute_button_text: str = "Execute"
    ) -> ttk.Frame:
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text=tab_name)
        
        frame.columnconfigure(1, weight=1)
        
        DescriptionLabel(frame, text=description).grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 15)
        )
        
        field_widgets = {}
        row = 1
        
        for field_name, field_config in fields.items():
            field_type = field_config.get('type', 'text')
            
            if field_type in ('file', 'folder'):
                ttk.Label(frame, text=field_config['label']).grid(
                    row=row, column=0, sticky=tk.W, pady=5
                )
                entry = ttk.Entry(frame, width=60)
                entry.grid(row=row, column=1, padx=5, sticky=(tk.W, tk.E))
                ttk.Button(
                    frame, text="Browse...",
                    command=field_config['browse_command'],
                    width=12
                ).grid(row=row, column=2)
                field_widgets[field_name] = entry
            
            elif field_type == 'integer':
                ttk.Label(frame, text=field_config['label']).grid(
                    row=row, column=0, sticky=tk.W, pady=5
                )
                var = tk.StringVar(value=field_config.get('default', '0'))
                entry = ttk.Entry(
                    frame, textvariable=var,
                    width=field_config.get('width', 10)
                )
                entry.grid(row=row, column=1, sticky=tk.W, padx=5)
                field_widgets[field_name] = var
            
            elif field_type == 'text':
                ttk.Label(frame, text=field_config['label']).grid(
                    row=row, column=0, sticky=tk.W, pady=5
                )
                var = tk.StringVar(value=field_config.get('default', ''))
                entry = ttk.Entry(frame, textvariable=var, width=60)
                entry.grid(row=row, column=1, padx=5, sticky=(tk.W, tk.E))
                field_widgets[field_name] = var
            
            elif field_type == 'note':
                note_label = ttk.Label(
                    frame,
                    text=field_config['text'],
                    foreground=field_config.get('color', 'orange'),
                    font=("Segoe UI", 9, "italic")
                )
                note_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
            
            row += 1
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        execute_btn = ttk.Button(
            btn_frame,
            text=execute_button_text,
            command=execute_command,
            style="Execute.TButton"
        )
        execute_btn.pack(ipadx=20, ipady=5)
        
        frame.field_widgets = field_widgets
        frame.execute_btn = execute_btn
        return frame
