import openpyxl
import re

excel_file = 'C:/Users/NavashanmugamAsokan/Desktop/Projects/Engagement Scoping Tool/documents/Engagement Scoping Tool - FCC.xlsx'

wb = openpyxl.load_workbook(excel_file, data_only=False)
ws = wb['Effort Estimation']

print('=== EXTRACTING EXACT TIER ADJUSTMENT VALUES ===')
print()

category_rows = [
    (5, 'Project Initiation and Planning'),
    (18, 'Requirement Gathering, Read back and Client Sign-off'),
    (28, 'Design'),
    (35, 'Build and Configure FCC'),
    (53, 'Setup Application Features'),
    (70, 'Application Customization'),
    (74, 'Calculations'),
    (80, 'Security'),
    (84, 'Historical Data'),
    (90, 'Integrations'),
    (97, 'Reporting'),
    (106, 'Automations'),
    (112, 'Testing/Training'),
    (119, 'Transition'),
    (123, 'Documentations'),
    (128, 'Change Management'),
]

tier_adjustments = {}

for row_idx, category_name in category_rows:
    cell_f = ws.cell(row_idx, 6)  # Column F
    
    if cell_f.value and isinstance(cell_f.value, str):
        formula = str(cell_f.value)
        
        # Extract the adjustment values using regex
        # Pattern: +4, +8, +12, etc.
        matches = re.findall(r'\+(\d+)', formula)
        
        if len(matches) >= 3:
            adj_120 = int(matches[0])
            adj_160 = int(matches[1])
            adj_else = int(matches[2])
            
            tier_adjustments[category_name] = {
                '<=100': 0,
                '<=120': adj_120,
                '<=160': adj_160,
                '>160': adj_else
            }
            
            print(f'{category_name}:')
            print(f'  Weightage <= 100: +0')
            print(f'  Weightage <= 120: +{adj_120}')
            print(f'  Weightage <= 160: +{adj_160}')
            print(f'  Weightage > 160: +{adj_else}')
            print()

print('='*80)
print('SUMMARY:')
print()
print('Categories with (0, 4, 6, 8) pattern:')
for cat, adj in tier_adjustments.items():
    if adj.get('<=120') == 4 and adj.get('<=160') == 6 and adj.get('>160') == 8:
        print(f'  - {cat}')

print()
print('Categories with (0, 8, 12, 16) pattern:')
for cat, adj in tier_adjustments.items():
    if adj.get('<=120') == 8 and adj.get('<=160') == 12 and adj.get('>160') == 16:
        print(f'  - {cat}')

print()
print('Categories with (0, 8, 16, 24) pattern:')
for cat, adj in tier_adjustments.items():
    if adj.get('<=120') == 8 and adj.get('<=160') == 16 and adj.get('>160') == 24:
        print(f'  - {cat}')

print()
print('Categories with (0, 8, 12, 12) pattern:')
for cat, adj in tier_adjustments.items():
    if adj.get('<=120') == 8 and adj.get('<=160') == 12 and adj.get('>160') == 12:
        print(f'  - {cat}')
