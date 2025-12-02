#!/usr/bin/env python
"""
Generate comprehensive comparison table and summary report
"""

print("""
================================================================================
COMPREHENSIVE EFFORT CALCULATION COMPARISON REPORT
================================================================================
""")

# Create detailed comparison table
categories = [
    {
        'name': 'Project Initiation and Planning',
        'excel_base': 12,
        'excel_final': 18,
        'python_calc': 18.0,
        'row': 5
    },
    {
        'name': 'Creating and Managing EPM Cloud Infrastructure',
        'excel_base': 6,
        'excel_final': 6,
        'python_calc': 6.0,
        'row': 14
    },
    {
        'name': 'Requirement Gathering, Read back and Client Sign-off',
        'excel_base': 32,
        'excel_final': 44,
        'python_calc': 44.0,
        'row': 18
    },
    {
        'name': 'Design',
        'excel_base': 26,
        'excel_final': 42,
        'python_calc': 42.0,
        'row': 28
    },
    {
        'name': 'Build and Configure FCC',
        'excel_base': 88,
        'excel_final': 104,
        'python_calc': 139.5,
        'row': 35,
        'issue': 'Python adds subtask details'
    },
    {
        'name': 'Setup Application Features',
        'excel_base': 79.5,
        'excel_final': 95.5,
        'python_calc': 97.5,
        'row': 53
    },
    {
        'name': 'Application Customization',
        'excel_base': 8,
        'excel_final': 20,
        'python_calc': 20.0,
        'row': 70
    },
    {
        'name': 'Calculations',
        'excel_base': 15,
        'excel_final': 27,
        'python_calc': 46.0,
        'row': 74,
        'issue': 'Python includes BR, MF, etc'
    },
    {
        'name': 'Secured Dimensions',
        'excel_base': 2,
        'excel_final': 4,
        'python_calc': 24.0,
        'row': 81,
        'issue': 'Task row, not category'
    },
    {
        'name': 'Historical Data',
        'excel_base': 60,
        'excel_final': 72,
        'python_calc': 592.0,
        'row': 84,
        'issue': 'HistData Validation incorrectly added'
    },
    {
        'name': 'Integrations',
        'excel_base': 80,
        'excel_final': 92,
        'python_calc': 124.0,
        'row': 90,
        'issue': 'Python adds task details'
    },
    {
        'name': 'Management Reports',
        'excel_base': 8,
        'excel_final': 52,
        'python_calc': 0.0,
        'row': 98,
        'issue': 'Formula not implemented'
    },
    {
        'name': 'Automations',
        'excel_base': 52,
        'excel_final': 64,
        'python_calc': 64.0,
        'row': 106
    },
    {
        'name': 'Testing/Training',
        'excel_base': 152,
        'excel_final': 164,
        'python_calc': 244.0,
        'row': 112,
        'issue': 'Python calculation incorrect'
    },
    {
        'name': 'Documentations',
        'excel_base': 24,
        'excel_final': 36,
        'python_calc': 36.0,
        'row': 123
    },
    {
        'name': 'Change Management',
        'excel_base': 32,
        'excel_final': 44,
        'python_calc': 44.0,
        'row': 128
    },
]

print()
print('COMPARISON TABLE: Excel vs Python Calculations')
print('=' * 140)
print('{:<50s} | {:>10s} | {:>12s} | {:>12s} | {:>12s} | {:>8s} | {:<30s}'.format(
    'Category Name', 'Excel Base', 'Excel Final', 'Python Calc', 'Difference', 'Var %', 'Status'))
print('-' * 140)

total_excel_final = 0
total_python_calc = 0
mismatches = []

for cat in categories:
    excel_final = cat['excel_final']
    python_calc = cat['python_calc']
    
    total_excel_final += excel_final
    total_python_calc += python_calc
    
    diff = python_calc - excel_final
    var_pct = (diff / excel_final * 100) if excel_final > 0 else 0
    
    status = 'MATCH' if abs(diff) < 0.1 else ('OK' if abs(var_pct) < 5 else 'MISMATCH!')
    
    if status == 'MISMATCH!':
        mismatches.append(cat)
    
    issue_note = cat.get('issue', '')
    
    print('{:<50s} | {:>10.1f} | {:>12.1f} | {:>12.1f} | {:>+12.1f} | {:>+7.1f}% | {:<30s}'.format(
        cat['name'][:50], cat['excel_base'], excel_final, python_calc, diff, var_pct, status))

print('-' * 140)
print('{:<50s} | {:>10s} | {:>12.1f} | {:>12.1f} | {:>+12.1f} | {:>8s} | {:<30s}'.format(
    'TOTAL', '', total_excel_final, total_python_calc, total_python_calc - total_excel_final, '', ''))
print('=' * 140)

print()
print()
print('SUMMARY STATISTICS')
print('=' * 80)
print('Total Excel Final Estimate:  {:>10.1f} hours'.format(total_excel_final))
print('Total Python Calculation:    {:>10.1f} hours'.format(total_python_calc))
print('Difference:                  {:>+10.1f} hours'.format(total_python_calc - total_excel_final))
print('Variance:                    {:>+10.1f}%'.format(
    (total_python_calc - total_excel_final) / total_excel_final * 100))
print()

print()
print('CRITICAL MISMATCHES REQUIRING FIX')
print('=' * 80)

for cat in mismatches:
    diff = cat['python_calc'] - cat['excel_final']
    pct = (diff / cat['excel_final'] * 100) if cat['excel_final'] > 0 else 0
    
    print()
    print('  Row {}: {}'.format(cat['row'], cat['name']))
    print('    Excel:  Base={:>6.1f}, Final={:>6.1f}'.format(cat['excel_base'], cat['excel_final']))
    print('    Python: {:>20.1f}'.format(cat['python_calc']))
    print('    Error:  {:>+6.1f} hours ({:>+.1f}%)'.format(diff, pct))
    if 'issue' in cat:
        print('    Issue:  {}'.format(cat['issue']))

print()
print()
print('ACTION ITEMS')
print('=' * 80)
print()
print('1. Build and Configure FCC (+35.5 hours)')
print('   - Python incorrectly sums subtask details (Account Alt Hier, Currency, etc)')
print('   - Fix: Remove detail calculations from category - use only base + tier adjustment')
print()
print('2. Historical Data (+520 hours)')
print('   - Python includes "Historical Data Validation" row (520h) in category sum')
print('   - Fix: HistData Validation is separate task, NOT part of category')
print()
print('3. Calculations (+19 hours)')
print('   - Python includes Business Rules, Member Formula under Calculations')
print('   - Fix: These are separate tasks in different categories')
print()
print('4. Secured Dimensions (+20 hours)')
print('   - Row 81 is a SINGLE TASK with formula E*4, NOT a category header')
print('   - Fix: Remove from category_final_estimate, handle as individual task')
print()
print('5. Management Reports (-52 hours)')
print('   - Row 98 has complex formula: =ROUND(E*0.5,0)*8 + ROUND(E*0.25,0)*12 + ROUND(E*0.25,0)*16')
print('   - Fix: Implement this formula in calculate_task_final_estimate')
print()
print('6. Testing/Training (+80 hours)')
print('   - Python calculation logic appears wrong')
print('   - Fix: Verify tier adjustment and base calculation logic')
print()
print('7. Integrations (+32 hours)')
print('   - Similar issue to Build/Configure - subtask details being summed')
print('   - Fix: Use only base + tier adjustment for category')
print()
print('=' * 80)
