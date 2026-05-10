#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair páginas específicas de um PDF baseado em números de pedidos do Excel.
Utiliza PyMuPDF (fitz) para melhor desempenho.

Versão: 9.0
Data: 31/10/2025

Mudanças v9.0:
- Suporte a pedidos com múltiplas páginas
- Continua pegando páginas até encontrar novo pedido ou marcadores de início
- Detecta: Nome:, CNPJ/CPF:, Número do Pedido:, Status do Pedido:
- Mantém todas as otimizações da v8.0
"""

import os
import sys
import pandas as pd
import fitz  # PyMuPDF
import re
from pathlib import Path
from collections import Counter
import time


def ler_pedidos_excel_por_linha(caminho_excel):
    """Lê o arquivo Excel e extrai os números de pedidos organizados por linha."""
    print(f"Lendo arquivo Excel: {caminho_excel}")
    
    df = pd.read_excel(caminho_excel)
    
    linhas_info = []
    todos_pedidos = set()
    tamanhos = []
    
    for idx, row in df.iterrows():
        linha_num = idx + 1
        data = str(row.iloc[0]) if pd.notna(row.iloc[0]) else f"Linha{linha_num}"
        
        pedidos_linha = []
        for valor in row.iloc[1:]:
            if pd.notna(valor):
                if isinstance(valor, (int, float)):
                    pedido = str(int(valor))
                else:
                    pedido = str(valor).strip()
                
                if pedido and pedido != 'nan':
                    pedidos_linha.append(pedido)
                    todos_pedidos.add(pedido)
                    tamanhos.append(len(pedido))
        
        if pedidos_linha:
            linhas_info.append({
                'numero': linha_num,
                'data': data,
                'pedidos': pedidos_linha
            })
    
    if tamanhos:
        contador_tamanhos = Counter(tamanhos)
        tamanho_mais_comum = contador_tamanhos.most_common(1)[0][0]
        tamanhos_unicos = sorted(set(tamanhos))
        
        print(f"Total de linhas com pedidos: {len(linhas_info)}")
        print(f"Total de pedidos: {len(todos_pedidos)}")
        print(f"Tamanhos detectados: {tamanhos_unicos}")
        print(f"Tamanho mais comum: {tamanho_mais_comum} dígitos")
        print()
        
        for linha in linhas_info:
            print(f"  Linha {linha['numero']} ({linha['data']}): {len(linha['pedidos'])} pedidos - {linha['pedidos']}")
    else:
        tamanho_mais_comum = 7
    
    return linhas_info, tamanho_mais_comum, list(todos_pedidos)


def criar_cache_output(pasta_output, tamanho_esperado):
    """Lê TODOS os PDFs da pasta output UMA VEZ e cria um cache."""
    print(f"\n{'='*60}")
    print("CRIANDO CACHE DA PASTA OUTPUT")
    print(f"{'='*60}")
    
    if not os.path.exists(pasta_output):
        print(f"Pasta output não encontrada: {pasta_output}")
        return {}
    
    arquivos = [f for f in os.listdir(pasta_output) if f.endswith('.pdf')]
    
    if not arquivos:
        print("Nenhum arquivo PDF encontrado na pasta output")
        return {}
    
    print(f"Lendo {len(arquivos)} arquivos da pasta output...")
    
    cache = {}
    tamanho_min = max(5, tamanho_esperado - 2)
    tamanho_max = min(10, tamanho_esperado + 2)
    padrao = f'\\d{{{tamanho_min},{tamanho_max}}}'
    
    inicio = time.time()
    
    for i, arquivo in enumerate(arquivos, 1):
        caminho_completo = os.path.join(pasta_output, arquivo)
        pedidos_encontrados = set()
        
        try:
            doc = fitz.open(caminho_completo)
            
            for pagina in doc:
                texto = pagina.get_text()
                linhas = texto.split('\n')
                
                for linha in linhas:
                    matches = re.findall(padrao, linha)
                    for match in matches:
                        if len(match) == tamanho_esperado:
                            pedidos_encontrados.add(match)
            
            doc.close()
            cache[arquivo] = pedidos_encontrados
            
            if pedidos_encontrados:
                print(f"  [{i}/{len(arquivos)}] {arquivo}: {len(pedidos_encontrados)} pedidos")
            else:
                print(f"  [{i}/{len(arquivos)}] {arquivo}: nenhum pedido encontrado")
                
        except Exception as e:
            print(f"  [{i}/{len(arquivos)}] {arquivo}: ERRO - {e}")
            cache[arquivo] = set()
    
    tempo_total = time.time() - inicio
    print(f"\n✓ Cache criado em {tempo_total:.2f}s")
    print(f"Total de arquivos no cache: {len(cache)}")
    print(f"{'='*60}\n")
    
    return cache


def buscar_arquivo_output_com_cache(pedidos_linha, cache_output):
    """Busca o arquivo correspondente usando o cache (MUITO RÁPIDO)."""
    if not cache_output:
        return None
    
    pedidos_linha_set = set(pedidos_linha)
    
    melhor_match = None
    maior_interseccao = 0
    
    for arquivo, pedidos_pdf in cache_output.items():
        interseccao = len(pedidos_linha_set.intersection(pedidos_pdf))
        
        if interseccao == len(pedidos_linha) and interseccao > maior_interseccao:
            melhor_match = arquivo
            maior_interseccao = interseccao
    
    if melhor_match:
        return os.path.splitext(melhor_match)[0]
    else:
        return None


def eh_inicio_de_novo_pedido(texto):
    """
    Verifica se a página é o início de um novo pedido.
    Retorna True se encontrar os marcadores de início.
    """
    # Marcadores que indicam início de novo pedido
    marcadores = [
        r'Nome\s*:',
        r'CNPJ/CPF\s*:',
        r'N[uú]mero\s+do\s+Pedido\s*:',
        r'Status\s+do\s+Pedido\s*:'
    ]
    
    for marcador in marcadores:
        if re.search(marcador, texto, re.IGNORECASE):
            return True
    
    return False


def extrair_numero_pedido_da_pagina(texto, pedidos_procurados, tamanho_esperado):
    """Extrai o número do pedido de uma página do PDF."""
    tamanho_min = max(5, tamanho_esperado - 2)
    tamanho_max = min(10, tamanho_esperado + 2)
    padrao_tamanho = f'\\d{{{tamanho_min},{tamanho_max}}}'
    
    linhas = texto.split('\n')
    
    # ESTRATÉGIA 1: Busca próxima ao label "Número do Pedido"
    for i, linha in enumerate(linhas):
        if re.search(r'N[uú]mero\s+do\s+Pedido\s*:', linha, re.IGNORECASE) and \
           not re.search(r'Valor\s+do\s+Pedido', linha, re.IGNORECASE) and \
           not re.search(r'Status\s+do\s+Pedido', linha, re.IGNORECASE):
            
            for j in range(max(0, i - 10), i):
                linha_anterior = linhas[j].strip()
                match_numero = re.match(f'^({padrao_tamanho})$', linha_anterior)
                if match_numero:
                    numero = match_numero.group(1)
                    if numero in pedidos_procurados:
                        return numero
            
            for j in range(i + 1, min(i + 11, len(linhas))):
                proxima_linha = linhas[j].strip()
                match_numero = re.match(f'^({padrao_tamanho})$', proxima_linha)
                if match_numero:
                    numero = match_numero.group(1)
                    if numero in pedidos_procurados:
                        return numero
    
    # ESTRATÉGIA 2: Busca em todas as linhas
    for i, linha in enumerate(linhas):
        linha_limpa = linha.strip()
        match_numero = re.match(f'^({padrao_tamanho})$', linha_limpa)
        if match_numero:
            numero = match_numero.group(1)
            if len(numero) == tamanho_esperado and numero in pedidos_procurados:
                if i > 0:
                    return numero
            elif numero in pedidos_procurados:
                if i > 0:
                    return numero
    
    return None


def extrair_paginas_por_linha(caminho_pdf, linhas_info, tamanho_esperado, pasta_saida, cache_output):
    """
    Extrai páginas do PDF e agrupa por linha do Excel.
    Suporta pedidos com múltiplas páginas.
    """
    print(f"Processando PDF: {caminho_pdf}")
    print(f"Buscando números com {tamanho_esperado} dígitos (±2)")
    print(f"Suporte a pedidos com múltiplas páginas: ATIVADO")
    
    Path(pasta_saida).mkdir(parents=True, exist_ok=True)
    
    # Criar mapa de pedido -> linha
    pedido_para_linha = {}
    for linha in linhas_info:
        for pedido in linha['pedidos']:
            pedido_para_linha[pedido] = linha
    
    # Abrir o PDF
    documento = fitz.open(caminho_pdf)
    total_paginas = len(documento)
    
    print(f"Total de páginas no PDF: {total_paginas}")
    print(f"Procurando pedidos...\n")
    
    # Dicionário para armazenar páginas por linha
    paginas_por_linha = {linha['numero']: [] for linha in linhas_info}
    pedidos_encontrados = {}
    todos_pedidos = list(pedido_para_linha.keys())
    
    pedido_atual = None
    linha_atual = None
    
    # Percorrer cada página
    for num_pagina in range(total_paginas):
        pagina = documento[num_pagina]
        texto = pagina.get_text()
        
        # Verificar se é início de novo pedido
        eh_novo_pedido = eh_inicio_de_novo_pedido(texto)
        
        # Tentar extrair número do pedido
        numero_pedido = extrair_numero_pedido_da_pagina(texto, todos_pedidos, tamanho_esperado)
        
        if numero_pedido and numero_pedido in pedido_para_linha:
            # Encontrou um novo pedido
            pedido_atual = numero_pedido
            linha_atual = pedido_para_linha[numero_pedido]
            
            print(f"✓ Página {num_pagina + 1}: Pedido {numero_pedido} (Linha {linha_atual['numero']}) - INÍCIO")
            
            paginas_por_linha[linha_atual['numero']].append((num_pagina, numero_pedido))
            pedidos_encontrados[numero_pedido] = num_pagina + 1
            
        elif pedido_atual and not eh_novo_pedido:
            # Página de continuação do pedido atual
            print(f"  → Página {num_pagina + 1}: Continuação do pedido {pedido_atual}")
            paginas_por_linha[linha_atual['numero']].append((num_pagina, pedido_atual))
            
        elif eh_novo_pedido and not numero_pedido:
            # Início de novo pedido mas não está na lista
            pedido_atual = None
            linha_atual = None
            print(f"  ○ Página {num_pagina + 1}: Início de pedido não procurado")
        
        if (num_pagina + 1) % 100 == 0:
            print(f"Progresso: {num_pagina + 1}/{total_paginas} páginas processadas...")
    
    # Criar PDFs agrupados por linha
    print("\nCriando PDFs agrupados por linha...")
    
    for linha in linhas_info:
        linha_num = linha['numero']
        paginas = paginas_por_linha[linha_num]
        
        if paginas:
            # Criar PDF com todas as páginas desta linha
            pdf_saida = fitz.open()
            
            # Remover duplicatas mantendo ordem
            paginas_unicas = []
            paginas_vistas = set()
            for num_pag, num_ped in paginas:
                if num_pag not in paginas_vistas:
                    paginas_unicas.append((num_pag, num_ped))
                    paginas_vistas.add(num_pag)
            
            # Ordenar por número de página
            paginas_unicas.sort(key=lambda x: x[0])
            
            for num_pagina, num_pedido in paginas_unicas:
                pdf_saida.insert_pdf(documento, from_page=num_pagina, to_page=num_pagina)
            
            # Buscar nome usando cache
            nome_base = buscar_arquivo_output_com_cache(linha['pedidos'], cache_output)
            
            if nome_base:
                nome_arquivo = f"{nome_base} 2.pdf"
                print(f"  ✓ Linha {linha_num}: {len(paginas_unicas)} páginas → '{nome_arquivo}'")
            else:
                data_limpa = linha['data'].replace('/', '-').replace(':', '-')
                nome_arquivo = f"Linha_{linha_num}_{data_limpa}.pdf"
                print(f"  ✓ Linha {linha_num}: {len(paginas_unicas)} páginas → '{nome_arquivo}' (fallback)")
            
            arquivo_completo = os.path.join(pasta_saida, nome_arquivo)
            pdf_saida.save(arquivo_completo)
            pdf_saida.close()
        else:
            print(f"  ✗ Linha {linha_num}: Nenhuma página encontrada")
    
    documento.close()

    # Relatório final
    print("\n" + "="*60)
    print("RELATÓRIO FINAL")
    print("="*60)
    print(f"Total de linhas processadas: {len(linhas_info)}")
    print(f"Total de pedidos procurados: {len(todos_pedidos)}")
    print(f"Pedidos encontrados: {len(pedidos_encontrados)}")

    pedidos_nao_encontrados = set(todos_pedidos) - set(pedidos_encontrados.keys())
    if pedidos_nao_encontrados:
        print(f"\nPedidos NÃO encontrados ({len(pedidos_nao_encontrados)}):")
        for pedido in sorted(pedidos_nao_encontrados):
            linha = pedido_para_linha[pedido]
            print(f"  - Pedido {pedido} (Linha {linha['numero']})")

    # Datas (linhas) sem páginas encontradas
    datas_sem_pedidos = []
    for linha in linhas_info:
        if not paginas_por_linha.get(linha['numero']):
            datas_sem_pedidos.append({
                'numero': linha['numero'],
                'data': linha['data'],
                'pedidos': linha['pedidos']
            })

    print(f"\nArquivos salvos em: {os.path.abspath(pasta_saida)}")
    print("="*60)

    # Montar estatísticas para retorno
    stats = {
        'linhas_processadas': len(linhas_info),
        'pedidos_procurados': len(todos_pedidos),
        'pedidos_encontrados': len(pedidos_encontrados),
        'pedidos_nao_encontrados': len(pedidos_nao_encontrados),
        'datas_sem_pedidos': len(datas_sem_pedidos),
        'pedidos_nao_encontrados_lista': sorted(pedidos_nao_encontrados),
        'datas_sem_pedidos_lista': datas_sem_pedidos,
        'pasta_saida': os.path.abspath(pasta_saida)
    }

    return stats


def main(caminho_excel=None, caminho_pdf=None, pasta_output='output'):
    """Função principal do script."""
    print("="*60)
    print("EXTRATOR DE PÁGINAS DE PEDIDOS - v9.0")
    print("Com suporte a pedidos com múltiplas páginas")
    print("="*60)
    
    if caminho_excel is None or caminho_pdf is None:
        if len(sys.argv) < 3:
            print("\nUso: python3 extrair_pedidos_v9.py <arquivo_excel> <arquivo_pdf> [pasta_output]")
            print("\nExemplo:")
            print("  python3 extrair_pedidos_v9.py NPedidos.xlsx Arquivo_Grande.pdf")
            print("  python3 extrair_pedidos_v9.py NPedidos.xlsx Arquivo_Grande.pdf output")
            print("\nNOVO: Suporta pedidos com múltiplas páginas!")
            sys.exit(1)
        
        caminho_excel = sys.argv[1]
        caminho_pdf = sys.argv[2]
        pasta_output = sys.argv[3] if len(sys.argv) > 3 else 'output'
    
    pasta_saida = pasta_output
    
    if not os.path.exists(caminho_excel):
        print(f"ERRO: Arquivo Excel não encontrado: {caminho_excel}")
        sys.exit(1)
    
    if not os.path.exists(caminho_pdf):
        print(f"ERRO: Arquivo PDF não encontrado: {caminho_pdf}")
        sys.exit(1)
    
    try:
        inicio_total = time.time()
        
        linhas_info, tamanho_esperado, todos_pedidos = ler_pedidos_excel_por_linha(caminho_excel)
        
        if not linhas_info:
            print("ERRO: Nenhuma linha com pedidos encontrada no Excel")
            sys.exit(1)
        
        cache_output = criar_cache_output(pasta_output, tamanho_esperado)
        
        stats = extrair_paginas_por_linha(caminho_pdf, linhas_info, tamanho_esperado, pasta_saida, cache_output)
        
        tempo_total = time.time() - inicio_total
        print(f"\n✓ Processo concluído com sucesso em {tempo_total:.2f}s!")
        
        # Propagar estatísticas quando chamada programaticamente
        return stats
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
