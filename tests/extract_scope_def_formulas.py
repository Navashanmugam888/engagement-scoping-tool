"""
Extract the formulas in Column E (Details/Weightage) of Scope Definition
"""
import openpyxl
from pathlib import Path

excel_path = Path("C:\\Users\\NavashanmugamAsokan\\Desktop\\Projects\\Engagement Scoping Tool\\scoping_tool\\Engagement Scoping Tool - FCC.xlsx")
wb = openpyxl.load_workbook(excel_path)
ws_scope = wb['Scope Definition']

print("=" * 130)
print("SCOPE DEFINITION - FORMULAS IN COLUMN E (Weightage/Details)")
print("=" * 130)

# Read formulas for key metrics
metrics_to_check = [40, 41, 44, 45, 49]  # Data Forms, Dashboards, Business Rules, Member Formula, etc.

for row in metrics_to_check:
    col_b = ws_scope[f'B{row}'].value
    cell_e = ws_scope[f'E{row}']
    
    if col_b:
        print(f"\nRow {row}: {col_b}")
        # Try to get the formula value
        formula_value = cell_e.value
        if hasattr(formula_value, 'text'):
            print(f"  Formula: {formula_value.text}")
        else:
            print(f"  Formula: {formula_value}")
        print(f"  Type: {type(formula_value)}")
