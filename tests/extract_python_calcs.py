#!/usr/bin/env python
"""Extract Python calculations for comparison with Excel"""

import json
import sys
sys.path.insert(0, '.')

# Create sample input that matches your test data
scope_result = {
    'metrics': [
        {'name': 'Account', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Account Alternate Hierarchies', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 2},
        {'name': 'Multi-Currency', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Reporting Currency', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Entity', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Entity Alternate Hierarchies', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Scenario', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Multi-GAAP', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Custom Dimensions', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 2},
        {'name': 'Alternate Hierarchies in Custom Dimensions', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Additional Alias Tables', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 2},
        {'name': 'Journal Templates', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 2},
        {'name': 'Business Rules', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 2},
        {'name': 'Member Formula', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 4},
        {'name': 'Secured Dimensions', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Number of Users', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 20},
        {'name': 'Historical Data Validation', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 4},
        {'name': 'Data Validation for Account Alt Hierarchies', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Data Validation for Entity Alt Hierarchies', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Files Based Loads', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Direct Connect Integrations', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Outbound Integrations', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Pipeline', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Custom Scripting', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Management Reports', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 4},
        {'name': 'Consolidation Reports', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Consolidation Journal Reports', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Intercompany Reports', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 1},
        {'name': 'Task Manager Reports', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Enterprise Journal Reports', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 0},
        {'name': 'Smart View Reports', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 2},
        {'name': 'Parallel Testing', 'in_scope_flag': 1, 'in_scope': 'YES', 'details': 2},
    ],
    'total_weightage': 141.0,
    'tier': 3,
    'tier_name': 'Tier 3'
}

from backend.core.effort_calculator import EffortCalculator

calc = EffortCalculator(scope_result)
effort = calc.calculate_effort()
summary = calc.generate_summary(effort)

# Print just the category totals
print('PYTHON CALCULATIONS - CATEGORY FINAL ESTIMATES')
print('=' * 80)
for cat, data in effort.items():
    print('{:40s}: {:8.1f}'.format(cat, data['final_estimate']))

print()
print('SUMMARY:')
print(json.dumps(summary, indent=2))
