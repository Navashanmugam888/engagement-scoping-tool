import openpyxl

excel_file = 'C:/Users/NavashanmugamAsokan/Desktop/Projects/Engagement Scoping Tool/documents/Engagement Scoping Tool - FCC.xlsx'

wb = openpyxl.load_workbook(excel_file, data_only=False)
ws = wb['Effort Estimation']

print('=' * 120)
print('COMPLETE EFFORT ESTIMATION STRUCTURE - ALL ROWS WITH FORMULAS')
print('=' * 120)
print()

# Print ALL rows from 5-130 to see the complete structure
for row_idx in range(5, 131):
    row = ws[row_idx]
    
    # Check if this row has any content
    has_content = any(cell.value for cell in row[:8])
    
    if has_content:
        b_val = row[1].value  # Column B
        c_val = row[2].value  # Column C
        d_val = row[3].value  # Column D
        e_val = row[4].value  # Column E
        f_val = row[5].value  # Column F
        g_val = row[6].value  # Column G
        
        # Format for display
        b_str = str(b_val)[:50] if b_val else ''
        c_str = str(c_val)[:20] if c_val else ''
        e_str = str(e_val)[:30] if e_val else ''
        f_str = str(f_val)[:50] if f_val else ''
        g_str = str(g_val)[:30] if g_val else ''
        
        print(f'Row {row_idx:3d}: B={b_str:50s} C={c_str:20s} E={e_str:30s} F={f_str:50s} G={g_str:30s}')
