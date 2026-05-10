# Guia de Desenvolvimento

Instruções para contribuidores que desejam estender ou modificar a aplicação.

## Arquitetura

### Estrutura de Camadas

```
UI Layer (tkinter)
    ↓
Core Layer (validação, arquivo, módulos)
    ↓
Modules Layer (lógica de negócio)
    ↓
External (pandas, PIL, etc)
```

### Componentes Principais

1. **config.py**: Configurações centralizadas
2. **ui/**: Interface gráfica (widgets, tabs, main_window)
3. **core/**: Lógica central (validators, file_handler, module_loader)
4. **modules/**: Módulos de processamento específicos

## Adicionando um Novo Módulo

### 1. Criar Estrutura de Diretórios

```bash
mkdir -p src/modules/novo_modulo
touch src/modules/novo_modulo/__init__.py
touch src/modules/novo_modulo/novo_modulo.py
```

### 2. Implementar o Módulo

**src/modules/novo_modulo/novo_modulo.py:**

```python
def executar_novo_modulo(arquivo_entrada: str, callback=None) -> tuple:
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    try:
        log("Iniciando novo módulo...")
        # Sua lógica aqui
        return True, "Sucesso!", {}
    except Exception as e:
        return False, f"Erro: {e}", {}
```

### 3. Adicionar Configuração

**src/config.py:**

```python
MODULES_CONFIG = {
    # ... módulos existentes ...
    'novo_modulo': {
        'name': 'Nome do Novo Módulo',
        'icon': '🎯',
        'description': 'Descrição do módulo',
        'module_name': 'novo_modulo'
    }
}
```

### 4. Adicionar Aba na UI

**src/ui/main_window.py:**

```python
def _criar_aba_novo_modulo(self) -> None:
    config = Config.MODULES_CONFIG['novo_modulo']
    
    fields = {
        'arquivo': {
            'type': 'file',
            'label': 'Arquivo de entrada:',
            'browse_command': lambda: self._selecionar_arquivo(
                'Selecionar arquivo',
                Config.FILE_TYPES['excel']
            )
        }
    }
    
    tab = TabFactory.create_simple_tab(
        self.notebook,
        f"{config['icon']} {config['name']}",
        config['description'],
        fields,
        self.executar_novo_modulo,
        "▶️ Executar"
    )
    
    self.novo_modulo_fields = tab.field_widgets

def _criar_abas(self) -> None:
    # ... abas existentes ...
    self._criar_aba_novo_modulo()

def executar_novo_modulo(self) -> None:
    if self.executando:
        messagebox.showwarning("Aviso", "Já existe uma execução em andamento")
        return
    
    arquivo = self.novo_modulo_fields['arquivo'].get()
    
    validacao, msg = Validators.validar_arquivo_existe(arquivo)
    if not validacao:
        messagebox.showerror("Erro", msg)
        return
    
    def executar():
        try:
            self.executando = True
            self.status_bar.set_running("Executando novo módulo...")
            self.log(f"Arquivo: {arquivo}")
            
            novo_modulo = self.module_loader.load('novo_modulo')
            sucesso, mensagem, _ = novo_modulo.executar_novo_modulo(
                arquivo, callback=self.log
            )
            
            if sucesso:
                self.log(mensagem)
                self.log("✓ Concluído com sucesso!")
                self.status_bar.set_success("Concluído")
                messagebox.showinfo("Sucesso", mensagem)
            else:
                self.log(f"✗ Erro: {mensagem}")
                self.status_bar.set_error("Erro")
                messagebox.showerror("Erro", mensagem)
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            self.status_bar.set_error("Erro")
            messagebox.showerror("Erro", f"Erro ao executar:\n{str(e)}")
        finally:
            self.executando = False
            self.status_bar.set_ready()
    
    thread = threading.Thread(target=executar, daemon=True)
    thread.start()
```

### 5. Atualizar build.py

**scripts/build.py:**

```python
f'--add-data={SRC_DIR / "modules" / "novo_modulo"}:src/modules/novo_modulo',
'--hidden-import=novo_modulo',
```

## Adicionando um Novo Widget

**src/ui/widgets.py:**

```python
class MeuWidget(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # Implementar widget
    
    def get(self):
        # Retornar valor
        pass
    
    def set(self, value):
        # Definir valor
        pass
```

## Adicionando Validação

**src/core/validators.py:**

```python
@staticmethod
def validar_email(email: str) -> Tuple[bool, str]:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    return False, "Email inválido"
```

## Padrões de Código

### Type Hints

```python
from typing import Dict, List, Tuple, Optional

def funcao(param1: str, param2: int) -> Tuple[bool, str]:
    return True, "sucesso"
```

### Tratamento de Erros

```python
try:
    # código
except ValueError as e:
    self.log(f"Erro de validação: {e}")
except Exception as e:
    self.log(f"Erro inesperado: {e}")
```

### Logging

```python
def log(msg: str) -> None:
    self.log_frame.append(msg)
```

## Testes

### Estrutura de Testes

```bash
mkdir -p tests
touch tests/__init__.py
touch tests/test_validators.py
```

### Exemplo de Teste

**tests/test_validators.py:**

```python
import pytest
from src.core.validators import Validators

def test_validar_inteiro_positivo():
    sucesso, msg = Validators.validar_inteiro_positivo("5")
    assert sucesso is True
    
    sucesso, msg = Validators.validar_inteiro_positivo("-5")
    assert sucesso is False
```

### Executar Testes

```bash
pytest
```

## Formatação de Código

### Black

```bash
black src/
```

### Flake8

```bash
flake8 src/
```

### MyPy

```bash
mypy src/
```

## Documentação

Adicione docstrings em todas as funções:

```python
def minha_funcao(param1: str) -> str:
    """
    Descrição breve da função.
    
    Args:
        param1: Descrição do parâmetro
    
    Returns:
        Descrição do retorno
    
    Raises:
        ValueError: Quando algo está inválido
    """
    pass
```

## Debugging

### Modo Debug

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Mensagem de debug")
```

### Breakpoints

```python
import pdb
pdb.set_trace()
```

## Performance

### Profiling

```python
import cProfile
cProfile.run('minha_funcao()')
```

### Memory Profiling

```bash
pip install memory-profiler
python -m memory_profiler script.py
```

## Checklist para Contribuições

- [ ] Código segue o padrão PEP 8
- [ ] Type hints adicionados
- [ ] Testes escritos e passando
- [ ] Documentação atualizada
- [ ] Sem imports não utilizados
- [ ] Sem hardcoding de valores
- [ ] Tratamento de erros apropriado
- [ ] Log de execução claro

## Recursos Úteis

- [Python Docs](https://docs.python.org/3/)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints](https://docs.python.org/3/library/typing.html)
