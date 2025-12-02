#!/usr/bin/env python
"""
Check effort breakdown by category
"""
import json
from backend.scoping_engine import ScopingEngine

# Sample data FROM THE IMAGE YOU PROVIDED
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
    {'name': 'Multi-GAAP', 'in_scope': 'YES', 'details': 1},
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
    {'name': 'Files Based Loads', 'in_scope': 'NO', 'details': 2},
    {'name': 'Direct Connect Integrations', 'in_scope': 'YES', 'details': 1},
    {'name': 'Outbound Integrations', 'in_scope': 'NO', 'details': 0},
    {'name': 'Pipeline', 'in_scope': 'NO', 'details': 0},
    {'name': 'Custom Scripting', 'in_scope': 'YES', 'details': 2},
    
    # REPORTING
    {'name': 'Management Reports', 'in_scope': 'YES', 'details': 5},
    {'name': 'Consolidation Reports', 'in_scope': 'NO', 'details': 0},
    {'name': 'Consolidation Journal Reports', 'in_scope': 'YES', 'details': 1},
    {'name': 'Intercompany Reports', 'in_scope': 'YES', 'details': 0},
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

engine = ScopingEngine()
scope_result = engine.process_scope(user_input)
effort_result = engine.calculate_effort()

print("\n" + "=" * 80)
print("CATEGORY BREAKDOWN")
print("=" * 80)

categories = effort_result['categories']
total_hours = 0

for category_name in sorted(categories.keys()):
    category_data = categories[category_name]
    final_est = category_data.get('final_estimate', 0)
    base = category_data.get('base_hours', 0)
    total_hours += final_est
    print(f"{category_name:50s} Base: {base:7.1f}  →  Final: {final_est:7.1f}")

print("=" * 80)
print(f"{'TOTAL':50s}                      Final: {total_hours:7.1f}")
print("=" * 80)
print(f"\nExpected:  1892.5 hours")
print(f"Got:       {total_hours} hours")
print(f"Gap:       {1892.5 - total_hours} hours ({((1892.5 - total_hours) / 1892.5 * 100):.1f}%)")
