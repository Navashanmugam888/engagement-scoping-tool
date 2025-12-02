import openpyxl

excel_file = 'C:/Users/NavashanmugamAsokan/Desktop/Projects/Engagement Scoping Tool/documents/Engagement Scoping Tool - FCC.xlsx'

wb = openpyxl.load_workbook(excel_file, data_only=False)
ws = wb['Effort Estimation']

print('=== EFFORT ESTIMATION FORMULAS - KEY ROWS ===')
print()

# Look at specific task row formulas
key_rows = [
    (51, 'Additional Alias Tables'),
    (76, 'Member Formula'),
    (82, 'Number of Users'),
    (86, 'Data Validation for Account Alt Hierarchies'),
    (100, 'Consolidation Journal Reports'),
    (107, 'Automated Data loads'),
]

for row_idx, task_name in key_rows:
    print(f'Row {row_idx}: {task_name}')
    for col in range(1, 9):
        cell = ws.cell(row_idx, col)
        col_letter = chr(64+col)
        if cell.value:
            val = str(cell.value)[:100]
            print(f'  {col_letter}: {val}')
    print()

print('=' * 80)
print('UNDERSTANDING THE STRUCTURE:')
print()
print('Column E (Details): Contains the lookup value from Scope Definition')
print('Column F (Final Estimate): Contains the formula that uses Column E')
print()
print('Example formulas:')
print('  Row 51 (Additional Alias Tables): F51 = C51*E51')
print('  Row 76 (Member Formula): F76 = ROUND(E76*0.5,0)*2 + ROUND(E76*0.25,0)*3 + ROUND(E76*0.25,0)*4')
print('  Row 82 (Number of Users): F82 = E82*0.2')
print()
print('KEY INSIGHT:')
print('- Most tasks multiply base hours (Column C) by Details (Column E)')
print('- Some tasks have special formulas that scale with Details')
print('- Category headers use tier-adjusted fixed amounts')
print()
print('The issue: We are NOT correctly implementing these task-level formulas!')
