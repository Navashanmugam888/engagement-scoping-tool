#!/usr/bin/env python
"""
Verify that in_scope_flag is correctly used in effort calculation
"""
import sys
sys.path.insert(0, '.')

from backend.core.effort_calculator import EffortCalculator
from backend.core.scope_processor import ScopeDefinitionProcessor

# Test data with mix of in/out of scope items
scope_inputs = [
    {'name': 'Data Forms', 'in_scope': 'YES', 'details': 5},
    {'name': 'Dashboards', 'in_scope': 'NO', 'details': 3},
    {'name': 'Business Rules', 'in_scope': 'YES', 'details': 3},
]

user_input = {
    'scope_inputs': scope_inputs,
    'selected_roles': ['PM USA']
}

processor = ScopeDefinitionProcessor()
scope_result = processor.process_user_input(user_input)

print("=" * 100)
print("VERIFICATION: In Scope Flag in Scope Definition")
print("=" * 100)
for metric in scope_result['metrics']:
    if metric['name'] in ['Data Forms', 'Dashboards', 'Business Rules']:
        print(f"{metric['name']:30s} | in_scope={metric['in_scope']:3s} | in_scope_flag={metric['in_scope_flag']} | details={metric['details']}")

calc = EffortCalculator(scope_result)

print("\n" + "=" * 100)
print("VERIFICATION: Effort Calculator lookup_inscope()")
print("=" * 100)
for task in ['Data Forms', 'Dashboards', 'Business Rules']:
    inscope = calc.lookup_inscope(task)
    details = calc.lookup_details(task)
    print(f"{task:30s} | lookup_inscope()={inscope:3s} | lookup_details()={details}")

print("\n" + "=" * 100)
print("VERIFICATION: Task Final Estimates")
print("=" * 100)
for task in ['Data Forms', 'Dashboards', 'Business Rules']:
    estimate = calc.calculate_task_final_estimate(task)
    print(f"{task:30s} | Final Estimate = {estimate:7.1f} hours")
    if task == 'Dashboards':
        print(f"  (Should be 0 because in_scope_flag=0, even though details=3)")
