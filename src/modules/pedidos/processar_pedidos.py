#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo adaptado de processamento de pedidos para aceitar parâmetros externos
Versão simplificada para GUI
"""

import openpyxl
import fitz  # PyMuPDF
from datetime import datetime
from collections import defaultdict, Counter
import os
import re
import time


def ler_pedidos_excel_por_linha(caminho_excel):
    """Le o Excel e retorna uma lista onde cada item representa UMA LINHA"""
    workbook = openpyxl.load_workbook(caminho_excel)
    sheet = workbook.active
    
    linhas_pedidos = []
    
    for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        if row[0] is None:
            continue
        
        # Converter data para formato YYYY-MM-DD
        if isinstance(row[0], datetime):
            data = row[0].strftime('%Y-%m-%d')
        elif isinstance(row[0], str):
            try:
                if '/' in row[0]:
                    data_obj = datetime.strptime(row[0], '%d/%m/%Y')
                    data = data_obj.strftime('%Y-%m-%d')
                elif '-' in row[0] and row[0].count('-') == 2:
                    partes = row[0].split('-')
                    if len(partes[0]) == 2:
                        data_obj = datetime.strptime(row[0], '%d-%m-%Y')
                        data = data_obj.strftime('%Y-%m-%d')
                    else:
                        data = row[0]
                else:
                    data = str(row[0]).replace('/', '-')
            except:
                data = str(row[0]).replace('/', '-').replace('\\', '-')
        else:
            data = str(row[0]).replace('/', '-').replace('\\', '-')
        
        # Coletar pedidos
        pedidos_linha = []
        for i in range(1, len(row)):
            if row[i] is not None and row[i] != '':
                numero = str(int(float(row[i]))) if isinstance(row[i], float) else str(row[i])
                pedidos_linha.append(numero)
        
        if pedidos_linha:
            linhas_pedidos.append({
                'data': data,
                'linha': idx,
                'pedidos': pedidos_linha
            })
    
    workbook.close()
    return linhas_pedidos


def extrair_valor_total_pagina(texto):
    """Extrai o valor TOTAL da pagina"""
    if 'TOTAL:' not in texto:
        return None
    
    valores_encontrados = []
    linhas = texto.split('\n')
    
    for linha in linhas:
        linha = linha.strip()
        match = re.match(r'^([\d,.]+)$', linha)
        if match:
            valor_str = match.group(1)
            
            if ',' in valor_str and '.' in valor_str:
                valor_str = valor_str.replace(',', '')
            elif ',' in valor_str and '.' not in valor_str:
                valor_str = valor_str.replace(',', '.')
            
            try:
                valor = float(valor_str)
                if 1.0 <= valor <= 1000000:
                    valores_encontrados.append(valor)
            except:
                continue
    
    if not valores_encontrados:
        return None
    
    contagem = Counter(valores_encontrados)
    valor_mais_comum = contagem.most_common(1)[0][0]
    
    return valor_mais_comum


def buscar_pedidos_e_valores(caminho_pdf, todos_numeros_pedidos, callback=None):
    """Busca pedidos e extrai valores totais de cada pagina"""
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    log("Buscando pedidos e extraindo valores...")
    
    paginas_por_pedido = defaultdict(list)
    valores_por_pagina = {}
    tempo_inicio = time.time()
    
    padroes = {numero: re.compile(r'\b' + re.escape(numero) + r'\b') 
               for numero in todos_numeros_pedidos}
    
    try:
        pdf_doc = fitz.open(caminho_pdf)
        total_paginas = len(pdf_doc)
        
        log(f"Total de páginas: {total_paginas}")
        log(f"Pedidos a buscar: {len(todos_numeros_pedidos)}")
        
        for num_pagina in range(total_paginas):
            if (num_pagina + 1) % 100 == 0:
                tempo_decorrido = time.time() - tempo_inicio
                pag_seg = (num_pagina + 1) / tempo_decorrido if tempo_decorrido > 0 else 0
                progresso = (num_pagina + 1) / total_paginas * 100
                log(f"Progresso: {progresso:.1f}% ({num_pagina + 1}/{total_paginas}) - {pag_seg:.0f} pág/seg")
            
            try:
                pagina = pdf_doc[num_pagina]
                texto = pagina.get_text()
                
                if texto:
                    for numero, padrao in padroes.items():
                        if padrao.search(texto):
                            paginas_por_pedido[numero].append(num_pagina)
                    
                    valor = extrair_valor_total_pagina(texto)
                    if valor is not None:
                        valores_por_pagina[num_pagina] = valor
            except:
                continue
        
        pdf_doc.close()
        tempo_total = time.time() - tempo_inicio
        log(f"✅ Concluído em {tempo_total:.1f} segundos!")
        log(f"Valores extraídos de {len(valores_por_pagina)} páginas")
        
    except Exception as e:
        log(f"❌ Erro: {e}")
        return {}, {}
    
    return dict(paginas_por_pedido), valores_por_pagina


def criar_pagina_total(valor_total):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'PaginaFinal.pdf')
    
    if not os.path.exists(template_path):
        pdf = fitz.open()
        pagina = pdf.new_page(width=595, height=841)
        valor_formatado = f"{valor_total:,.2f}"
        pagina.insert_text((420, 90), "Total Geral:", fontsize=12, fontname="helv")
        pagina.insert_text((520, 90), valor_formatado, fontsize=12, fontname="helv")
        return pdf
    
    template = fitz.open(template_path)
    pdf_novo = fitz.open()
    pdf_novo.insert_pdf(template)
    template.close()
    
    pagina = pdf_novo[0]
    
    valor_formatado = f"{valor_total:,.2f}"
    
    texto = pagina.get_text("dict")
    
    for bloco in texto["blocks"]:
        if "lines" in bloco:
            for linha in bloco["lines"]:
                for span in linha["spans"]:
                    texto_span = span["text"].strip()
                    if re.match(r'^[\d,.]+$', texto_span) and len(texto_span) > 3:
                        bbox = span["bbox"]
                        rect = fitz.Rect(bbox)
                        rect.x0 -= 2
                        rect.y0 -= 2
                        rect.x1 += 2
                        rect.y1 += 2
                        pagina.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                        
                        pagina.insert_text(
                            (bbox[0] - 6, bbox[3] - 3),
                            valor_formatado,
                            fontsize=span["size"],
                            fontname="hebo"
                        )
                        break
    
    return pdf_novo


def criar_pdfs_com_valores(caminho_pdf, linhas_pedidos, paginas_por_pedido, 
                          valores_por_pagina, diretorio='output', callback=None):
    """Cria PDFs individuais com valores"""
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    
    log("Criando PDFs com valores...")
    
    pdf_original = fitz.open(caminho_pdf)
    pedidos_nao_encontrados = []
    datas_sem_pedidos = []
    pdfs_criados = 0
    
    total_linhas = len(linhas_pedidos)
    
    for idx, item in enumerate(linhas_pedidos, 1):
        data = item['data']
        linha_excel = item['linha']
        pedidos = item['pedidos']
        
        if idx % 5 == 0:
            progresso = idx / total_linhas * 100
            log(f"Processando: {progresso:.1f}% ({idx}/{total_linhas})")
        
        paginas_unicas = set()
        valor_total = 0.0
        pedidos_nao_encontrados_nesta_linha = []
        
        for numero in pedidos:
            if numero in paginas_por_pedido:
                paginas = paginas_por_pedido[numero]
                paginas_unicas.update(paginas)
                
                for pag in paginas:
                    if pag in valores_por_pagina:
                        valor_total += valores_por_pagina[pag]
            else:
                pedidos_nao_encontrados_nesta_linha.append(numero)
        
        if pedidos_nao_encontrados_nesta_linha:
            pedidos_nao_encontrados.append({
                'data': data,
                'linha': linha_excel,
                'pedidos': pedidos_nao_encontrados_nesta_linha
            })
        
        if paginas_unicas:
            pdf_novo = fitz.open()
            
            for pag in sorted(paginas_unicas):
                pdf_novo.insert_pdf(pdf_original, from_page=pag, to_page=pag)
            
            pdf_total = criar_pagina_total(valor_total)
            pdf_novo.insert_pdf(pdf_total)
            pdf_total.close()
            
            partes_data = data.split('-')
            dia = partes_data[2] if len(partes_data) == 3 else '01'
            mes = partes_data[1] if len(partes_data) == 3 else '01'
            
            valor_formatado = f"{valor_total:.2f}".replace('.', ',')
            nome_base = f"{mes} {dia} {valor_formatado}.pdf"
            
            nome_arquivo_final = nome_base
            arquivo = os.path.join(diretorio, nome_base)
            
            if os.path.exists(arquivo):
                nome, extensao = os.path.splitext(nome_base)
                contador = 2
                while True:
                    nome_arquivo_final = f"{nome} {contador}{extensao}"
                    arquivo = os.path.join(diretorio, nome_arquivo_final)
                    if not os.path.exists(arquivo):
                        break
                    contador += 1
            
            pdf_novo.save(arquivo)
            pdf_novo.close()
            pdfs_criados += 1
        else:
            datas_sem_pedidos.append({
                'data': data,
                'linha': linha_excel,
                'pedidos': pedidos
            })
    
    pdf_original.close()
    log(f"✅ {pdfs_criados} PDFs criados com sucesso!")
    
    return pedidos_nao_encontrados, datas_sem_pedidos


def executar_processamento_pedidos(caminho_excel, caminho_pdf, pasta_saida='output', callback=None):
    """
    Executa o processamento completo de pedidos
    
    Args:
        caminho_excel: Caminho para o arquivo Excel com pedidos
        caminho_pdf: Caminho para o PDF fonte
        pasta_saida: Pasta onde salvar os PDFs gerados
        callback: Função para reportar progresso
    
    Returns:
        tuple: (sucesso: bool, mensagem: str, estatisticas: dict)
    """
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    try:
        log('=== Iniciando processamento de pedidos ===')
        
        # Validar arquivos
        if not os.path.exists(caminho_excel):
            return False, f"Arquivo Excel não encontrado: {caminho_excel}", {}
        
        if not os.path.exists(caminho_pdf):
            return False, f"Arquivo PDF não encontrado: {caminho_pdf}", {}
        
        # Ler pedidos do Excel
        log("Lendo pedidos do Excel...")
        linhas_pedidos = ler_pedidos_excel_por_linha(caminho_excel)
        
        if not linhas_pedidos:
            return False, "Nenhum pedido encontrado no Excel", {}
        
        todos_pedidos = set()
        for linha in linhas_pedidos:
            todos_pedidos.update(linha['pedidos'])
        
        log(f"✅ {len(linhas_pedidos)} linhas com {len(todos_pedidos)} pedidos únicos")
        
        # Buscar pedidos no PDF
        paginas_por_pedido, valores_por_pagina = buscar_pedidos_e_valores(
            caminho_pdf, list(todos_pedidos), callback
        )
        
        # Criar PDFs
        pedidos_nao_encontrados, datas_sem_pedidos = criar_pdfs_com_valores(
            caminho_pdf, linhas_pedidos, paginas_por_pedido, 
            valores_por_pagina, pasta_saida, callback
        )
        
        # Log das estatísticas detalhadas
        log(f"Pedidos não encontrados: {len(pedidos_nao_encontrados)}")
        log(f"Datas sem pedidos: {len(datas_sem_pedidos)}")
        if pedidos_nao_encontrados:
            log("Lista de pedidos não encontrados:")
            for item in pedidos_nao_encontrados:
                log(f"  Data: {item['data']} | Linha: {item['linha']} | Pedidos: {', '.join(item['pedidos'])}")
        else:
            log("Nenhum pedido ficou sem correspondência.")

        if datas_sem_pedidos:
            log("Lista de datas sem pedidos encontrados:")
            for item in datas_sem_pedidos:
                log(f"  Data: {item['data']} | Linha: {item['linha']} | Pedidos: {', '.join(item['pedidos'])}")
        else:
            log("Todas as datas tiveram pedidos correspondentes.")
        log('=== Processo concluído ===')
        
        # Estatísticas
        stats = {
            'linhas_processadas': len(linhas_pedidos),
            'pedidos_unicos': len(todos_pedidos),
            'pedidos_encontrados': len(paginas_por_pedido),
            'pedidos_nao_encontrados': len(pedidos_nao_encontrados),
            'datas_sem_pedidos': len(datas_sem_pedidos),
            # listas detalhadas para uso pela GUI
            'pedidos_nao_encontrados_lista': pedidos_nao_encontrados,
            'datas_sem_pedidos_lista': datas_sem_pedidos
        }
        
        mensagem = f"""✅ Processamento concluído!
📊 Estatísticas:
   - Linhas processadas: {stats['linhas_processadas']}
   - Pedidos únicos: {stats['pedidos_unicos']}
   - Pedidos encontrados: {stats['pedidos_encontrados']}
   - Pedidos não encontrados: {stats['pedidos_nao_encontrados']}
   - Datas sem pedidos: {stats['datas_sem_pedidos']}
📁 Pasta de saída: {os.path.abspath(pasta_saida)}"""
        
        return True, mensagem, stats
        
    except Exception as e:
        return False, f"Erro crítico: {e}", {}


if __name__ == "__main__":
    print("Módulo de Pedidos - Teste")
