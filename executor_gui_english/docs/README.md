# AutoScript - Executor de Scripts v8.0

Interface gráfica para automação de processamento de dados com múltiplos módulos especializados.

## 📋 Características

- **Organizador de Rifa**: Reorganiza dados de arquivos Excel em uma única coluna seguindo padrão de blocos
- **Conciliação Financeira**: Compara valores entre arquivo Excel e nomes de arquivos PDF
- **Processamento de Pedidos**: Processa pedidos e gera PDFs individualizados
- **Extração Detalhada**: Extração avançada com suporte a múltiplas páginas
- **Comparação de Arquivos**: Compara dois arquivos Excel e gera relatório de diferenças
- **Marcação de Usuários**: Marca usuários com uso em período retroativo

## 🚀 Início Rápido

### Requisitos
- Python 3.8+
- pip ou conda

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

**Linux/macOS:**
```bash
bash scripts/run.sh
```

**Windows:**
```bash
scripts\run.bat
```

**Ou diretamente com Python:**
```bash
python -m src.main
```

## 📁 Estrutura do Projeto

```
executor_gui/
├── src/
│   ├── main.py                 # Ponto de entrada
│   ├── config.py               # Configurações centralizadas
│   ├── ui/                     # Interface gráfica
│   │   ├── main_window.py      # Janela principal
│   │   ├── tabs.py             # Criação de abas
│   │   └── widgets.py          # Componentes reutilizáveis
│   ├── core/                   # Lógica central
│   │   ├── validators.py       # Validação de dados
│   │   ├── file_handler.py     # Seleção/salvamento de arquivos
│   │   └── module_loader.py    # Carregamento dinâmico
│   └── modules/                # Módulos de processamento
│       ├── rifa/
│       ├── conciliacao/
│       ├── pedidos/
│       ├── comparacao/
│       └── marcar_usuarios/
├── assets/                     # Recursos (imagens, etc)
├── docs/                       # Documentação
├── scripts/                    # Scripts de build e execução
├── requirements.txt            # Dependências
└── pyproject.toml             # Configuração do projeto
```

## 🔧 Desenvolvimento

### Instalação de Dependências de Desenvolvimento

```bash
pip install -e ".[dev]"
```

### Executar Testes

```bash
pytest
```

### Formatação de Código

```bash
black src/
```

### Verificação de Tipos

```bash
mypy src/
```

## 📦 Compilação para Executável

### Instalação de Dependências de Build

```bash
pip install -e ".[build]"
```

### Compilar

```bash
python scripts/build.py
```

O executável será gerado em `dist/AutoScript.exe`

## 🎨 Melhorias Realizadas

### Organização
- ✅ Estrutura modular clara e bem definida
- ✅ Separação de responsabilidades
- ✅ Código reutilizável

### Qualidade
- ✅ Type hints em todo o código
- ✅ Validação robusta de dados
- ✅ Tratamento de erros melhorado
- ✅ Logging estruturado

### Manutenibilidade
- ✅ Redução de duplicação de código
- ✅ Métodos menores e mais focados
- ✅ Configuração centralizada
- ✅ Documentação clara

### Performance
- ✅ Cache de módulos otimizado
- ✅ Carregamento dinâmico eficiente
- ✅ Redução de tamanho do executável

## 📝 Notas de Versão

### v7.0.0 (Refatorada)
- Reorganização completa da estrutura do projeto
- Modularização do código principal
- Adição de type hints
- Melhoria na validação de dados
- Criação de componentes reutilizáveis
- Remoção de arquivos desnecessários (~140 MB)
- Novo sistema de configuração centralizado

## 📧 Suporte

Autor: João Victor Cotrim - joaocotrimprofi@gmail.com

## 📄 Licença

MIT License - Veja LICENSE para detalhes.
