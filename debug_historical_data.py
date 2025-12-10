"""
Add detailed debug logging to see Historical Data calculation
"""

from backend.scoping_engine import ScopingEngine
import json

test_scope_inputs = [
    {'name': 'Historical Data Validation', 'in_scope': 'YES', 'details': 2},
    {'name': 'Data Validation for Account Alt Hierarchies', 'in_scope': 'YES', 'details': 0},
    {'name': 'Data Validation for Entity Alt Hierarchies', 'in_scope': 'YES', 'details': 0},
    {'name': 'Historical Journal Conversion', 'in_scope': 'YES', 'details': 0},
]

# Add all other items as NO
other_items = [
    'Account', 'Account Alternate Hierarchies', 'Rationalization of CoA', 'Multi-Currency',
    'Reporting Currency', 'Entity', 'Entity Redesign', 'Entity Alternate Hierarchies',
    'Scenario', 'Multi-GAAP', 'Custom Dimensions', 'Alternate Hierarchies in Custom Dimensions',
    'Additional Alias Tables', 'Elimination', 'Custom Elimination Requirement',
    'Consolidation Journals', 'Journal Templates', 'Parent Currency Journals',
    'Ownership Management', 'Enhanced Organization by Period', 'Equity Pickup',
    'Partner Elimination', 'Configurable Consolidation Rules', 'Cash Flow',
    'Supplemental Data Collection', 'Enterprise Journals', 'Approval Process',
    'Historic Overrides', 'Task Manager', 'Audit', 'Data Forms', 'Dashboards',
    'Business Rules', 'Member Formula', 'Ratios', 'Custom KPIs', 'Secured Dimensions',
    'Number of Users', 'Files Based Loads', 'Direct Connect Integrations',
    'Outbound Integrations', 'Pipeline', 'Custom Scripting', 'Management Reports',
    'Consolidation Reports', 'Consolidation Journal Reports', 'Intercompany Reports',
    'Task Manager Reports', 'Enterprise Journal Reports', 'Smart View Reports',
    'Automated Data loads', 'Automated Consolidations', 'Backup and Archival',
    'Metadata Import', 'Unit Testing', 'UAT', 'SIT', 'Parallel Testing',
    'User Training', 'Go Live', 'Hypercare', 'RTM', 'Design Document',
    'System Configuration Document', 'Admin Desktop Procedures',
    'End User Desktop Procedures', 'Project Management'
]

for item in other_items:
    test_scope_inputs.append({'name': item, 'in_scope': 'NO', 'details': 0})

user_input = {
    'scope_inputs': test_scope_inputs,
    'selected_roles': ['PM USA']
}

engine = ScopingEngine()
scope_result = engine.process_scope(user_input)
effort_result = engine.calculate_effort()

print("="*80)
print("HISTORICAL DATA CATEGORY DEBUG")
print("="*80)

# Check Historical Data category
hist_data_cat = effort_result['categories'].get('Historical Data', {})

print(f"\nHistorical Data Category:")
print(f"  base_hours: {hist_data_cat.get('base_hours', 0)}")
print(f"  final_estimate: {hist_data_cat.get('final_estimate', 0)}")
print(f"  in_days: {hist_data_cat.get('in_days', 0)}")

print(f"\n  Tasks in Historical Data:")
for task in hist_data_cat.get('tasks', []):
    print(f"    - {task['name']}")
    print(f"      in_scope: {task['in_scope']}")
    print(f"      details: {task['details']}")
    print(f"      base_hours: {task['base_hours']}")
    print(f"      final_estimate: {task['final_estimate']}")

# Calculate manually
print(f"\nManual Calculation:")
print(f"  Historical Data Validation details: 2")
print(f"  Formula: (15 + (2+1)*10)*8 = (15 + 30)*8 = 45*8 = 360")

hist_data_val_estimate = (15 + (2+1)*10)*8
print(f"  Historical Data Validation estimate: {hist_data_val_estimate}")

# Other tasks reuse the details=2 value
data_val_acc_estimate = 12 * 8 * 2  # 12 * 8 * details
data_val_ent_estimate = 12 * 8 * 2  # 12 * 8 * details  
hist_journ_estimate = 8 * 2  # 8 * details

print(f"  Data Validation for Account Alt: 12*8*2 = {data_val_acc_estimate}")
print(f"  Data Validation for Entity Alt: 12*8*2 = {data_val_ent_estimate}")
print(f"  Historical Journal Conversion: 8*2 = {hist_journ_estimate}")

task_sum = hist_data_val_estimate + data_val_acc_estimate + data_val_ent_estimate + hist_journ_estimate
print(f"  Sum of tasks: {task_sum}")

# Category base (engagement weightage affects this)
print(f"\n  Engagement Weightage: {scope_result['total_weightage']}")
print(f"  Category base_hours: {hist_data_cat.get('base_hours', 0)}")
print(f"  Expected final_estimate: base + tasks = {hist_data_cat.get('base_hours', 0)} + {task_sum} = {hist_data_cat.get('base_hours', 0) + task_sum}")
print(f"  Actual final_estimate: {hist_data_cat.get('final_estimate', 0)}")

# Check if they match
expected = hist_data_cat.get('base_hours', 0) + task_sum
actual = hist_data_cat.get('final_estimate', 0)
if abs(expected - actual) < 0.01:
    print(f"\n  ✓ MATCH: Calculation is correct!")
else:
    print(f"\n  ✗ MISMATCH: Expected {expected} but got {actual}")
    print(f"  Difference: {actual - expected}")
