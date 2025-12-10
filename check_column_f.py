import openpyxl

# Load with formulas (not calculated values)
wb = openpyxl.load_workbook('Engagement Scoping Tool - FCC.xlsx')
ws_effort = wb['Effort Estimation']

print("=" * 80)
print("CHECKING COLUMN F FORMULAS (Final Hours)")
print("=" * 80)

print(f"\nRow 86: Data Validation for Account Alt Hierarchies")
print(f"  Column F Formula: {ws_effort['F86'].value}")

print(f"\nRow 87: Data Validation for Entity Alt Hierarchies")
print(f"  Column F Formula: {ws_effort['F87'].value}")

print(f"\nRow 88: Historical Journal Conversion")
print(f"  Column F Formula: {ws_effort['F88'].value}")

# Also check a few rows above to understand the pattern
print("\n" + "=" * 80)
print("CHECKING PARENT TASK (Historical Data Validation)")
print("=" * 80)

for row in range(83, 89):
    task_name = ws_effort[f'A{row}'].value
    col_c = ws_effort[f'C{row}'].value
    col_e = ws_effort[f'E{row}'].value
    col_f = ws_effort[f'F{row}'].value
    if task_name:
        print(f"\nRow {row}: {task_name}")
        print(f"  C (Base): {col_c}")
        print(f"  E (Formula): {col_e}")
        print(f"  F (Formula): {col_f}")
