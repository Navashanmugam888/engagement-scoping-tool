"""
Extract the lookup values from Scope Definition sheet for metrics with lookup formulas
"""
import openpyxl
from pathlib import Path

excel_path = Path("C:\\Users\\NavashanmugamAsokan\\Desktop\\Projects\\Engagement Scoping Tool\\scoping_tool\\Engagement Scoping Tool - FCC.xlsx")
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws_scope = wb['Scope Definition']

print("=" * 100)
print("SCOPE DEFINITION SHEET - METRICS WITH DETAILS")
print("=" * 100)
print(f"{'Row':>3} {'B: Metric':45s} {'D: In Scope':>10} {'E: Details':>12}")
print("-" * 100)

# Read all rows to identify the metrics and their detail values
for row in range(3, 50):
    col_b = ws_scope[f'B{row}'].value
    col_d = ws_scope[f'D{row}'].value
    col_e = ws_scope[f'E{row}'].value
    
    if col_b and col_d:  # Has metric name and in-scope indicator
        print(f"{row:3d} {str(col_b)[:44]:45s} {str(col_d):>10} {str(col_e):>12}")
