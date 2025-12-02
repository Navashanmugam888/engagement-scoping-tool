"""
Check Application Customization and Reporting tasks in Excel
"""
import openpyxl
from pathlib import Path

excel_path = Path("C:\\Users\\NavashanmugamAsokan\\Desktop\\Projects\\Engagement Scoping Tool\\scoping_tool\\Engagement Scoping Tool - FCC.xlsx")

wb_data = openpyxl.load_workbook(excel_path, data_only=True)
ws_data = wb_data['Effort Estimation']

wb_formulas = openpyxl.load_workbook(excel_path)
ws_formulas = wb_formulas['Effort Estimation']

print("=" * 130)
print("APPLICATION CUSTOMIZATION SECTION (Rows ~70-73)")
print("=" * 130)
# Find Application Customization header first
for row in range(60, 80):
    if ws_data[f'B{row}'].value and 'Application Customization' in str(ws_data[f'B{row}'].value):
        print(f"Found at Row {row}")
        # Print this row and next few rows
        for r in range(row, row + 10):
            col_b = ws_data[f'B{r}'].value or ""
            col_c = ws_data[f'C{r}'].value or ""
            col_e = ws_data[f'E{r}'].value or ""
            col_f = ws_data[f'F{r}'].value or ""
            col_f_formula = ws_formulas[f'F{r}'].value or ""
            
            print(f"Row {r}: {str(col_b)[:40]:40s} C={str(col_c):>6} E={str(col_e):>6} F={str(col_f):>8} Formula={str(col_f_formula)[:40]}")

print("\n" + "=" * 130)
print("REPORTING SECTION (Rows ~97-106)")
print("=" * 130)
# Find Reporting header
for row in range(90, 110):
    if ws_data[f'B{row}'].value and 'Reporting' in str(ws_data[f'B{row}'].value) and 'Requirement' not in str(ws_data[f'B{row}'].value):
        print(f"Found at Row {row}")
        # Print this row and next few rows
        for r in range(row, min(row + 12, 110)):
            col_b = ws_data[f'B{r}'].value or ""
            col_c = ws_data[f'C{r}'].value or ""
            col_e = ws_data[f'E{r}'].value or ""
            col_f = ws_data[f'F{r}'].value or ""
            col_f_formula = ws_formulas[f'F{r}'].value or ""
            
            print(f"Row {r}: {str(col_b)[:40]:40s} C={str(col_c):>6} E={str(col_e):>6} F={str(col_f):>8} Formula={str(col_f_formula)[:40]}")
