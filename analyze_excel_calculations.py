import openpyxl

wb = openpyxl.load_workbook('Engagement Scoping Tool - FCC.xlsx', data_only=True)
ws_effort = wb['Effort Estimation']
ws_scope = wb['Scope Definition']

print("=" * 80)
print("CHECKING HISTORICAL DATA CALCULATIONS IN EXCEL")
print("=" * 80)

# Check what value is in D54 (Historical Data Validation details)
hist_data_details = ws_scope['D54'].value
print(f"\nHistorical Data Validation details (Scope Definition D54): {hist_data_details}")

# Check the calculated values in column F (Final Hours)
print("\n" + "=" * 80)
print("EFFORT ESTIMATION SHEET - Calculated Values:")
print("=" * 80)

print(f"\nRow 86: Data Validation for Account Alt Hierarchies")
print(f"  Column C (Base): {ws_effort['C86'].value}")
print(f"  Column E (Details used): {ws_effort['E86'].value}")
print(f"  Column F (Final Hours): {ws_effort['F86'].value}")

print(f"\nRow 87: Data Validation for Entity Alt Hierarchies")
print(f"  Column C (Base): {ws_effort['C87'].value}")
print(f"  Column E (Details used): {ws_effort['E87'].value}")
print(f"  Column F (Final Hours): {ws_effort['F87'].value}")

print(f"\nRow 88: Historical Journal Conversion")
print(f"  Column C (Base): {ws_effort['C88'].value}")
print(f"  Column E (Details used): {ws_effort['E88'].value}")
print(f"  Column F (Final Hours): {ws_effort['F88'].value}")

print("\n" + "=" * 80)
print("CALCULATION ANALYSIS:")
print("=" * 80)

if ws_effort['F86'].value and ws_effort['E86'].value:
    multiplier_86 = ws_effort['F86'].value / ws_effort['E86'].value
    print(f"\nRow 86: {ws_effort['F86'].value} ÷ {ws_effort['E86'].value} = {multiplier_86}")
    print(f"  This means the multiplier is {multiplier_86}, not {ws_effort['C86'].value}")

if ws_effort['F87'].value and ws_effort['E87'].value:
    multiplier_87 = ws_effort['F87'].value / ws_effort['E87'].value
    print(f"\nRow 87: {ws_effort['F87'].value} ÷ {ws_effort['E87'].value} = {multiplier_87}")
    print(f"  This means the multiplier is {multiplier_87}, not {ws_effort['C87'].value}")

if ws_effort['F88'].value and ws_effort['E88'].value:
    multiplier_88 = ws_effort['F88'].value / ws_effort['E88'].value
    print(f"\nRow 88: {ws_effort['F88'].value} ÷ {ws_effort['E88'].value} = {multiplier_88}")
    print(f"  This means the multiplier is {multiplier_88}, not {ws_effort['C88'].value}")
