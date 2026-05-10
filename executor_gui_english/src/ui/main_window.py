import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from pathlib import Path
from typing import Optional

from config import Config
from core import FileHandler, Validators, ModuleLoader
from .widgets import LogFrame, StatusBar, DescriptionLabel
from .tabs import TabFactory


class ExecutorGUI:
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.minsize(Config.MIN_WIDTH, Config.MIN_HEIGHT)
        self.root.resizable(True, True)
        
        self._configure_styles()
        
        self.running = False
        self._logo_cache: Optional[ImageTk.PhotoImage] = None
        
        self.module_loader = ModuleLoader(Config.MODULES_DIR)
        
        self.create_interface()
    
    def _configure_styles(self) -> None:
        self.style = ttk.Style()
        self.style.theme_use(Config.THEME)
        
        self.style.configure("Execute.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 8)
        )
        self.style.map("Execute.TButton",
            background=[('active', Config.COLORS['secondary'])],
            foreground=[('disabled', 'gray')]
        )
        
        self.style.configure("Header.TLabel",
            font=Config.TITLE_FONT
        )
        
        self.style.configure("Subtitle.TLabel",
            font=Config.SUBTITLE_FONT,
            foreground="#555555"
        )
    
    def load_logo(self) -> Optional[ImageTk.PhotoImage]:
        if self._logo_cache is not None:
            return self._logo_cache
        
        if not Config.LOGO_PATH.exists():
            return None
        
        try:
            logo_img = Image.open(Config.LOGO_PATH)
            aspect_ratio = logo_img.height / logo_img.width
            new_height = int(Config.LOGO_WIDTH * aspect_ratio)
            logo_img = logo_img.resize((Config.LOGO_WIDTH, new_height), Image.Resampling.LANCZOS)
            self._logo_cache = ImageTk.PhotoImage(logo_img)
            return self._logo_cache
        except Exception:
            return None
    
    def create_interface(self) -> None:
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        self._create_header(main_frame)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self._create_tabs()
        
        self.log_frame = LogFrame(main_frame)
        self.log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_frame.rowconfigure(2, weight=1)
        
        self.status_bar = StatusBar(main_frame)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.log("Script Executor v8.0 started")
        self.log("Select a tab and configure the necessary files")
    
    def _create_header(self, parent: ttk.Frame) -> None:
        titulo_frame = ttk.Frame(parent)
        titulo_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        logo_photo = self.load_logo()
        if logo_photo:
            logo_label = ttk.Label(titulo_frame, image=logo_photo)
            logo_label.image = logo_photo
            logo_label.pack(pady=(0, 10))
        
        titulo = ttk.Label(
            titulo_frame,
            text="Script Executor",
            style="Header.TLabel"
        )
        titulo.pack()
        
        subtitulo = ttk.Label(
            titulo_frame,
            text="Select a script below to execute",
            style="Subtitle.TLabel"
        )
        subtitulo.pack()
    
    def _create_tabs(self) -> None:
        self._create_data_organizer_tab()
        self._create_reconciliation_tab()
        self._create_orders_tab()
        self._create_comparison_tab()
        self._create_mark_users_tab()
    
    def _create_data_organizer_tab(self) -> None:
        config = Config.MODULES_CONFIG['rifa']
        
        self.rifa_entrada_var = tk.StringVar()
        self.rifa_bloco_var = tk.StringVar(value='5')
        self.rifa_saida_var = tk.StringVar()
        
        fields = {
            'entrada': {
                'type': 'file',
                'label': 'Input Excel file:',
                'browse_command': lambda: self._select_and_update(
                    self.rifa_entrada_var,
                    'Select Excel file',
                    Config.FILE_TYPES['excel']
                )
            },
            'bloco': {
                'type': 'integer',
                'label': 'Block size:',
                'default': '5',
                'width': 10
            },
            'saida': {
                'type': 'file',
                'label': 'Output file:',
                'browse_command': lambda: self._save_and_update(
                    self.rifa_saida_var,
                    'Save as',
                    '.xlsx',
                    Config.FILE_TYPES['excel']
                )
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            config['name'],
            config['description'],
            fields,
            self.execute_data_organizer,
            "Execute Data Organizer"
        )
        
        self.rifa_tab = tab
        self.rifa_fields = tab.field_widgets
        self.rifa_fields['entrada'].config(textvariable=self.rifa_entrada_var)
        self.rifa_fields['bloco'] = self.rifa_bloco_var
        self.rifa_fields['saida'].config(textvariable=self.rifa_saida_var)
    
    def _create_reconciliation_tab(self) -> None:
        config = Config.MODULES_CONFIG['conciliacao']
        
        self.conciliacao_excel_var = tk.StringVar()
        self.conciliacao_pdfs_var = tk.StringVar()
        
        fields = {
            'excel': {
                'type': 'file',
                'label': 'Excel file:',
                'browse_command': lambda: self._select_and_update(
                    self.conciliacao_excel_var,
                    'Select Excel file',
                    Config.FILE_TYPES['excel']
                )
            },
            'pdfs': {
                'type': 'folder',
                'label': 'PDF folder:',
                'browse_command': lambda: self._select_folder_and_update(
                    self.conciliacao_pdfs_var,
                    'Select folder with PDFs'
                )
            },
            'nota': {
                'type': 'note',
                'text': 'PDFs must follow the pattern: MM DD VALUE.pdf (ex: 01 15 1234,56.pdf)',
                'color': 'orange'
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            config['name'],
            config['description'],
            fields,
            self.execute_reconciliation,
            "Execute Reconciliation"
        )
        
        self.conciliacao_tab = tab
        self.conciliacao_fields = tab.field_widgets
        self.conciliacao_fields['excel'].config(textvariable=self.conciliacao_excel_var)
        self.conciliacao_fields['pdfs'].config(textvariable=self.conciliacao_pdfs_var)
    
    def _create_orders_tab(self) -> None:
        config = Config.MODULES_CONFIG['pedidos']
        
        self.pedidos_excel_var = tk.StringVar()
        self.pedidos_pdf_var = tk.StringVar()
        self.pedidos_saida_var = tk.StringVar()
        
        fields = {
            'excel': {
                'type': 'file',
                'label': 'Excel file:',
                'browse_command': lambda: self._select_and_update(
                    self.pedidos_excel_var,
                    'Select Excel file',
                    Config.FILE_TYPES['excel']
                )
            },
            'pdf': {
                'type': 'file',
                'label': 'PDF file:',
                'browse_command': lambda: self._select_and_update(
                    self.pedidos_pdf_var,
                    'Select PDF file',
                    Config.FILE_TYPES['pdf']
                )
            },
            'saida': {
                'type': 'folder',
                'label': 'Output folder:',
                'browse_command': lambda: self._select_folder_and_update(
                    self.pedidos_saida_var,
                    'Select output folder'
                )
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            config['name'],
            config['description'],
            fields,
            self.execute_orders,
            "Execute Processing"
        )
        
        self.pedidos_tab = tab
        self.pedidos_fields = tab.field_widgets
        self.pedidos_fields['excel'].config(textvariable=self.pedidos_excel_var)
        self.pedidos_fields['pdf'].config(textvariable=self.pedidos_pdf_var)
        self.pedidos_fields['saida'].config(textvariable=self.pedidos_saida_var)
    
    def _create_comparison_tab(self) -> None:
        config = Config.MODULES_CONFIG['comparacao']
        
        self.comparacao_arquivo1_var = tk.StringVar()
        self.comparacao_arquivo2_var = tk.StringVar()
        self.comparacao_saida_var = tk.StringVar()
        
        fields = {
            'arquivo1': {
                'type': 'file',
                'label': 'File 1 (text):',
                'browse_command': lambda: self._select_and_update(
                    self.comparacao_arquivo1_var,
                    'Select first file',
                    Config.FILE_TYPES['text']
                )
            },
            'arquivo2': {
                'type': 'file',
                'label': 'File 2 (text):',
                'browse_command': lambda: self._select_and_update(
                    self.comparacao_arquivo2_var,
                    'Select second file',
                    Config.FILE_TYPES['text']
                )
            },
            'saida': {
                'type': 'file',
                'label': 'Output file:',
                'browse_command': lambda: self._save_and_update(
                    self.comparacao_saida_var,
                    'Save report as',
                    '.txt',
                    Config.FILE_TYPES['text']
                )
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            config['name'],
            config['description'],
            fields,
            self.execute_comparison,
            "Execute Comparison"
        )
        
        self.comparacao_tab = tab
        self.comparacao_fields = tab.field_widgets
        self.comparacao_fields['arquivo1'].config(textvariable=self.comparacao_arquivo1_var)
        self.comparacao_fields['arquivo2'].config(textvariable=self.comparacao_arquivo2_var)
        self.comparacao_fields['saida'].config(textvariable=self.comparacao_saida_var)
    
    def _create_mark_users_tab(self) -> None:
        config = Config.MODULES_CONFIG['marcar_usuarios']
        
        self.marcar_arquivo_var = tk.StringVar()
        self.marcar_meses_var = tk.StringVar(value='6')
        
        fields = {
            'arquivo': {
                'type': 'file',
                'label': 'Excel file:',
                'browse_command': lambda: self._select_and_update(
                    self.marcar_arquivo_var,
                    'Select Excel file',
                    Config.FILE_TYPES['excel']
                )
            },
            'meses': {
                'type': 'integer',
                'label': 'Months to analyze:',
                'default': '6',
                'width': 10
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            config['name'],
            config['description'],
            fields,
            self.execute_mark_users,
            "Execute Marking"
        )
        
        self.marcar_tab = tab
        self.marcar_usuarios_fields = tab.field_widgets
        self.marcar_usuarios_fields['arquivo'].config(textvariable=self.marcar_arquivo_var)
        self.marcar_usuarios_fields['meses'] = self.marcar_meses_var
    
    def _select_and_update(self, var: tk.StringVar, titulo: str, tipos: list) -> None:
        arquivo = FileHandler.select_file(titulo, tipos)
        if arquivo:
            var.set(arquivo)
    
    def _select_folder_and_update(self, var: tk.StringVar, titulo: str) -> None:
        pasta = FileHandler.select_folder(titulo)
        if pasta:
            var.set(pasta)
    
    def _save_and_update(self, var: tk.StringVar, titulo: str, extensao: str, tipos: list) -> None:
        arquivo = FileHandler.save_file(titulo, extensao, tipos)
        if arquivo:
            var.set(arquivo)
    
    def log(self, message: str) -> None:
        self.log_frame.append(message)
    
    def _set_running(self, estado: bool) -> None:
        self.running = estado
        self.status_bar.set_status("Running..." if estado else "Ready")
    
    def execute_data_organizer(self) -> None:
        entrada = self.rifa_entrada_var.get()
        bloco = self.rifa_bloco_var.get()
        saida = self.rifa_saida_var.get()
        
        if not Validators.validate_file(entrada):
            messagebox.showerror("Error", "Invalid input file")
            return
        if not Validators.validate_integer(bloco, 1, 1000):
            messagebox.showerror("Error", "Block size must be between 1 and 1000")
            return
        if not saida:
            messagebox.showerror("Error", "Output file not specified")
            return
        
        self._set_running(True)
        thread = threading.Thread(
            target=self._execute_rifa_thread,
            args=(entrada, int(bloco), saida)
        )
        thread.daemon = True
        thread.start()
    
    def _execute_rifa_thread(self, entrada: str, bloco: int, saida: str) -> None:
        try:
            self.log(f"Starting Data Organizer...")
            self.log(f"Input: {entrada}")
            self.log(f"Block size: {bloco}")
            
            modulo = self.module_loader.load_module('rifa')
            resultado = modulo.processar(entrada, bloco, saida)
            
            if resultado:
                self.log(f"✓ Success! Output saved to: {saida}")
                messagebox.showinfo("Success", "Data organization completed successfully!")
            else:
                self.log("✗ Error during processing")
                messagebox.showerror("Error", "Error during processing")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            self._set_running(False)
    
    def execute_reconciliation(self) -> None:
        excel = self.conciliacao_excel_var.get()
        pdfs = self.conciliacao_pdfs_var.get()
        
        if not Validators.validate_file(excel):
            messagebox.showerror("Error", "Invalid Excel file")
            return
        if not Validators.validate_folder(pdfs):
            messagebox.showerror("Error", "Invalid PDF folder")
            return
        
        self._set_running(True)
        thread = threading.Thread(
            target=self._execute_reconciliation_thread,
            args=(excel, pdfs)
        )
        thread.daemon = True
        thread.start()
    
    def _execute_reconciliation_thread(self, excel: str, pdfs: str) -> None:
        try:
            self.log(f"Starting Financial Reconciliation...")
            self.log(f"Excel file: {excel}")
            self.log(f"PDF folder: {pdfs}")
            
            modulo = self.module_loader.load_module('conciliacao')
            resultado = modulo.processar(excel, pdfs)
            
            if resultado:
                self.log(f"✓ Reconciliation completed!")
                messagebox.showinfo("Success", "Reconciliation completed successfully!")
            else:
                self.log("✗ Error during reconciliation")
                messagebox.showerror("Error", "Error during reconciliation")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            self._set_running(False)
    
    def execute_orders(self) -> None:
        excel = self.pedidos_excel_var.get()
        pdf = self.pedidos_pdf_var.get()
        saida = self.pedidos_saida_var.get()
        
        if not Validators.validate_file(excel):
            messagebox.showerror("Error", "Invalid Excel file")
            return
        if not Validators.validate_file(pdf):
            messagebox.showerror("Error", "Invalid PDF file")
            return
        if not Validators.validate_folder(saida):
            messagebox.showerror("Error", "Invalid output folder")
            return
        
        self._set_running(True)
        thread = threading.Thread(
            target=self._execute_orders_thread,
            args=(excel, pdf, saida)
        )
        thread.daemon = True
        thread.start()
    
    def _execute_orders_thread(self, excel: str, pdf: str, saida: str) -> None:
        try:
            self.log(f"Starting Order Processing...")
            self.log(f"Excel: {excel}")
            self.log(f"PDF: {pdf}")
            self.log(f"Output folder: {saida}")
            
            modulo = self.module_loader.load_module('pedidos')
            resultado = modulo.processar(excel, pdf, saida)
            
            if resultado:
                self.log(f"✓ Order processing completed!")
                messagebox.showinfo("Success", "Order processing completed successfully!")
            else:
                self.log("✗ Error during processing")
                messagebox.showerror("Error", "Error during processing")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            self._set_running(False)
    
    def execute_comparison(self) -> None:
        arquivo1 = self.comparacao_arquivo1_var.get()
        arquivo2 = self.comparacao_arquivo2_var.get()
        saida = self.comparacao_saida_var.get()
        
        if not Validators.validate_file(arquivo1):
            messagebox.showerror("Error", "Invalid file 1")
            return
        if not Validators.validate_file(arquivo2):
            messagebox.showerror("Error", "Invalid file 2")
            return
        if not saida:
            messagebox.showerror("Error", "Output file not specified")
            return
        
        self._set_running(True)
        thread = threading.Thread(
            target=self._execute_comparison_thread,
            args=(arquivo1, arquivo2, saida)
        )
        thread.daemon = True
        thread.start()
    
    def _execute_comparison_thread(self, arquivo1: str, arquivo2: str, saida: str) -> None:
        try:
            self.log(f"Starting File Comparison...")
            self.log(f"File 1: {arquivo1}")
            self.log(f"File 2: {arquivo2}")
            
            modulo = self.module_loader.load_module('comparacao')
            resultado = modulo.processar(arquivo1, arquivo2, saida)
            
            if resultado:
                self.log(f"✓ Comparison completed! Report saved to: {saida}")
                messagebox.showinfo("Success", "Comparison completed successfully!")
            else:
                self.log("✗ Error during comparison")
                messagebox.showerror("Error", "Error during comparison")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            self._set_running(False)
    
    def execute_mark_users(self) -> None:
        arquivo = self.marcar_arquivo_var.get()
        meses = self.marcar_meses_var.get()
        
        if not Validators.validate_file(arquivo):
            messagebox.showerror("Error", "Invalid Excel file")
            return
        if not Validators.validate_integer(meses, 1, 60):
            messagebox.showerror("Error", "Months must be between 1 and 60")
            return
        
        self._set_running(True)
        thread = threading.Thread(
            target=self._execute_mark_users_thread,
            args=(arquivo, int(meses))
        )
        thread.daemon = True
        thread.start()
    
    def _execute_mark_users_thread(self, arquivo: str, meses: int) -> None:
        try:
            self.log(f"Starting Mark Users...")
            self.log(f"File: {arquivo}")
            self.log(f"Months to analyze: {meses}")
            
            modulo = self.module_loader.load_module('marcar_usuarios')
            resultado = modulo.processar(arquivo, meses)
            
            if resultado:
                self.log(f"✓ Users marked successfully!")
                messagebox.showinfo("Success", "Users marked successfully!")
            else:
                self.log("✗ Error during marking")
                messagebox.showerror("Error", "Error during marking")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            self._set_running(False)


def main():
    root = tk.Tk()
    app = ExecutorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
