#!/usr/bin/env python3

def executar_comparacao(arquivo1, arquivo2, arquivo_saida):
    try:
        with open(arquivo1, 'r', encoding='utf-8') as f1:
            conteudo1 = f1.read()
        
        with open(arquivo2, 'r', encoding='utf-8') as f2:
            conteudo2 = f2.read()
    except FileNotFoundError as e:
        raise Exception(f"Erro: {e}")

    nomes_1 = set(nome.strip() for nome in conteudo1.replace('\n', '').split(',') if nome.strip())
    nomes_2 = set(nome.strip() for nome in conteudo2.replace('\n', '').split(',') if nome.strip())

    apenas_em_1 = nomes_1 - nomes_2
    apenas_em_2 = nomes_2 - nomes_1
    em_ambos = nomes_1 & nomes_2

    relatorio = []
    relatorio.append("=" * 80)
    relatorio.append("RELATÓRIO DE COMPARAÇÃO")
    relatorio.append("=" * 80)
    relatorio.append("")

    relatorio.append(f"Total de nomes em {arquivo1}: {len(nomes_1)}")
    relatorio.append(f"Total de nomes em {arquivo2}: {len(nomes_2)}")
    relatorio.append(f"Nomes em comum: {len(em_ambos)}")
    relatorio.append("")

    relatorio.append("-" * 80)
    relatorio.append(f"APENAS EM {arquivo1} ({len(apenas_em_1)} nomes)")
    relatorio.append("-" * 80)
    if apenas_em_1:
        for nome in sorted(apenas_em_1):
            relatorio.append(f"  {nome}")
    else:
        relatorio.append("  (nenhum)")
    relatorio.append("")

    relatorio.append("-" * 80)
    relatorio.append(f"APENAS EM {arquivo2} ({len(apenas_em_2)} nomes)")
    relatorio.append("-" * 80)
    if apenas_em_2:
        for nome in sorted(apenas_em_2):
            relatorio.append(f"  {nome}")
    else:
        relatorio.append("  (nenhum)")
    relatorio.append("")

    relatorio.append("=" * 80)
    relatorio.append("RESUMO DAS DIFERENÇAS")
    relatorio.append("=" * 80)
    relatorio.append(f"Nomes removidos: {len(apenas_em_1)}")
    relatorio.append(f"Nomes adicionados: {len(apenas_em_2)}")
    relatorio.append(f"Total de mudanças: {len(apenas_em_1) + len(apenas_em_2)}")
    relatorio.append("")

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(relatorio))

    return {
        'total_arquivo1': len(nomes_1),
        'total_arquivo2': len(nomes_2),
        'em_comum': len(em_ambos),
        'apenas_em_1': len(apenas_em_1),
        'apenas_em_2': len(apenas_em_2)
    }
