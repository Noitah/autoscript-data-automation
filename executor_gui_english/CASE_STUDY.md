# Case Study: AutoScript - Plataforma de Automação de Processos

## 1. Visão Geral do Projeto

O **AutoScript** é uma aplicação desktop desenvolvida em Python com interface gráfica (GUI) que centraliza e executa múltiplos scripts de automação de dados. O projeto foi criado para resolver o problema de processos manuais repetitivos em rotinas administrativas e financeiras, transformando tarefas que levavam horas em execuções de poucos segundos.

**Autor:** João Victor Cotrim
**Tecnologias:** Python, Tkinter, Pandas, OpenPyXL, PyMuPDF (fitz), PyInstaller
**Tamanho do Projeto:** ~2.500 linhas de código modularizado

## 2. O Desafio

Muitas empresas lidam com volumes massivos de dados espalhados entre planilhas Excel e documentos PDF. O processamento manual desses dados apresenta três problemas principais:
1. **Tempo excessivo:** Tarefas como conciliação financeira e extração de dados de PDFs consumiam horas de trabalho diário.
2. **Alta taxa de erro:** A digitação e comparação manual de milhares de registros inevitavelmente gerava erros humanos.
3. **Falta de padronização:** Diferentes colaboradores executavam as tarefas de maneiras distintas.

## 3. A Solução Desenvolvida

Desenvolvi uma aplicação desktop robusta com uma arquitetura modular que permite a execução de diferentes rotinas de automação através de uma interface amigável.

### Arquitetura do Sistema
O projeto foi estruturado seguindo boas práticas de engenharia de software:
- **Separação de Responsabilidades (MVC-like):** Interface gráfica (`ui/`), lógica de negócios (`core/`) e scripts específicos (`modules/`) estão isolados.
- **Carregamento Dinâmico:** Os módulos são carregados dinamicamente via `ModuleLoader`, permitindo adicionar novas automações sem alterar o código principal.
- **Validação Centralizada:** Um sistema de validação (`Validators`) garante que todos os inputs (arquivos, pastas, parâmetros) estejam corretos antes da execução.

### Módulos de Automação Implementados

1. **Conciliação Financeira:** 
   - Lê milhares de registros de um arquivo Excel e compara com valores extraídos de nomes de arquivos PDF.
   - Gera um relatório automatizado destacando divergências e aplicando formatação condicional (cores) para fácil visualização.

2. **Processamento e Extração de Pedidos (PDF/Excel):**
   - Lê linhas de pedidos em Excel e busca correspondências em PDFs de centenas de páginas.
   - Extrai páginas específicas, calcula valores totais e gera novos PDFs individualizados por pedido.

3. **Organizador de Dados (Rifa):**
   - Reorganiza dados complexos de planilhas Excel em uma estrutura de coluna única baseada em blocos, facilitando a importação para outros sistemas.

4. **Comparação de Arquivos:**
   - Analisa dois arquivos de texto/dados distintos e gera um relatório detalhado mostrando itens em comum e itens exclusivos de cada arquivo.

## 4. Resultados e Impacto

A implementação desta ferramenta gerou resultados significativos:

- **Redução de Tempo:** Processos de conciliação que levavam horas agora são executados em menos de 1 minuto.
- **Precisão de 100%:** Eliminação completa de erros de digitação e comparação manual.
- **Acessibilidade:** A interface gráfica intuitiva permitiu que usuários sem conhecimento técnico (programação) pudessem executar scripts complexos de Python.
- **Distribuição Facilitada:** O projeto foi empacotado como um executável standalone (`.exe`) usando PyInstaller, não exigindo a instalação do Python nas máquinas dos usuários finais.

## 5. Habilidades Demonstradas

Este projeto demonstra minha capacidade de:
- Desenvolver soluções completas de ponta a ponta (do backend à interface do usuário).
- Trabalhar com bibliotecas avançadas de manipulação de dados (Pandas) e documentos (PyMuPDF).
- Aplicar conceitos de Clean Code, Type Hints e modularização em Python.
- Entender problemas de negócios reais e traduzi-los em soluções de software eficientes.
