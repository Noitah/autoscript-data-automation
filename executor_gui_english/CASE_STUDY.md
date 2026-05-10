# Case Study: AutoScript - Process Automation Platform

## 1. Project Overview

**AutoScript** is a desktop application developed in Python with a graphical user interface (GUI) that centralizes and executes multiple data automation scripts. The project was created to solve the problem of repetitive manual processes in administrative and financial routines, transforming tasks that took hours into executions of a few seconds.

**Author:** João Victor Cotrim
**Technologies:** Python, Tkinter, Pandas, OpenPyXL, PyMuPDF (fitz), PyInstaller
**Project Size:** ~2,500 lines of modularized code

## 2. The Challenge

Many companies deal with massive volumes of data spread across Excel spreadsheets and PDF documents. Manual processing of this data presents three main problems:
1. **Excessive time:** Tasks like financial reconciliation and data extraction from PDFs consumed hours of daily work.
2. **High error rate:** Manual typing and comparison of thousands of records inevitably generated human errors.
3. **Lack of standardization:** Different employees executed tasks in different ways.

## 3. The Developed Solution

I developed a robust desktop application with a modular architecture that allows the execution of different automation routines through a user-friendly interface.

### System Architecture
The project was structured following software engineering best practices:
- **Separation of Concerns (MVC-like):** Graphical interface (`ui/`), business logic (`core/`), and specific scripts (`modules/`) are isolated.
- **Dynamic Loading:** Modules are loaded dynamically via `ModuleLoader`, allowing new automations to be added without changing the main code.
- **Centralized Validation:** A validation system (`Validators`) ensures that all inputs (files, folders, parameters) are correct before execution.

### Implemented Automation Modules

1. **Financial Reconciliation:** 
   - Reads thousands of records from an Excel file and compares them with values extracted from PDF file names.
   - Generates an automated report highlighting discrepancies and applying conditional formatting (colors) for easy visualization.

2. **Order Processing and Extraction (PDF/Excel):**
   - Reads order lines in Excel and searches for matches in PDFs with hundreds of pages.
   - Extracts specific pages, calculates total values, and generates new individualized PDFs per order.

3. **Data Organizer (Raffle):**
   - Reorganizes complex data from Excel spreadsheets into a single-column structure based on blocks, facilitating import into other systems.

4. **File Comparison:**
   - Analyzes two distinct text/data files and generates a detailed report showing common items and exclusive items from each file.

## 4. Results and Impact

The implementation of this tool generated significant results:

- **Time Reduction:** Reconciliation processes that took hours are now executed in less than 1 minute.
- **100% Accuracy:** Complete elimination of typing and manual comparison errors.
- **Accessibility:** The intuitive graphical interface allowed users without technical knowledge (programming) to execute complex Python scripts.
- **Easy Distribution:** The project was packaged as a standalone executable (`.exe`) using PyInstaller, not requiring Python installation on end-users' machines.

## 5. Demonstrated Skills

This project demonstrates my ability to:
- Develop complete end-to-end solutions (from backend to user interface).
- Work with advanced data manipulation (Pandas) and document (PyMuPDF) libraries.
- Apply Clean Code concepts, Type Hints, and modularization in Python.
- Understand real business problems and translate them into efficient software solutions.
