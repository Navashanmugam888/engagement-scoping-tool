import openpyxl

excel_file = 'C:/Users/NavashanmugamAsokan/Desktop/Projects/Engagement Scoping Tool/documents/Engagement Scoping Tool - FCC.xlsx'

# Load with formulas
wb = openpyxl.load_workbook(excel_file, data_only=False)
ws_scope = wb['Scope Definition']
ws_effort = wb['Effort Estimation']

print('=== CRITICAL FINDINGS ===')
print()
print('1. Scope Definition E103 (Total Weightage):')
print(f'   Formula: {ws_scope["E103"].value}')
print()

print('2. Effort Estimation uses EngagementWeightage variable:')
print('   F5 formula uses: EngagementWeightage as variable')
print('   Meaning: EngagementWeightage must be a named range')
print()

print('3. Named Range Search:')
wb_named = openpyxl.load_workbook(excel_file)
all_names = []
try:
    for defined_name in wb_named.defined_names.definedName:
        all_names.append(f'{defined_name.name}')
        if 'Engagement' in defined_name.name or 'weightage' in defined_name.name.lower():
            print(f'   Found: {defined_name.name} = {defined_name.value}')
except:
    print('   Could not access named ranges')

print()
print('4. Understanding the structure:')
print('   - Scope Definition sheet: E103 = SUM(E6:E102) = Total Weightage')
print('   - Effort Estimation sheet: References EngagementWeightage in formulas')
print('   - EngagementWeightage likely points to: Scope Definition!E103')
print()

print('5. Summary Row 132 in Effort Estimation:')
print('   F132 (Hours): =SUM(G5:G130) = Sum of all Final Estimate rows')
print('   G132 (Days): =F132/8 = Hours / 8')
print('   H132 (Months): =G132/30 = Days / 30')
