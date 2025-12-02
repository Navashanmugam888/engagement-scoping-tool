import sys
sys.path.insert(0, '.')

from backend.core.effort_calculator import EffortCalculator
from backend.core.scope_processor import ScopeDefinitionProcessor
from test_image_data_simple import scope_inputs, user_input

processor = ScopeDefinitionProcessor()
scope_result = processor.process_user_input(user_input)

calc = EffortCalculator(scope_result)
effort_estimation = calc.calculate_effort()

total_hours = sum(cat_data.get('final_estimate', 0) for cat_data in effort_estimation.values())
total_days = total_hours / 8
total_months = total_days / 30

print(f"\nTOTAL EFFORT ESTIMATION:")
print(f"  Total Hours: {total_hours:.1f}")
print(f"  Total Days (Hours/8): {total_days:.1f}")
print(f"  Total Months (Days/30): {total_months:.2f}")

print(f"\nExpected:")
print(f"  Total Hours: 1892.5")
print(f"  Total Days: 236.5625")
print(f"  Total Months: 7.89")

print(f"\nMatch: {'✓ YES' if abs(total_hours - 1892.5) < 0.1 else '✗ NO - Gap: ' + str(1892.5 - total_hours)}")
