#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo adaptado do organizador de rifa para aceitar parâmetros externos
"""

import pandas as pd
import numpy as np
import os


def detectar_dados_numericos(df):
    """
    Detecta e extrai apenas os dados numéricos da matriz, ignorando cabeçalhos de texto.
    """
    dados_numericos = []
    
    # Verificar se os cabeçalhos são numéricos
    cabecalhos_numericos = []
    for col in df.columns:
        try:
            num = float(col)
            if num.is_integer():
                cabecalhos_numericos.append(int(num))
            else:
                cabecalhos_numericos.append(num)
        except (ValueError, TypeError):
            pass
    
    # Se temos cabeçalhos numéricos, incluí-los
    if cabecalhos_numericos and len(cabecalhos_numericos) == len(df.columns):
        dados_numericos.append(cabecalhos_numericos)
    
    # Processar cada linha do DataFrame
    for _, linha in df.iterrows():
        linha_numerica = []
        for valor in linha:
            try:
                num = float(valor)
                if num.is_integer():
                    linha_numerica.append(int(num))
                else:
                    linha_numerica.append(num)
            except (ValueError, TypeError):
                continue
        
        if linha_numerica and len(linha_numerica) == len(df.columns):
            dados_numericos.append(linha_numerica)
    
    return np.array(dados_numericos)


def reorganizar_dados_em_blocos(arquivo_entrada, arquivo_saida, tamanho_bloco=5, callback=None):
    """
    Reorganiza dados de qualquer arquivo Excel em uma única coluna seguindo o padrão de blocos.
    
    Args:
        arquivo_entrada (str): Caminho para o arquivo Excel de entrada
        arquivo_saida (str): Caminho para o arquivo Excel de saída
        tamanho_bloco (int): Número de elementos por bloco (padrão: 5)
        callback (callable): Função para reportar progresso (recebe mensagem string)
    
    Returns:
        tuple: (sucesso: bool, mensagem: str, dados_reorganizados: list)
    """
    
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    try:
        # Verificar se o arquivo de entrada existe
        if not os.path.exists(arquivo_entrada):
            return False, f"Arquivo não encontrado: {arquivo_entrada}", []
        
        log(f"📂 Carregando arquivo: {arquivo_entrada}")
        
        # Carregar o arquivo Excel
        df = pd.read_excel(arquivo_entrada)
        
        log(f"📊 DataFrame original: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Detectar e extrair apenas dados numéricos
        matriz_numerica = detectar_dados_numericos(df)
        
        if matriz_numerica.size == 0:
            return False, "Nenhum dado numérico encontrado no arquivo!", []
        
        log(f"🔢 Matriz numérica detectada: {matriz_numerica.shape[0]} linhas x {matriz_numerica.shape[1]} colunas")
        
        # Lista para armazenar os dados reorganizados
        dados_reorganizados = []
        
        # Número total de linhas e colunas
        num_linhas, num_colunas = matriz_numerica.shape
        
        # Calcular quantos blocos completos temos
        num_blocos = (num_linhas + tamanho_bloco - 1) // tamanho_bloco
        
        log(f"⚙️  Processando {num_blocos} blocos de {tamanho_bloco} elementos cada")
        
        # Para cada bloco
        for bloco in range(num_blocos):
            inicio_linha = bloco * tamanho_bloco
            fim_linha = min(inicio_linha + tamanho_bloco, num_linhas)
            
            # Para cada coluna
            for coluna in range(num_colunas):
                # Pegar o bloco da coluna atual
                bloco_dados = matriz_numerica[inicio_linha:fim_linha, coluna]
                dados_reorganizados.extend(bloco_dados)
            
            if callback and bloco % 10 == 0:
                progresso = (bloco + 1) / num_blocos * 100
                log(f"Progresso: {progresso:.1f}%")
        
        log(f"✅ Total de elementos reorganizados: {len(dados_reorganizados)}")
        
        # Criar DataFrame com os dados reorganizados
        df_resultado = pd.DataFrame(dados_reorganizados, columns=['Números'])
        
        # Salvar o arquivo
        df_resultado.to_excel(arquivo_saida, index=False)
        log(f"💾 Arquivo salvo como: {arquivo_saida}")
        
        return True, f"Sucesso! {len(dados_reorganizados)} elementos reorganizados", dados_reorganizados
        
    except Exception as e:
        return False, f"Erro durante o processamento: {e}", []


if __name__ == "__main__":
    # Teste standalone
    print("Módulo de Rifa - Teste")
    resultado = reorganizar_dados_em_blocos(
        "teste.xlsx",
        "saida.xlsx",
        tamanho_bloco=5
    )
    print(f"Resultado: {resultado[0]}, Mensagem: {resultado[1]}")
