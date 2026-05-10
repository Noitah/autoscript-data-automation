#!/usr/bin/env python3

def executar_comparacao(file1, file2, output_file):
    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            content1 = f1.read()
        
        with open(file2, 'r', encoding='utf-8') as f2:
            content2 = f2.read()
    except FileNotFoundError as e:
        raise Exception(f"Error: {e}")

    names_1 = set(name.strip() for name in content1.replace('\n', '').split(',') if name.strip())
    names_2 = set(name.strip() for name in content2.replace('\n', '').split(',') if name.strip())

    only_in_1 = names_1 - names_2
    only_in_2 = names_2 - names_1
    in_both = names_1 & names_2

    report = []
    report.append("=" * 80)
    report.append("COMPARISON REPORT")
    report.append("=" * 80)
    report.append("")

    report.append(f"Total names in {file1}: {len(names_1)}")
    report.append(f"Total names in {file2}: {len(names_2)}")
    report.append(f"Names in common: {len(in_both)}")
    report.append("")

    report.append("-" * 80)
    report.append(f"ONLY IN {file1} ({len(only_in_1)} names)")
    report.append("-" * 80)
    if only_in_1:
        for name in sorted(only_in_1):
            report.append(f"  {name}")
    else:
        report.append("  (none)")
    report.append("")

    report.append("-" * 80)
    report.append(f"ONLY IN {file2} ({len(only_in_2)} names)")
    report.append("-" * 80)
    if only_in_2:
        for name in sorted(only_in_2):
            report.append(f"  {name}")
    else:
        report.append("  (none)")
    report.append("")

    report.append("=" * 80)
    report.append("DIFFERENCES SUMMARY")
    report.append("=" * 80)
    report.append(f"Names removed: {len(only_in_1)}")
    report.append(f"Names added: {len(only_in_2)}")
    report.append(f"Total changes: {len(only_in_1) + len(only_in_2)}")
    report.append("")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    return {
        'total_file1': len(names_1),
        'total_file2': len(names_2),
        'in_common': len(in_both),
        'only_in_1': len(only_in_1),
        'only_in_2': len(only_in_2)
    }
