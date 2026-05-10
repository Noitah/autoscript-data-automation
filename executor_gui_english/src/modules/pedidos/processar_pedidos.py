#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openpyxl
import fitz  # PyMuPDF
from datetime import datetime
from collections import defaultdict, Counter
import os
import re
import time


def read_orders_from_excel(excel_path):
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active
    
    order_lines = []
    
    for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        if row[0] is None:
            continue
        
        if isinstance(row[0], datetime):
            date = row[0].strftime('%Y-%m-%d')
        elif isinstance(row[0], str):
            try:
                if '/' in row[0]:
                    date_obj = datetime.strptime(row[0], '%d/%m/%Y')
                    date = date_obj.strftime('%Y-%m-%d')
                elif '-' in row[0] and row[0].count('-') == 2:
                    parts = row[0].split('-')
                    if len(parts[0]) == 2:
                        date_obj = datetime.strptime(row[0], '%d-%m-%Y')
                        date = date_obj.strftime('%Y-%m-%d')
                    else:
                        date = row[0]
                else:
                    date = str(row[0]).replace('/', '-')
            except:
                date = str(row[0]).replace('/', '-').replace('\\', '-')
        else:
            date = str(row[0]).replace('/', '-').replace('\\', '-')
        
        line_orders = []
        for i in range(1, len(row)):
            if row[i] is not None and row[i] != '':
                number = str(int(float(row[i]))) if isinstance(row[i], float) else str(row[i])
                line_orders.append(number)
        
        if line_orders:
            order_lines.append({
                'data': date,
                'linha': idx,
                'pedidos': line_orders
            })
    
    workbook.close()
    return order_lines


def extract_page_total_value(text):
    if 'TOTAL:' not in text:
        return None
    
    found_values = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        match = re.match(r'^([\d,.]+)$', line)
        if match:
            value_str = match.group(1)
            
            if ',' in value_str and '.' in value_str:
                value_str = value_str.replace(',', '')
            elif ',' in value_str and '.' not in value_str:
                value_str = value_str.replace(',', '.')
            
            try:
                value = float(value_str)
                if 1.0 <= value <= 1000000:
                    found_values.append(value)
            except:
                continue
    
    if not found_values:
        return None
    
    count = Counter(found_values)
    most_common_value = count.most_common(1)[0][0]
    
    return most_common_value


def search_orders_and_values(pdf_path, all_order_numbers, callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    log("Searching orders and extracting values...")
    
    pages_by_order = defaultdict(list)
    values_by_page = {}
    start_time = time.time()
    
    patterns = {number: re.compile(r'\b' + re.escape(number) + r'\b') 
               for number in all_order_numbers}
    
    try:
        pdf_doc = fitz.open(pdf_path)
        total_pages = len(pdf_doc)
        
        log(f"Total pages: {total_pages}")
        log(f"Orders to search: {len(all_order_numbers)}")
        
        for page_num in range(total_pages):
            if (page_num + 1) % 100 == 0:
                elapsed = time.time() - start_time
                pages_sec = (page_num + 1) / elapsed if elapsed > 0 else 0
                progress = (page_num + 1) / total_pages * 100
                log(f"Progress: {progress:.1f}% ({page_num + 1}/{total_pages}) - {pages_sec:.0f} pages/sec")
            
            try:
                page = pdf_doc[page_num]
                text = page.get_text()
                
                if text:
                    for number, pattern in patterns.items():
                        if pattern.search(text):
                            pages_by_order[number].append(page_num)
                    
                    value = extract_page_total_value(text)
                    if value is not None:
                        values_by_page[page_num] = value
            except:
                continue
        
        pdf_doc.close()
        total_time = time.time() - start_time
        log(f"Done in {total_time:.1f} seconds!")
        log(f"Values extracted from {len(values_by_page)} pages")
        
    except Exception as e:
        log(f"Error: {e}")
        return {}, {}
    
    return dict(pages_by_order), values_by_page


def create_total_page(total_value):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'PaginaFinal.pdf')
    
    if not os.path.exists(template_path):
        pdf = fitz.open()
        page = pdf.new_page(width=595, height=841)
        formatted_value = f"{total_value:,.2f}"
        page.insert_text((420, 90), "Grand Total:", fontsize=12, fontname="helv")
        page.insert_text((520, 90), formatted_value, fontsize=12, fontname="helv")
        return pdf
    
    template = fitz.open(template_path)
    new_pdf = fitz.open()
    new_pdf.insert_pdf(template)
    template.close()
    
    page = new_pdf[0]
    
    formatted_value = f"{total_value:,.2f}"
    
    text = page.get_text("dict")
    
    for block in text["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    span_text = span["text"].strip()
                    if re.match(r'^[\d,.]+$', span_text) and len(span_text) > 3:
                        bbox = span["bbox"]
                        rect = fitz.Rect(bbox)
                        rect.x0 -= 2
                        rect.y0 -= 2
                        rect.x1 += 2
                        rect.y1 += 2
                        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                        
                        page.insert_text(
                            (bbox[0] - 6, bbox[3] - 3),
                            formatted_value,
                            fontsize=span["size"],
                            fontname="hebo"
                        )
                        break
    
    return new_pdf


def create_pdfs_with_values(pdf_path, order_lines, pages_by_order, 
                           values_by_page, output_dir='output', callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    log("Creating PDFs with values...")
    
    original_pdf = fitz.open(pdf_path)
    orders_not_found = []
    dates_without_orders = []
    pdfs_created = 0
    
    total_lines = len(order_lines)
    
    for idx, item in enumerate(order_lines, 1):
        date = item['data']
        excel_line = item['linha']
        orders = item['pedidos']
        
        if idx % 5 == 0:
            progress = idx / total_lines * 100
            log(f"Processing: {progress:.1f}% ({idx}/{total_lines})")
        
        unique_pages = set()
        total_value = 0.0
        not_found_in_line = []
        
        for number in orders:
            if number in pages_by_order:
                pages = pages_by_order[number]
                unique_pages.update(pages)
                
                for page in pages:
                    if page in values_by_page:
                        total_value += values_by_page[page]
            else:
                not_found_in_line.append(number)
        
        if not_found_in_line:
            orders_not_found.append({
                'data': date,
                'linha': excel_line,
                'pedidos': not_found_in_line
            })
        
        if unique_pages:
            new_pdf = fitz.open()
            
            for page in sorted(unique_pages):
                new_pdf.insert_pdf(original_pdf, from_page=page, to_page=page)
            
            total_pdf = create_total_page(total_value)
            new_pdf.insert_pdf(total_pdf)
            total_pdf.close()
            
            date_parts = date.split('-')
            day = date_parts[2] if len(date_parts) == 3 else '01'
            month = date_parts[1] if len(date_parts) == 3 else '01'
            
            formatted_value = f"{total_value:.2f}".replace('.', ',')
            base_name = f"{month} {day} {formatted_value}.pdf"
            
            final_filename = base_name
            filepath = os.path.join(output_dir, base_name)
            
            if os.path.exists(filepath):
                name, ext = os.path.splitext(base_name)
                counter = 2
                while True:
                    final_filename = f"{name} {counter}{ext}"
                    filepath = os.path.join(output_dir, final_filename)
                    if not os.path.exists(filepath):
                        break
                    counter += 1
            
            new_pdf.save(filepath)
            new_pdf.close()
            pdfs_created += 1
        else:
            dates_without_orders.append({
                'data': date,
                'linha': excel_line,
                'pedidos': orders
            })
    
    original_pdf.close()
    log(f"{pdfs_created} PDFs created successfully!")
    
    return orders_not_found, dates_without_orders


def executar_processamento_pedidos(excel_path, pdf_path, output_folder='output', callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    try:
        log('=== Starting order processing ===')
        
        if not os.path.exists(excel_path):
            return False, f"Excel file not found: {excel_path}", {}
        
        if not os.path.exists(pdf_path):
            return False, f"PDF file not found: {pdf_path}", {}
        
        log("Reading orders from Excel...")
        order_lines = read_orders_from_excel(excel_path)
        
        if not order_lines:
            return False, "No orders found in Excel", {}
        
        all_orders = set()
        for line in order_lines:
            all_orders.update(line['pedidos'])
        
        log(f"{len(order_lines)} lines with {len(all_orders)} unique orders")
        
        pages_by_order, values_by_page = search_orders_and_values(
            pdf_path, list(all_orders), callback
        )
        
        orders_not_found, dates_without_orders = create_pdfs_with_values(
            pdf_path, order_lines, pages_by_order, 
            values_by_page, output_folder, callback
        )
        
        log(f"Orders not found: {len(orders_not_found)}")
        log(f"Dates without orders: {len(dates_without_orders)}")
        if orders_not_found:
            log("List of orders not found:")
            for item in orders_not_found:
                log(f"  Date: {item['data']} | Line: {item['linha']} | Orders: {', '.join(item['pedidos'])}")
        else:
            log("All orders were matched successfully.")

        if dates_without_orders:
            log("List of dates without matching orders:")
            for item in dates_without_orders:
                log(f"  Date: {item['data']} | Line: {item['linha']} | Orders: {', '.join(item['pedidos'])}")
        else:
            log("All dates had matching orders.")
        log('=== Process completed ===')
        
        stats = {
            'linhas_processadas': len(order_lines),
            'pedidos_unicos': len(all_orders),
            'pedidos_encontrados': len(pages_by_order),
            'pedidos_nao_encontrados': len(orders_not_found),
            'datas_sem_pedidos': len(dates_without_orders),
            'pedidos_nao_encontrados_lista': orders_not_found,
            'datas_sem_pedidos_lista': dates_without_orders
        }
        
        message = f"""Processing completed!
Statistics:
   - Lines processed: {stats['linhas_processadas']}
   - Unique orders: {stats['pedidos_unicos']}
   - Orders found: {stats['pedidos_encontrados']}
   - Orders not found: {stats['pedidos_nao_encontrados']}
   - Dates without orders: {stats['datas_sem_pedidos']}
Output folder: {os.path.abspath(output_folder)}"""
        
        return True, message, stats
        
    except Exception as e:
        return False, f"Critical error: {e}", {}


if __name__ == "__main__":
    print("Order Processing Module - Test")
