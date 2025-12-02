#!/usr/bin/env python
"""
Debug Historical Data Validation calculation
"""
import sys
sys.path.insert(0, '.')

from backend.core.effort_calculator import EffortCalculator
from backend.core.scope_processor import ScopeDefinitionProcessor

scope_inputs = [
    {'name': 'Historical Data Validation', 'in_scope': 'YES', 'details': 2},
]

user_input = {
    'scope_inputs': scope_inputs,
    'selected_roles': ['PM USA']
}

processor = ScopeDefinitionProcessor()
scope_result = processor.process_user_input(user_input)

# Check what metrics we have
print("=" * 80)
print("SCOPE METRICS")
print("=" * 80)
for metric in scope_result['metrics']:
    print(f"Name: {metric['name']}, In Scope: {metric['in_scope']}, Details: {metric.get('details', 0)}")

# Now check the calculator
calc = EffortCalculator(scope_result)

# Check lookup functions
print("\n" + "=" * 80)
print("CALCULATOR CHECKS")
print("=" * 80)
print(f"Lookup inscope('Historical Data Validation'): {calc.lookup_inscope('Historical Data Validation')}")
print(f"Lookup details('Historical Data Validation'): {calc.lookup_details('Historical Data Validation')}")

# Calculate the task
task_result = calc.calculate_task_final_estimate('Historical Data Validation')
print(f"Calculate task final estimate('Historical Data Validation'): {task_result}")
print(f"Expected: 360 (from formula = (15 + (2+1)*10) * 8)")
