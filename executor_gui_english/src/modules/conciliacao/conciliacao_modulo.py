#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import re
from datetime import datetime
import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
from openpyxl.formatting.rule import FormulaRule
from pathlib import Path


PDF_PATTERN = re.compile(r'(\d{2})\s+(\d{2})\s+([\d.,]+)(?:\s+(\d))?.*\.pdf$', re.IGNORECASE)
TOLERANCE_THRESHOLD = 0.01


def extract_pdf_filename_data(filename):
    try:
        match = PDF_PATTERN.match(filename)
        if not match:
            return None
        
        month = int(match.group(1))
        day = int(match.group(2))
        value_str = match.group(3).replace('.', '').replace(',', '.')
        value = float(value_str)
        version = int(match.group(4)) if match.group(4) else 1
        
        if not (1 <= month <= 12) or not (1 <= day <= 31):
            return None
        
        date_key = f"{day:02d}/{month:02d}"
        return month, day, value, version, date_key
        
    except Exception:
        return None


def load_excel_data(filepath, callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    log(f"Loading Excel data: {filepath}")
    
    if not os.path.exists(filepath):
        return None, f"Excel file not found: {filepath}"
    
    try:
        df = pd.read_excel(filepath, usecols=[0, 4], names=['Date', 'Value'])
        initial_records = len(df)
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
        df.dropna(subset=['Date'], inplace=True)
        
        records_after_date = len(df)
        if initial_records != records_after_date:
            log(f"Warning: {initial_records - records_after_date} records removed due to invalid dates")
        
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df.fillna({'Value': 0}, inplace=True)
        
        log(f"Done: {len(df)} valid records loaded from Excel")
        return df, None
        
    except Exception as e:
        return None, f"Failed to read Excel file: {e}"


def sum_pdf_values(pdf_folder, callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    log(f"Processing PDF files in folder: {pdf_folder}")
    
    if not os.path.isdir(pdf_folder):
        return None, 0, f"PDF folder not found: {pdf_folder}"
    
    all_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    
    if not all_files:
        log("Warning: No PDF files found in folder")
        return pd.DataFrame(columns=['Date', 'PDF Sum']), 0, None
    
    log(f"Found {len(all_files)} PDF files")
    
    pdf_values = {}
    ignored_files = []
    
    for i, file in enumerate(all_files, 1):
        if i % 50 == 0:
            log(f"Processing: {i}/{len(all_files)} files...")
        
        data = extract_pdf_filename_data(file)
        if data:
            month, day, value, version, date_key = data
            if version == 1:
                pdf_values[date_key] = pdf_values.get(date_key, 0) + value
        else:
            ignored_files.append(file)
    
    if ignored_files:
        log(f"Warning: {len(ignored_files)} PDF files ignored (non-standard naming)")
    
    df_pdf = pd.DataFrame(list(pdf_values.items()), columns=['Date', 'PDF Sum'])
    log(f"Done: {len(df_pdf)} days with consolidated PDF values")
    return df_pdf, len(ignored_files), None


def generate_reconciliation_report(df_excel, df_pdfs, callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    log("Generating reconciliation report...")
    
    df_excel_grouped = (
        df_excel.groupby(df_excel['Date'].dt.strftime('%d/%m'))['Value']
        .sum()
        .reset_index()
    )
    df_excel_grouped.rename(columns={'Value': 'Excel Value', 'Date': 'Date'}, inplace=True)

    df_final = pd.merge(df_excel_grouped, df_pdfs, on='Date', how='outer')
    df_final.fillna(0, inplace=True)

    df_final['Difference'] = df_final['Excel Value'] - df_final['PDF Sum']

    df_final['Status'] = df_final['Difference'].apply(
        lambda x: 'OK' if abs(x) < TOLERANCE_THRESHOLD else 'DIVERGENT'
    )
    
    df_final['Balance'] = df_final['Difference'].apply(
        lambda x: 'OK' if abs(x) < TOLERANCE_THRESHOLD else 
                 ('MISSING VALUE IN PDF' if x > 0 else 'EXCESS VALUE IN PDF')
    )

    current_year = str(datetime.now().year)
    df_final['DateObj'] = pd.to_datetime(
        df_final['Date'] + '/' + current_year, 
        format='%d/%m/%Y'
    )
    df_final.sort_values('DateObj', inplace=True)
    df_final.drop(columns=['DateObj'], inplace=True)

    log(f"Done: Report generated with {len(df_final)} records")
    return df_final


def apply_excel_formatting(ws):
    header_fill = PatternFill(start_color='4F81BD', end_color='4F81BD', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF')
    center_align = Alignment(horizontal='center', vertical='center')
    currency_format = '$ #,##0.00'
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
        cell.border = thin_border

    column_widths = {'A': 12, 'B': 15, 'C': 15, 'D': 15, 'E': 15, 'F': 22}
    for col_letter, width in column_widths.items():
        ws.column_dimensions[col_letter].width = width

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row:
            cell.border = thin_border
            if cell.column in [2, 3, 4]:
                cell.number_format = currency_format

    red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
    green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')

    ws.conditional_formatting.add(
        f'E2:E{ws.max_row}',
        FormulaRule(formula=[f'E2="DIVERGENT"'], fill=red_fill)
    )
    ws.conditional_formatting.add(
        f'E2:E{ws.max_row}',
        FormulaRule(formula=[f'E2="OK"'], fill=green_fill)
    )

    ws.freeze_panes = 'A2'


def executar_conciliacao(excel_path, pdf_folder, output_folder=None, callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    try:
        log('=== Starting reconciliation process ===')
        
        if output_folder is None:
            home = Path.home()
            desktop_names = ['Desktop', 'Escritorio']
            for name in desktop_names:
                desktop_path = home / name
                if desktop_path.exists():
                    output_folder = desktop_path / "Reconciliation"
                    break
            if output_folder is None:
                output_folder = home / 'Desktop' / 'Reconciliation'
        
        os.makedirs(output_folder, exist_ok=True)
        log(f'Output folder: {output_folder}')
        
        df_excel, error = load_excel_data(excel_path, callback)
        if df_excel is None:
            return False, error, None
        
        df_pdfs, ignored_files, error = sum_pdf_values(pdf_folder, callback)
        if df_pdfs is None:
            return False, error, None
        
        df_result = generate_reconciliation_report(df_excel, df_pdfs, callback)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f'reconciliation_final_{timestamp}.xlsx'
        output_path = os.path.join(output_folder, output_filename)
        
        log(f"Saving report...")
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_result.to_excel(writer, index=False, sheet_name='Reconciliation')
            ws = writer.sheets['Reconciliation']
            apply_excel_formatting(ws)
        
        log('=== Process completed successfully ===')
        
        message = f"""Reconciliation completed!
Statistics:
   - Excel records: {len(df_excel)}
   - PDF days: {len(df_pdfs)}
   - Report records: {len(df_result)}
   - Ignored files: {ignored_files}
Output file: {output_path}"""
        
        return True, message, output_path
        
    except Exception as e:
        return False, f"Critical error in process: {e}", None


if __name__ == "__main__":
    print("Reconciliation Module - Test")
