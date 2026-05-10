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
        
        self._configurar_estilos()
        
        self.executando = False
        self._logo_cache: Optional[ImageTk.PhotoImage] = None
        
        self.module_loader = ModuleLoader(Config.MODULES_DIR)
        
        self.criar_interface()
    
    def _configurar_estilos(self) -> None:
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
    
    def carregar_logo(self) -> Optional[ImageTk.PhotoImage]:
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
    
    def criar_interface(self) -> None:
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        self._criar_header(main_frame)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self._criar_abas()
        
        self.log_frame = LogFrame(main_frame)
        self.log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_frame.rowconfigure(2, weight=1)
        
        self.status_bar = StatusBar(main_frame)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.log("Executor de Scripts v8.0 iniciado")
        self.log("Selecione uma aba e configure os arquivos necessarios")
    
    def _criar_header(self, parent: ttk.Frame) -> None:
        titulo_frame = ttk.Frame(parent)
        titulo_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        logo_photo = self.carregar_logo()
        if logo_photo:
            logo_label = ttk.Label(titulo_frame, image=logo_photo)
            logo_label.image = logo_photo
            logo_label.pack(pady=(0, 10))
        
        titulo = ttk.Label(
            titulo_frame,
            text="Executor de Scripts",
            style="Header.TLabel"
        )
        titulo.pack()
        
        subtitulo = ttk.Label(
            titulo_frame,
            text="Selecione um script abaixo para executar",
            style="Subtitle.TLabel"
        )
        subtitulo.pack()
    
    def _criar_abas(self) -> None:
        self._criar_aba_rifa()
        self._criar_aba_conciliacao()
        self._criar_aba_pedidos()
        self._criar_aba_comparacao()
        self._criar_aba_marcar_usuarios()
    
    def _criar_aba_rifa(self) -> None:
        config = Config.MODULES_CONFIG['rifa']
        
        self.rifa_entrada_var = tk.StringVar()
        self.rifa_bloco_var = tk.StringVar(value='5')
        self.rifa_saida_var = tk.StringVar()
        
        fields = {
            'entrada': {
                'type': 'file',
                'label': 'Arquivo Excel de entrada:',
                'browse_command': lambda: self._selecionar_e_atualizar(
                    self.rifa_entrada_var,
                    'Selecionar arquivo Excel',
                    Config.FILE_TYPES['excel']
                )
            },
            'bloco': {
                'type': 'integer',
                'label': 'Tamanho do bloco:',
                'default': '5',
                'width': 10
            },
            'saida': {
                'type': 'file',
                'label': 'Arquivo de saida:',
                'browse_command': lambda: self._salvar_e_atualizar(
                    self.rifa_saida_var,
                    'Salvar como',
                    '.xlsx',
                    Config.FILE_TYPES['excel']
                )
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            f" {config['icon']} ",
            config['description'],
            fields,
            self.executar_rifa,
            "Executar Organizador de Rifa"
        )
        
        self.rifa_tab = tab
        self.rifa_fields = tab.field_widgets
        self.rifa_fields['entrada'].config(textvariable=self.rifa_entrada_var)
        self.rifa_fields['bloco'] = self.rifa_bloco_var
        self.rifa_fields['saida'].config(textvariable=self.rifa_saida_var)
    
    def _criar_aba_conciliacao(self) -> None:
        config = Config.MODULES_CONFIG['conciliacao']
        
        self.conciliacao_excel_var = tk.StringVar()
        self.conciliacao_pdfs_var = tk.StringVar()
        
        fields = {
            'excel': {
                'type': 'file',
                'label': 'Arquivo Excel:',
                'browse_command': lambda: self._selecionar_e_atualizar(
                    self.conciliacao_excel_var,
                    'Selecionar arquivo Excel',
                    Config.FILE_TYPES['excel']
                )
            },
            'pdfs': {
                'type': 'folder',
                'label': 'Pasta com PDFs:',
                'browse_command': lambda: self._selecionar_pasta_e_atualizar(
                    self.conciliacao_pdfs_var,
                    'Selecionar pasta com PDFs'
                )
            },
            'nota': {
                'type': 'note',
                'text': 'Os PDFs devem seguir o padrao: MM DD VALOR.pdf (ex: 01 15 1234,56.pdf)',
                'color': 'orange'
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            f" {config['icon']} ",
            config['description'],
            fields,
            self.executar_conciliacao,
            "Executar Conciliacao"
        )
        
        self.conciliacao_tab = tab
        self.conciliacao_fields = tab.field_widgets
        self.conciliacao_fields['excel'].config(textvariable=self.conciliacao_excel_var)
        self.conciliacao_fields['pdfs'].config(textvariable=self.conciliacao_pdfs_var)
    
    def _criar_aba_pedidos(self) -> None:
        config = Config.MODULES_CONFIG['pedidos']
        
        self.pedidos_excel_var = tk.StringVar()
        self.pedidos_pdf_var = tk.StringVar()
        self.pedidos_saida_var = tk.StringVar()
        
        fields = {
            'excel': {
                'type': 'file',
                'label': 'Arquivo Excel:',
                'browse_command': lambda: self._selecionar_e_atualizar(
                    self.pedidos_excel_var,
                    'Selecionar arquivo Excel',
                    Config.FILE_TYPES['excel']
                )
            },
            'pdf': {
                'type': 'file',
                'label': 'Arquivo PDF:',
                'browse_command': lambda: self._selecionar_e_atualizar(
                    self.pedidos_pdf_var,
                    'Selecionar arquivo PDF',
                    Config.FILE_TYPES['pdf']
                )
            },
            'saida': {
                'type': 'folder',
                'label': 'Pasta de saida:',
                'browse_command': lambda: self._selecionar_pasta_e_atualizar(
                    self.pedidos_saida_var,
                    'Selecionar pasta de saida'
                )
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            f" {config['icon']} ",
            config['description'],
            fields,
            self.executar_pedidos,
            "Executar Processamento"
        )
        
        self.pedidos_tab = tab
        self.pedidos_fields = tab.field_widgets
        self.pedidos_fields['excel'].config(textvariable=self.pedidos_excel_var)
        self.pedidos_fields['pdf'].config(textvariable=self.pedidos_pdf_var)
        self.pedidos_fields['saida'].config(textvariable=self.pedidos_saida_var)
    
    def _criar_aba_comparacao(self) -> None:
        config = Config.MODULES_CONFIG['comparacao']
        
        self.comparacao_arquivo1_var = tk.StringVar()
        self.comparacao_arquivo2_var = tk.StringVar()
        self.comparacao_saida_var = tk.StringVar()
        
        fields = {
            'arquivo1': {
                'type': 'file',
                'label': 'Arquivo 1 (texto):',
                'browse_command': lambda: self._selecionar_e_atualizar(
                    self.comparacao_arquivo1_var,
                    'Selecionar primeiro arquivo',
                    Config.FILE_TYPES['text']
                )
            },
            'arquivo2': {
                'type': 'file',
                'label': 'Arquivo 2 (texto):',
                'browse_command': lambda: self._selecionar_e_atualizar(
                    self.comparacao_arquivo2_var,
                    'Selecionar segundo arquivo',
                    Config.FILE_TYPES['text']
                )
            },
            'saida': {
                'type': 'file',
                'label': 'Arquivo de saida:',
                'browse_command': lambda: self._salvar_e_atualizar(
                    self.comparacao_saida_var,
                    'Salvar relatorio como',
                    '.txt',
                    Config.FILE_TYPES['text']
                )
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            f" {config['icon']} ",
            config['description'],
            fields,
            self.executar_comparacao,
            "Executar Comparacao"
        )
        
        self.comparacao_tab = tab
        self.comparacao_fields = tab.field_widgets
        self.comparacao_fields['arquivo1'].config(textvariable=self.comparacao_arquivo1_var)
        self.comparacao_fields['arquivo2'].config(textvariable=self.comparacao_arquivo2_var)
        self.comparacao_fields['saida'].config(textvariable=self.comparacao_saida_var)
    
    def _criar_aba_marcar_usuarios(self) -> None:
        config = Config.MODULES_CONFIG['marcar_usuarios']
        
        self.marcar_arquivo_var = tk.StringVar()
        self.marcar_meses_var = tk.StringVar(value='6')
        
        fields = {
            'arquivo': {
                'type': 'file',
                'label': 'Arquivo Excel:',
                'browse_command': lambda: self._selecionar_e_atualizar(
                    self.marcar_arquivo_var,
                    'Selecionar arquivo Excel',
                    Config.FILE_TYPES['excel']
                )
            },
            'meses': {
                'type': 'integer',
                'label': 'Meses para analisar:',
                'default': '6',
                'width': 10
            }
        }
        
        tab = TabFactory.create_simple_tab(
            self.notebook,
            f" {config['icon']} ",
            config['description'],
            fields,
            self.executar_marcar_usuarios,
            "Executar Marcacao"
        )
        
        self.marcar_tab = tab
        self.marcar_usuarios_fields = tab.field_widgets
        self.marcar_usuarios_fields['arquivo'].config(textvariable=self.marcar_arquivo_var)
        self.marcar_usuarios_fields['meses'] = self.marcar_meses_var
    
    def _selecionar_e_atualizar(self, var: tk.StringVar, titulo: str, tipos: list) -> None:
        arquivo = FileHandler.selecionar_arquivo(titulo, tipos)
        if arquivo:
            var.set(arquivo)
    
    def _selecionar_pasta_e_atualizar(self, var: tk.StringVar, titulo: str) -> None:
        pasta = FileHandler.selecionar_pasta(titulo)
        if pasta:
            var.set(pasta)
    
    def _salvar_e_atualizar(self, var: tk.StringVar, titulo: str, extensao: str, tipos: list) -> None:
        arquivo = FileHandler.salvar_arquivo(titulo, extensao, tipos)
        if arquivo:
            var.set(arquivo)
    
    def log(self, message: str) -> None:
        self.log_frame.append(message)
    
    def _set_executando(self, estado: bool) -> None:
        self.executando = estado
    
    def _executar_em_thread(self, func, nome_operacao: str) -> None:
        if self.executando:
            messagebox.showwarning("Aviso", "Ja existe uma execucao em andamento")
            return
        
        def wrapper():
            try:
                self._set_executando(True)
                self.status_bar.set_running(f"Executando {nome_operacao}...")
                func()
            except Exception as e:
                self.log(f"Erro: {str(e)}")
                self.status_bar.set_error(str(e)[:50])
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao executar:\n{str(e)}"))
            finally:
                self._set_executando(False)
                self.status_bar.set_ready()
        
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
    
    def executar_rifa(self) -> None:
        entrada = self.rifa_entrada_var.get()
        bloco = self.rifa_bloco_var.get()
        saida = self.rifa_saida_var.get()
        
        validacao, msg = Validators.validar_campos({
            "Arquivo de entrada": entrada,
            "Tamanho do bloco": bloco,
            "Arquivo de saida": saida
        })
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_inteiro_positivo(bloco, "Tamanho do bloco")
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_arquivo_existe(entrada)
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        def executar():
            self.log(f"Iniciando organizador de rifa...")
            self.log(f"Entrada: {entrada}")
            self.log(f"Tamanho do bloco: {bloco}")
            self.log(f"Saida: {saida}")
            
            rifa = self.module_loader.load('rifa_modulo')
            sucesso, mensagem, _ = rifa.reorganizar_dados_em_blocos(
                entrada, saida, int(bloco), callback=self.log
            )
            
            if sucesso:
                self.log(mensagem)
                self.log("Organizador de rifa concluido com sucesso!")
                self.status_bar.set_success("Rifa concluida")
                self.root.after(0, lambda: messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{saida}"))
            else:
                raise Exception(mensagem)
        
        self._executar_em_thread(executar, "organizador de rifa")
    
    def executar_conciliacao(self) -> None:
        excel = self.conciliacao_excel_var.get()
        pdfs = self.conciliacao_pdfs_var.get()
        
        validacao, msg = Validators.validar_campos({
            "Arquivo Excel": excel,
            "Pasta com PDFs": pdfs
        })
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_arquivo_existe(excel)
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_pasta_existe(pdfs)
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        def executar():
            self.log(f"Iniciando conciliacao financeira...")
            self.log(f"Excel: {excel}")
            self.log(f"Pasta PDFs: {pdfs}")
            
            conciliacao = self.module_loader.load('conciliacao_modulo')
            sucesso, mensagem, caminho_arquivo = conciliacao.executar_conciliacao(
                excel, pdfs, callback=self.log
            )
            
            if sucesso:
                self.log(mensagem)
                self.log("Conciliacao concluida com sucesso!")
                self.status_bar.set_success("Conciliacao concluida")
                self.root.after(0, lambda: messagebox.showinfo("Sucesso", f"Conciliacao concluida!\n\nArquivo: {caminho_arquivo}"))
            else:
                raise Exception(mensagem)
        
        self._executar_em_thread(executar, "conciliacao")
    
    def executar_pedidos(self) -> None:
        excel = self.pedidos_excel_var.get()
        pdf = self.pedidos_pdf_var.get()
        saida = self.pedidos_saida_var.get()
        
        validacao, msg = Validators.validar_campos({
            "Arquivo Excel": excel,
            "Arquivo PDF": pdf,
            "Pasta de saida": saida
        })
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_arquivo_existe(excel)
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_arquivo_existe(pdf)
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        def executar():
            self.log(f"Iniciando processamento de pedidos...")
            self.log(f"Excel: {excel}")
            self.log(f"PDF: {pdf}")
            self.log(f"Saida: {saida}")
            
            pedidos = self.module_loader.load('processar_pedidos')
            sucesso, mensagem, stats = pedidos.executar_processamento_pedidos(
                excel, pdf, saida, callback=self.log
            )
            
            if sucesso:
                self.log("Processamento de pedidos concluido com sucesso!")
                self.status_bar.set_success("Pedidos processados")
                self.root.after(0, lambda: messagebox.showinfo("Sucesso", f"PDFs gerados em:\n{saida}"))
            else:
                raise Exception(mensagem)
        
        self._executar_em_thread(executar, "processamento de pedidos")
    
    def executar_comparacao(self) -> None:
        arquivo1 = self.comparacao_arquivo1_var.get()
        arquivo2 = self.comparacao_arquivo2_var.get()
        saida = self.comparacao_saida_var.get()
        
        validacao, msg = Validators.validar_campos({
            "Arquivo 1": arquivo1,
            "Arquivo 2": arquivo2,
            "Arquivo de saida": saida
        })
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_arquivos_existem({
            "Arquivo 1": arquivo1,
            "Arquivo 2": arquivo2
        })
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        def executar():
            self.log(f"Iniciando comparacao de arquivos...")
            self.log(f"Arquivo 1: {arquivo1}")
            self.log(f"Arquivo 2: {arquivo2}")
            self.log(f"Saida: {saida}")
            
            comparacao = self.module_loader.load('comparacao_modulo')
            stats = comparacao.executar_comparacao(arquivo1, arquivo2, saida)
            
            self.log(f"Total de nomes em arquivo 1: {stats['total_arquivo1']}")
            self.log(f"Total de nomes em arquivo 2: {stats['total_arquivo2']}")
            self.log(f"Nomes em comum: {stats['em_comum']}")
            self.log(f"Nomes apenas em arquivo 1: {stats['apenas_em_1']}")
            self.log(f"Nomes apenas em arquivo 2: {stats['apenas_em_2']}")
            self.log("Comparacao concluida com sucesso!")
            self.status_bar.set_success("Comparacao concluida")
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", f"Relatorio salvo em:\n{saida}"))
        
        self._executar_em_thread(executar, "comparacao")
    
    def executar_marcar_usuarios(self) -> None:
        arquivo = self.marcar_arquivo_var.get()
        meses_str = self.marcar_meses_var.get()
        
        validacao, msg = Validators.validar_campos({
            "Arquivo Excel": arquivo,
            "Meses": meses_str
        })
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_inteiro_positivo(meses_str, "Meses")
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        validacao, msg = Validators.validar_arquivo_existe(arquivo)
        if not validacao:
            messagebox.showerror("Erro", msg)
            return
        
        def executar():
            self.log(f"Iniciando marcacao de usuarios...")
            self.log(f"Arquivo: {arquivo}")
            self.log(f"Meses: {meses_str}")
            
            marcar = self.module_loader.load('marcar_usuarios_modulo')
            sucesso, mensagem, *extra = marcar.executar_marcar_usuarios(
                arquivo, int(meses_str), callback=self.log
            )
            
            if sucesso:
                self.log(mensagem)
                self.log("Marcacao de usuarios concluida com sucesso!")
                self.status_bar.set_success("Marcacao concluida")
                arquivo_saida = extra[0] if extra else arquivo
                self.root.after(0, lambda: messagebox.showinfo("Sucesso", f"Usuarios marcados em:\n{arquivo_saida}"))
            else:
                raise Exception(mensagem)
        
        self._executar_em_thread(executar, "marcacao de usuarios")
