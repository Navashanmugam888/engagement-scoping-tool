"""
Get actual calculated values for Historical Data section
"""
import openpyxl
from pathlib import Path

excel_path = Path("C:\\Users\\NavashanmugamAsokan\\Desktop\\Projects\\Engagement Scoping Tool\\scoping_tool\\Engagement Scoping Tool - FCC.xlsx")

# Load with data_only=True to get calculated values
wb_data = openpyxl.load_workbook(excel_path, data_only=True)
ws_data = wb_data['Effort Estimation']

# Load with formulas
wb_formulas = openpyxl.load_workbook(excel_path)
ws_formulas = wb_formulas['Effort Estimation']

print("=" * 130)
print("HISTORICAL DATA SECTION - CALCULATED VALUES & FORMULAS")
print("=" * 130)
print(f"{'Row':>3} {'B: Task':40s} {'C Calc':>8} {'E Calc':>8} {'F Calc':>10} {'F Formula':>50}")
print("-" * 130)

for row in range(84, 89):
    col_b = ws_data[f'B{row}'].value or ""
    col_c = ws_data[f'C{row}'].value or ""
    col_e = ws_data[f'E{row}'].value or ""
    col_f = ws_data[f'F{row}'].value or ""
    col_f_formula = ws_formulas[f'F{row}'].value or ""
    
    print(f"{row:3d} {str(col_b)[:39]:40s} {str(col_c):>8} {str(col_e):>8} {str(col_f):>10} {str(col_f_formula)[:49]:>50}")
