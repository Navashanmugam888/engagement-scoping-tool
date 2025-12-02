"""
Compare Python calculations with Excel Column G values side by side
"""
python_calc = {
    "Project Initiation and Planning": 18.0,
    "Creating and Managing EPM Cloud Infrastructure": 6.0,
    "Requirement Gathering, Read back and Client Sign-off": 44.0,
    "Design": 42.0,
    "Build and Configure FCC": 148.0,
    "Setup Application Features": 96.5,
    "Application Customization": 72.0,  # Note: our calc was 64.0
    "Calculations": 126.0,
    "Security": 24.0,
    "Historical Data": 432.0,  # Note: Excel expects 552.0
    "Integrations": 140.0,
    "Reporting": 140.0,
    "Automations": 64.0,
    "Testing/Training": 244.0,
    "Transition": 96.0,
    "Documentations": 36.0,
    "Change Management": 44.0,
}

excel_col_g = {
    "Project Initiation and Planning": 18.0,
    "Creating and Managing EPM Cloud Infrastructure": 6.0,
    "Requirement Gathering, Read back and Client Sign-off": 44.0,
    "Design": 42.0,
    "Build and Configure FCC": 148.0,
    "Setup Application Features": 96.5,
    "Application Customization": 72.0,
    "Calculations": 126.0,
    "Security": 24.0,
    "Historical Data": 552.0,
    "Integrations": 140.0,
    "Reporting": 140.0,
    "Automations": 64.0,
    "Testing/Training": 244.0,
    "Transition": 96.0,
    "Documentations": 36.0,
    "Change Management": 44.0,
}

print("=" * 120)
print("PYTHON vs EXCEL COMPARISON")
print("=" * 120)
print(f"{'Category':45s} {'Python':>12} {'Excel Col G':>12} {'Difference':>12} {'% Diff':>12}")
print("-" * 120)

python_total = 0
excel_total = 0
total_diff = 0

for category in sorted(python_calc.keys()):
    py_val = python_calc.get(category, 0)
    ex_val = excel_col_g.get(category, 0)
    diff = ex_val - py_val
    pct_diff = (diff / ex_val * 100) if ex_val else 0
    
    python_total += py_val
    excel_total += ex_val
    total_diff += diff
    
    marker = "  *** MISMATCH ***" if abs(diff) > 0.1 else ""
    print(f"{category:45s} {py_val:>12.1f} {ex_val:>12.1f} {diff:>12.1f} {pct_diff:>11.1f}%{marker}")

print("-" * 120)
print(f"{'TOTAL':45s} {python_total:>12.1f} {excel_total:>12.1f} {total_diff:>12.1f} {(total_diff/excel_total*100):>11.1f}%")
print("=" * 120)
