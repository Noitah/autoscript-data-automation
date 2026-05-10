#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill


def check_usage_period(date, start_date):
    try:
        if pd.isna(date):
            return False
        
        if not isinstance(date, pd.Timestamp):
            date = pd.to_datetime(date)
        
        return date >= start_date
    except:
        return False


def calculate_start_date(months):
    today = datetime.now()
    limit_date = today - timedelta(days=months * 30)
    start_date = datetime(limit_date.year, limit_date.month, 1)
    return start_date


def executar_marcar_usuarios(input_file, months_back, callback=None):
    def log(msg):
        if callback:
            callback(msg)
        else:
            print(msg)
    
    if not os.path.exists(input_file):
        msg = "Error: File '%s' not found." % input_file
        log(msg)
        return False, msg
    
    log("Reading file: %s" % input_file)
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        msg = "Error reading file: %s" % str(e)
        log(msg)
        return False, msg
    
    if 'USR_ID' not in df.columns:
        msg = "Error: Column 'USR_ID' not found"
        log(msg)
        return False, msg
    
    if 'ULT_USO' not in df.columns:
        msg = "Error: Column 'ULT_USO' not found"
        log(msg)
        return False, msg
    
    log("Total rows: %d" % len(df))
    
    start_date = calculate_start_date(months_back)
    log("Analysis period: from %s" % start_date.strftime("%B %d, %Y"))
    
    users_with_usage = {}
    
    for idx, row in df.iterrows():
        usr_id = row['USR_ID']
        usage_date = row['ULT_USO']
        
        if usr_id not in users_with_usage:
            users_with_usage[usr_id] = []
        
        has_usage = check_usage_period(usage_date, start_date)
        users_with_usage[usr_id].append({
            'line': idx,
            'has_usage': has_usage
        })
    
    users_to_mark = set()
    
    for usr_id, occurrences in users_with_usage.items():
        if len(occurrences) == 2:
            if occurrences[0]['has_usage'] and occurrences[1]['has_usage']:
                users_to_mark.add(usr_id)
        elif len(occurrences) == 1:
            if occurrences[0]['has_usage']:
                users_to_mark.add(usr_id)
    
    total_users = len(users_with_usage)
    marked_users = len(users_to_mark)
    
    log("Users to mark: %d" % marked_users)
    log("Total users: %d" % total_users)
    
    base_name = os.path.splitext(input_file)[0]
    extension = os.path.splitext(input_file)[1]
    output_file = "%s_marked%s" % (base_name, extension)
    
    if extension.lower() == '.xls':
        output_file = "%s_marked.xlsx" % base_name
    
    log("Saving file: %s" % output_file)
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    wb = load_workbook(output_file)
    ws = wb.active
    
    green_fill = PatternFill(start_color="00B050", end_color="00B050", fill_type="solid")
    
    marked_lines = 0
    for idx, row in df.iterrows():
        usr_id = row['USR_ID']
        if usr_id in users_to_mark:
            excel_row = idx + 2
            for col in range(1, len(df.columns) + 1):
                ws.cell(row=excel_row, column=col).fill = green_fill
            marked_lines += 1
    
    last_row = len(df) + 2
    ws.cell(row=last_row, column=1).value = "Total: %d" % marked_users
    
    for col in range(1, len(df.columns) + 1):
        ws.cell(row=last_row, column=col).font = ws.cell(row=last_row, column=col).font.copy()
    
    wb.save(output_file)
    
    log("\nSuccess!")
    log("- %d rows marked in green" % marked_lines)
    log("- Total users: %d" % total_users)
    log("- File saved as: %s" % output_file)
    
    return True, "Processing completed successfully", output_file
