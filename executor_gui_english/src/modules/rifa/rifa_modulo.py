#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os


def detect_numeric_data(df):
    numeric_data = []
    
    numeric_headers = []
    for col in df.columns:
        try:
            num = float(col)
            if num.is_integer():
                numeric_headers.append(int(num))
            else:
                numeric_headers.append(num)
        except (ValueError, TypeError):
            pass
    
    if numeric_headers and len(numeric_headers) == len(df.columns):
        numeric_data.append(numeric_headers)
    
    for _, row in df.iterrows():
        numeric_row = []
        for value in row:
            try:
                num = float(value)
                if num.is_integer():
                    numeric_row.append(int(num))
                else:
                    numeric_row.append(num)
            except (ValueError, TypeError):
                continue
        
        if numeric_row and len(numeric_row) == len(df.columns):
            numeric_data.append(numeric_row)
    
    return np.array(numeric_data)


def reorganize_data_in_blocks(input_file, output_file, block_size=5, callback=None):
    def log(msg):
        if callback:
            callback(msg)
        print(msg)
    
    try:
        if not os.path.exists(input_file):
            return False, f"File not found: {input_file}", []
        
        log(f"Loading file: {input_file}")
        
        df = pd.read_excel(input_file)
        
        log(f"Original DataFrame: {df.shape[0]} rows x {df.shape[1]} columns")
        
        numeric_matrix = detect_numeric_data(df)
        
        if numeric_matrix.size == 0:
            return False, "No numeric data found in the file!", []
        
        log(f"Numeric matrix detected: {numeric_matrix.shape[0]} rows x {numeric_matrix.shape[1]} columns")
        
        reorganized_data = []
        
        num_rows, num_cols = numeric_matrix.shape
        
        num_blocks = (num_rows + block_size - 1) // block_size
        
        log(f"Processing {num_blocks} blocks of {block_size} elements each")
        
        for block in range(num_blocks):
            start_row = block * block_size
            end_row = min(start_row + block_size, num_rows)
            
            for col in range(num_cols):
                block_data = numeric_matrix[start_row:end_row, col]
                reorganized_data.extend(block_data)
            
            if callback and block % 10 == 0:
                progress = (block + 1) / num_blocks * 100
                log(f"Progress: {progress:.1f}%")
        
        log(f"Total elements reorganized: {len(reorganized_data)}")
        
        df_result = pd.DataFrame(reorganized_data, columns=['Numbers'])
        
        df_result.to_excel(output_file, index=False)
        log(f"File saved as: {output_file}")
        
        return True, f"Success! {len(reorganized_data)} elements reorganized", reorganized_data
        
    except Exception as e:
        return False, f"Error during processing: {e}", []


def processar(input_file, block_size, output_file, callback=None):
    return reorganize_data_in_blocks(input_file, output_file, block_size, callback)


if __name__ == "__main__":
    print("Data Organizer Module - Test")
    result = reorganize_data_in_blocks(
        "test.xlsx",
        "output.xlsx",
        block_size=5
    )
    print(f"Result: {result[0]}, Message: {result[1]}")
