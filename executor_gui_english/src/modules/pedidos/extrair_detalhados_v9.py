#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import fitz  # PyMuPDF
import re
from pathlib import Path
from collections import Counter
import time


def read_orders_from_excel_by_line(excel_path):
    print(f"Reading Excel file: {excel_path}")
    
    df = pd.read_excel(excel_path)
    
    lines_info = []
    all_orders = set()
    sizes = []
    
    for idx, row in df.iterrows():
        line_num = idx + 1
        date = str(row.iloc[0]) if pd.notna(row.iloc[0]) else f"Line{line_num}"
        
        line_orders = []
        for value in row.iloc[1:]:
            if pd.notna(value):
                if isinstance(value, (int, float)):
                    order = str(int(value))
                else:
                    order = str(value).strip()
                
                if order and order != 'nan':
                    line_orders.append(order)
                    all_orders.add(order)
                    sizes.append(len(order))
        
        if line_orders:
            lines_info.append({
                'numero': line_num,
                'data': date,
                'pedidos': line_orders
            })
    
    if sizes:
        size_counter = Counter(sizes)
        most_common_size = size_counter.most_common(1)[0][0]
        unique_sizes = sorted(set(sizes))
        
        print(f"Total lines with orders: {len(lines_info)}")
        print(f"Total orders: {len(all_orders)}")
        print(f"Detected sizes: {unique_sizes}")
        print(f"Most common size: {most_common_size} digits")
        print()
        
        for line in lines_info:
            print(f"  Line {line['numero']} ({line['data']}): {len(line['pedidos'])} orders - {line['pedidos']}")
    else:
        most_common_size = 7
    
    return lines_info, most_common_size, list(all_orders)


def create_output_cache(output_folder, expected_size):
    print(f"\n{'='*60}")
    print("CREATING OUTPUT FOLDER CACHE")
    print(f"{'='*60}")
    
    if not os.path.exists(output_folder):
        print(f"Output folder not found: {output_folder}")
        return {}
    
    files = [f for f in os.listdir(output_folder) if f.endswith('.pdf')]
    
    if not files:
        print("No PDF files found in output folder")
        return {}
    
    print(f"Reading {len(files)} files from output folder...")
    
    cache = {}
    size_min = max(5, expected_size - 2)
    size_max = min(10, expected_size + 2)
    pattern = f'\\d{{{size_min},{size_max}}}'
    
    start = time.time()
    
    for i, file in enumerate(files, 1):
        full_path = os.path.join(output_folder, file)
        found_orders = set()
        
        try:
            doc = fitz.open(full_path)
            
            for page in doc:
                text = page.get_text()
                lines = text.split('\n')
                
                for line in lines:
                    matches = re.findall(pattern, line)
                    for match in matches:
                        if len(match) == expected_size:
                            found_orders.add(match)
            
            doc.close()
            cache[file] = found_orders
            
            if found_orders:
                print(f"  [{i}/{len(files)}] {file}: {len(found_orders)} orders")
            else:
                print(f"  [{i}/{len(files)}] {file}: no orders found")
                
        except Exception as e:
            print(f"  [{i}/{len(files)}] {file}: ERROR - {e}")
            cache[file] = set()
    
    total_time = time.time() - start
    print(f"\nCache created in {total_time:.2f}s")
    print(f"Total files in cache: {len(cache)}")
    print(f"{'='*60}\n")
    
    return cache


def find_output_file_with_cache(line_orders, output_cache):
    if not output_cache:
        return None
    
    line_orders_set = set(line_orders)
    
    best_match = None
    largest_intersection = 0
    
    for file, pdf_orders in output_cache.items():
        intersection = len(line_orders_set.intersection(pdf_orders))
        
        if intersection == len(line_orders) and intersection > largest_intersection:
            best_match = file
            largest_intersection = intersection
    
    if best_match:
        return os.path.splitext(best_match)[0]
    else:
        return None


def is_new_order_start(text):
    markers = [
        r'Nome\s*:',
        r'CNPJ/CPF\s*:',
        r'N[uú]mero\s+do\s+Pedido\s*:',
        r'Status\s+do\s+Pedido\s*:'
    ]
    
    for marker in markers:
        if re.search(marker, text, re.IGNORECASE):
            return True
    
    return False


def extract_order_number_from_page(text, target_orders, expected_size):
    size_min = max(5, expected_size - 2)
    size_max = min(10, expected_size + 2)
    size_pattern = f'\\d{{{size_min},{size_max}}}'
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if re.search(r'N[uú]mero\s+do\s+Pedido\s*:', line, re.IGNORECASE) and \
           not re.search(r'Valor\s+do\s+Pedido', line, re.IGNORECASE) and \
           not re.search(r'Status\s+do\s+Pedido', line, re.IGNORECASE):
            
            for j in range(max(0, i - 10), i):
                prev_line = lines[j].strip()
                match = re.match(f'^({size_pattern})$', prev_line)
                if match:
                    number = match.group(1)
                    if number in target_orders:
                        return number
            
            for j in range(i + 1, min(i + 11, len(lines))):
                next_line = lines[j].strip()
                match = re.match(f'^({size_pattern})$', next_line)
                if match:
                    number = match.group(1)
                    if number in target_orders:
                        return number
    
    for i, line in enumerate(lines):
        clean_line = line.strip()
        match = re.match(f'^({size_pattern})$', clean_line)
        if match:
            number = match.group(1)
            if len(number) == expected_size and number in target_orders:
                if i > 0:
                    return number
            elif number in target_orders:
                if i > 0:
                    return number
    
    return None


def extract_pages_by_line(pdf_path, lines_info, expected_size, output_dir, output_cache):
    print(f"Processing PDF: {pdf_path}")
    print(f"Searching for numbers with {expected_size} digits (+-2)")
    print(f"Multi-page order support: ENABLED")
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    order_to_line = {}
    for line in lines_info:
        for order in line['pedidos']:
            order_to_line[order] = line
    
    document = fitz.open(pdf_path)
    total_pages = len(document)
    
    print(f"Total pages in PDF: {total_pages}")
    print(f"Searching for orders...\n")
    
    pages_by_line = {line['numero']: [] for line in lines_info}
    found_orders = {}
    all_orders = list(order_to_line.keys())
    
    current_order = None
    current_line = None
    
    for page_num in range(total_pages):
        page = document[page_num]
        text = page.get_text()
        
        is_new_order = is_new_order_start(text)
        
        order_number = extract_order_number_from_page(text, all_orders, expected_size)
        
        if order_number and order_number in order_to_line:
            current_order = order_number
            current_line = order_to_line[order_number]
            
            print(f"Found - Page {page_num + 1}: Order {order_number} (Line {current_line['numero']}) - START")
            
            pages_by_line[current_line['numero']].append((page_num, order_number))
            found_orders[order_number] = page_num + 1
            
        elif current_order and not is_new_order:
            print(f"  -> Page {page_num + 1}: Continuation of order {current_order}")
            pages_by_line[current_line['numero']].append((page_num, current_order))
            
        elif is_new_order and not order_number:
            current_order = None
            current_line = None
            print(f"  o Page {page_num + 1}: Start of non-target order")
        
        if (page_num + 1) % 100 == 0:
            print(f"Progress: {page_num + 1}/{total_pages} pages processed...")
    
    print("\nCreating PDFs grouped by line...")
    
    for line in lines_info:
        line_num = line['numero']
        pages = pages_by_line[line_num]
        
        if pages:
            output_pdf = fitz.open()
            
            unique_pages = []
            seen_pages = set()
            for pg_num, ord_num in pages:
                if pg_num not in seen_pages:
                    unique_pages.append((pg_num, ord_num))
                    seen_pages.add(pg_num)
            
            unique_pages.sort(key=lambda x: x[0])
            
            for page_num, order_num in unique_pages:
                output_pdf.insert_pdf(document, from_page=page_num, to_page=page_num)
            
            base_name = find_output_file_with_cache(line['pedidos'], output_cache)
            
            if base_name:
                filename = f"{base_name} 2.pdf"
                print(f"  Line {line_num}: {len(unique_pages)} pages -> '{filename}'")
            else:
                clean_date = line['data'].replace('/', '-').replace(':', '-')
                filename = f"Line_{line_num}_{clean_date}.pdf"
                print(f"  Line {line_num}: {len(unique_pages)} pages -> '{filename}' (fallback)")
            
            full_path = os.path.join(output_dir, filename)
            output_pdf.save(full_path)
            output_pdf.close()
        else:
            print(f"  Line {line_num}: No pages found")
    
    document.close()

    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)
    print(f"Total lines processed: {len(lines_info)}")
    print(f"Total orders searched: {len(all_orders)}")
    print(f"Orders found: {len(found_orders)}")

    orders_not_found = set(all_orders) - set(found_orders.keys())
    if orders_not_found:
        print(f"\nOrders NOT found ({len(orders_not_found)}):")
        for order in sorted(orders_not_found):
            line = order_to_line[order]
            print(f"  - Order {order} (Line {line['numero']})")

    dates_without_orders = []
    for line in lines_info:
        if not pages_by_line.get(line['numero']):
            dates_without_orders.append({
                'numero': line['numero'],
                'data': line['data'],
                'pedidos': line['pedidos']
            })

    print(f"\nFiles saved to: {os.path.abspath(output_dir)}")
    print("="*60)

    stats = {
        'linhas_processadas': len(lines_info),
        'pedidos_procurados': len(all_orders),
        'pedidos_encontrados': len(found_orders),
        'pedidos_nao_encontrados': len(orders_not_found),
        'datas_sem_pedidos': len(dates_without_orders),
        'pedidos_nao_encontrados_lista': sorted(orders_not_found),
        'datas_sem_pedidos_lista': dates_without_orders,
        'pasta_saida': os.path.abspath(output_dir)
    }

    return stats


def main(excel_path=None, pdf_path=None, output_folder='output'):
    print("="*60)
    print("PDF PAGE EXTRACTOR - v9.0")
    print("With multi-page order support")
    print("="*60)
    
    if excel_path is None or pdf_path is None:
        if len(sys.argv) < 3:
            print("\nUsage: python3 extract_orders_v9.py <excel_file> <pdf_file> [output_folder]")
            print("\nExample:")
            print("  python3 extract_orders_v9.py Orders.xlsx LargeFile.pdf")
            print("  python3 extract_orders_v9.py Orders.xlsx LargeFile.pdf output")
            print("\nNEW: Supports orders with multiple pages!")
            sys.exit(1)
        
        excel_path = sys.argv[1]
        pdf_path = sys.argv[2]
        output_folder = sys.argv[3] if len(sys.argv) > 3 else 'output'
    
    output_dir = output_folder
    
    if not os.path.exists(excel_path):
        print(f"ERROR: Excel file not found: {excel_path}")
        sys.exit(1)
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    try:
        total_start = time.time()
        
        lines_info, expected_size, all_orders = read_orders_from_excel_by_line(excel_path)
        
        if not lines_info:
            print("ERROR: No lines with orders found in Excel")
            sys.exit(1)
        
        output_cache = create_output_cache(output_folder, expected_size)
        
        stats = extract_pages_by_line(pdf_path, lines_info, expected_size, output_dir, output_cache)
        
        total_time = time.time() - total_start
        print(f"\nProcess completed successfully in {total_time:.2f}s!")
        
        return stats
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
