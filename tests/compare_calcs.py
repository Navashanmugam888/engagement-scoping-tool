#!/usr/bin/env python
"""Compare Excel vs Python calculations"""

import openpyxl
import json

# Excel data directly from sheet
excel_data = {
    5: {'name': 'Project Initiation and Planning', 'base': 12, 'final': 18},
    14: {'name': 'Creating and Managing EPM Cloud Infrastructure', 'base': 6, 'final': 6},
    18: {'name': 'Requirement Gathering, Read back and Client Sign-off', 'base': 32, 'final': 44},
    28: {'name': 'Design', 'base': 26, 'final': 42},
    35: {'name': 'Build and Configure FCC', 'base': 88, 'final': 104},
    53: {'name': 'Setup Application Features', 'base': 79.5, 'final': 95.5},
    70: {'name': 'Application Customization', 'base': 8, 'final': 20},
    74: {'name': 'Calculations', 'base': 15, 'final': 27},
    81: {'name': 'Secured Dimensions', 'base': 2, 'final': 4},
    84: {'name': 'Historical Data', 'base': 60, 'final': 72},
    90: {'name': 'Integrations', 'base': 80, 'final': 92},
    98: {'name': 'Management Reports', 'base': 8, 'final': 52},
    106: {'name': 'Automations', 'base': 52, 'final': 64},
    112: {'name': 'Testing/Training', 'base': 152, 'final': 164},
    123: {'name': 'Documentations', 'base': 24, 'final': 36},
    128: {'name': 'Change Management', 'base': 32, 'final': 44},
}

python_data = {
    'Project Initiation and Planning': 18.0,
    'Creating and Managing EPM Cloud Infrastructure': 6.0,
    'Requirement Gathering, Read back and Client Sign-off': 44.0,
    'Design': 42.0,
    'Build and Configure FCC': 139.5,
    'Setup Application Features': 97.5,
    'Application Customization': 20.0,
    'Calculations': 46.0,
    'Secured Dimensions': 24.0,
    'Historical Data': 592.0,
    'Integrations': 124.0,
    'Automations': 64.0,
    'Testing/Training': 244.0,
    'Documentations': 36.0,
    'Change Management': 44.0,
}

print('=' * 120)
print('EFFORT CALCULATION COMPARISON: EXCEL vs PYTHON')
print('=' * 120)
print()
print('| Category | Excel Base | Excel Final | Python Calc | Difference | Variance % | Status |')
print('|' + '-' * 118 + '|')

total_excel = 0
total_python = 0
mismatches = []

for row_num in sorted(excel_data.keys()):
    excel_cat = excel_data[row_num]
    cat_name = excel_cat['name']
    excel_base = excel_cat['base']
    excel_final = excel_cat['final']
    
    python_calc = python_data.get(cat_name, 0)
    
    total_excel += excel_final
    total_python += python_calc
    
    diff = python_calc - excel_final
    variance_pct = (diff / excel_final * 100) if excel_final > 0 else 0
    
    # Determine status
    if abs(diff) < 0.1:
        status = 'MATCH'
    elif abs(variance_pct) < 5:
        status = 'OK'
    else:
        status = 'MISMATCH!'
        mismatches.append({
            'category': cat_name,
            'excel': excel_final,
            'python': python_calc,
            'diff': diff,
            'pct': variance_pct
        })
    
    print('| {:50s} | {:>10.1f} | {:>11.1f} | {:>11.1f} | {:>10.1f} | {:>9.1f}% | {:10s} |'.format(
        cat_name[:50], excel_base, excel_final, python_calc, diff, variance_pct, status))

print('|' + '-' * 118 + '|')
print('| {:50s} | {:>10s} | {:>11.1f} | {:>11.1f} | {:>10.1f} | {:>9s} | {:10s} |'.format(
    'TOTAL', '', total_excel, total_python, total_python - total_excel, '', ''))
print('=' * 120)

print('\n\nKEY FINDINGS:')
print('=' * 120)

if mismatches:
    print('\nCATEGORIES WITH SIGNIFICANT DISCREPANCIES:')
    print('-' * 120)
    for m in mismatches:
        print('  {} (Excel: {:.1f} -> Python: {:.1f}, Diff: {:+.1f}, {:+.1f}%)'.format(
            m['category'], m['excel'], m['python'], m['diff'], m['pct']))
else:
    print('No significant mismatches found!')

print('\n\nOVERALL VARIANCE:')
overall_pct = ((total_python - total_excel) / total_excel * 100) if total_excel > 0 else 0
print('  Excel Total:  {:.1f} hours'.format(total_excel))
print('  Python Total: {:.1f} hours'.format(total_python))
print('  Difference:   {:+.1f} hours ({:+.1f}%)'.format(total_python - total_excel, overall_pct))

# Save results to file
with open('comparison_results.json', 'w') as f:
    json.dump({
        'excel_total': total_excel,
        'python_total': total_python,
        'difference': total_python - total_excel,
        'variance_pct': overall_pct,
        'mismatches': mismatches,
        'categories': {
            excel_data[k]['name']: {
                'excel_final': excel_data[k]['final'],
                'python_calc': python_data.get(excel_data[k]['name'], 0),
                'difference': python_data.get(excel_data[k]['name'], 0) - excel_data[k]['final']
            }
            for k in excel_data.keys()
        }
    }, f, indent=2)

print('\n\nResults saved to comparison_results.json')
