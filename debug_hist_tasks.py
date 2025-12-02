import json
from backend.core.scope_processor import ScopeDefinitionProcessor
from backend.core.effort_calculator import EffortCalculator
from backend.data.effort_template import EFFORT_ESTIMATION_TEMPLATE

# Full test data
scope_inputs = [
    # DIMENSIONS
    {'name': 'Account', 'in_scope': 'YES', 'details': 2000},
    {'name': 'Account Alternate Hierarchies', 'in_scope': 'YES', 'details': 2},
    {'name': 'Rationalization of CoA', 'in_scope': 'YES', 'details': 0},
    {'name': 'Multi-Currency', 'in_scope': 'YES', 'details': 5},
    {'name': 'Reporting Currency', 'in_scope': 'YES', 'details': 2},
    {'name': 'Entity', 'in_scope': 'YES', 'details': 25},
    {'name': 'Entity Redesign', 'in_scope': 'NO', 'details': 0},
    {'name': 'Entity Alternate Hierarchies', 'in_scope': 'YES', 'details': 2},
    {'name': 'Scenario', 'in_scope': 'YES', 'details': 2},
    {'name': 'Multi-GAAP', 'in_scope': 'YES', 'details': 0},
    {'name': 'Custom Dimensions', 'in_scope': 'YES', 'details': 2},
    {'name': 'Alternate Hierarchies in Custom Dimensions', 'in_scope': 'YES', 'details': 2},
    {'name': 'Additional Alias Tables', 'in_scope': 'YES', 'details': 1},
    
    # APPLICATION FEATURES
    {'name': 'Elimination', 'in_scope': 'YES', 'details': 0},
    {'name': 'Custom Elimination Requirement', 'in_scope': 'NO', 'details': 0},
    {'name': 'Consolidation Journals', 'in_scope': 'YES', 'details': 0},
    {'name': 'Journal Templates', 'in_scope': 'YES', 'details': 1},
    {'name': 'Parent Currency Journals', 'in_scope': 'YES', 'details': 0},
    {'name': 'Ownership Management', 'in_scope': 'NO', 'details': 0},
    {'name': 'Enhanced Organization by Period', 'in_scope': 'NO', 'details': 0},
    {'name': 'Equity Pickup', 'in_scope': 'NO', 'details': 0},
    {'name': 'Partner Elimination', 'in_scope': 'NO', 'details': 0},
    {'name': 'Configurable Consolidation Rules', 'in_scope': 'NO', 'details': 0},
    {'name': 'Cash Flow', 'in_scope': 'YES', 'details': 0},
    {'name': 'Supplemental Data Collection', 'in_scope': 'NO', 'details': 0},
    {'name': 'Enterprise Journals', 'in_scope': 'NO', 'details': 0},
    {'name': 'Approval Process', 'in_scope': 'YES', 'details': 0},
    {'name': 'Historic Overrides', 'in_scope': 'YES', 'details': 0},
    {'name': 'Task Manager', 'in_scope': 'NO', 'details': 0},
    {'name': 'Audit', 'in_scope': 'YES', 'details': 0},
    
    # APPLICATION CUSTOMIZATION
    {'name': 'Data Forms', 'in_scope': 'YES', 'details': 5},
    {'name': 'Dashboards', 'in_scope': 'NO', 'details': 0},
    
    # CALCULATIONS
    {'name': 'Business Rules', 'in_scope': 'YES', 'details': 3},
    {'name': 'Member Formula', 'in_scope': 'YES', 'details': 20},
    {'name': 'Ratios', 'in_scope': 'YES', 'details': 0},
    {'name': 'Custom KPIs', 'in_scope': 'NO', 'details': 0},
    
    # SECURITY
    {'name': 'Secured Dimensions', 'in_scope': 'YES', 'details': 1},
    {'name': 'Number of Users', 'in_scope': 'YES', 'details': 20},
    
    # HISTORICAL DATA
    {'name': 'Historical Data Validation', 'in_scope': 'YES', 'details': 2},
    {'name': 'Data Validation for Account Alt Hierarchies', 'in_scope': 'YES', 'details': 0},
    {'name': 'Data Validation for Entity Alt Hierarchies', 'in_scope': 'YES', 'details': 0},
    {'name': 'Historical Journal Conversion', 'in_scope': 'YES', 'details': 0},
    
    # INTEGRATIONS
    {'name': 'Files Based Loads', 'in_scope': 'NO', 'details': 0},
    {'name': 'Direct Connect Integrations', 'in_scope': 'YES', 'details': 1},
    {'name': 'Outbound Integrations', 'in_scope': 'NO', 'details': 0},
    {'name': 'Pipeline', 'in_scope': 'NO', 'details': 0},
    {'name': 'Custom Scripting', 'in_scope': 'YES', 'details': 2},
    
    # REPORTING
    {'name': 'Management Reports', 'in_scope': 'YES', 'details': 5},
    {'name': 'Consolidation Reports', 'in_scope': 'NO', 'details': 0},
    {'name': 'Consolidation Journal Reports', 'in_scope': 'YES', 'details': 1},
    {'name': 'Intercompany Reports', 'in_scope': 'YES', 'details': 1},
    {'name': 'Task Manager Reports', 'in_scope': 'NO', 'details': 0},
    {'name': 'Enterprise Journal Reports', 'in_scope': 'NO', 'details': 0},
    {'name': 'Smart View Reports', 'in_scope': 'YES', 'details': 3},
    
    # AUTOMATIONS
    {'name': 'Automated Data loads', 'in_scope': 'YES', 'details': 0},
    {'name': 'Automated Consolidations', 'in_scope': 'YES', 'details': 0},
    {'name': 'Backup and Archival', 'in_scope': 'NO', 'details': 0},
    {'name': 'Metadata Import', 'in_scope': 'NO', 'details': 0},
    
    # TESTING/TRAINING
    {'name': 'Unit Testing', 'in_scope': 'YES', 'details': 0},
    {'name': 'UAT', 'in_scope': 'YES', 'details': 0},
    {'name': 'SIT', 'in_scope': 'YES', 'details': 0},
    {'name': 'Parallel Testing', 'in_scope': 'YES', 'details': 3},
    {'name': 'User Training', 'in_scope': 'YES', 'details': 0},
    
    # TRANSITION
    {'name': 'Go Live', 'in_scope': 'YES', 'details': 0},
    {'name': 'Hypercare', 'in_scope': 'YES', 'details': 0},
    
    # DOCUMENTATIONS
    {'name': 'RTM', 'in_scope': 'YES', 'details': 0},
    {'name': 'Design Document', 'in_scope': 'YES', 'details': 0},
    {'name': 'System Configuration Document', 'in_scope': 'YES', 'details': 0},
    
    # CHANGE MANAGEMENT
    {'name': 'Admin Desktop Procedures', 'in_scope': 'YES', 'details': 0},
    {'name': 'End User Desktop Procedures', 'in_scope': 'YES', 'details': 0},
    
    # PROJECT MANAGEMENT
    {'name': 'Project Management', 'in_scope': 'YES', 'details': 0},
]

user_input = {
    'scope_inputs': scope_inputs,
    'selected_roles': ['PM USA', 'PM India', 'Architect USA']
}

processor = ScopeDefinitionProcessor()
scope_result = processor.process_user_input(user_input)
calc = EffortCalculator(scope_result)

print(f"Total Weightage: {calc.engagement_weightage}")

# Check Historical Data tasks
print("\n\nHistorical Data tasks breakdown:")
hist_data_tasks = EFFORT_ESTIMATION_TEMPLATE["Historical Data"]["tasks"]
total_task_estimate = 0
for task_name in hist_data_tasks:
    task_estimate = calc.calculate_task_final_estimate(task_name)
    print(f"  {task_name}: {task_estimate}")
    total_task_estimate += task_estimate

print(f"\nTotal task estimates: {total_task_estimate}")

# Calculate category
base = 60
category_estimate = calc.calculate_category_final_estimate("Historical Data", base, {task: calc.calculate_task_final_estimate(task) for task in hist_data_tasks})
print(f"Category final estimate (with tier adjustment): {category_estimate}")

# Expected breakdown:
#  F84 = 72 (base + tier adjustment)
#  F85 = 360 (Historical Data Validation)
#  F86 = 40 (Data Validation for Account Alt Hierarchies)
#  F87 = 40 (Data Validation for Entity Alt Hierarchies)
#  F88 = 40 (Historical Journal Conversion)
#  Total = 72 + 360 + 40 + 40 + 40 = 552

print(f"\n\nExpected breakdown:")
print(f"  Category base with tier: 72")
print(f"  Historical Data Validation: 360")
print(f"  Data Validation for Account Alt Hierarchies: 40")
print(f"  Data Validation for Entity Alt Hierarchies: 40")
print(f"  Historical Journal Conversion: 40")
print(f"  Total expected: 552")
