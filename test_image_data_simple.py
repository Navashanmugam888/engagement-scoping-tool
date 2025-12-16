#!/usr/bin/env python
"""
Test with image data without unicode output
"""
import sys
sys.path.insert(0, '.')

from backend.core.effort_calculator import EffortCalculator
from backend.core.scope_processor import ScopeDefinitionProcessor

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

print("\n" + "=" * 80)
print("SCOPE DEFINITION")
print("=" * 80)
print(f"Total Weightage: {scope_result['total_weightage']}")
print(f"Tier: {scope_result['tier_name']}")

calc = EffortCalculator(scope_result)
effort_estimation = calc.calculate_effort()
summary = calc.generate_summary(effort_estimation)

# Compare with expected
categories_effort = {}
for cat_name, cat_data in effort_estimation.items():
    effort = cat_data.get('final_estimate', 0)
    categories_effort[cat_name] = effort

expected = {
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

print("\n" + "=" * 120)
print("Category-by-category comparison (looking for 8-hour gap):")
print("=" * 120)

total_diff = 0
for cat in sorted(categories_effort.keys()):
    py_val = categories_effort.get(cat, 0)
    ex_val = expected.get(cat, 0)
    diff = ex_val - py_val
    total_diff += diff
    marker = "  *** SHORT ***" if diff > 0.1 else ""
    print(f"{cat:45s} {py_val:>12.1f} {ex_val:>12.1f} {diff:>12.1f}{marker}")
