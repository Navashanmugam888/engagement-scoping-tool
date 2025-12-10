"""
Debug tool to compare Excel calculations with Backend calculations
This will help identify where the mismatch occurs
"""

from backend.scoping_engine import ScopingEngine
import json

# Test data - modify this to match your exact test
test_scope_inputs = [
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
    {'name': 'Project Management', 'in_scope': 'YES', 'details': 0}
]

test_roles = [
    "PM USA",
    "PM India",
    "Architect USA",
    "Delivery Lead India",
    "Sr. Delivery Lead India",
    "App Lead USA",
    "App Lead India",
    "App Developer India",
    "Integration Lead USA",
    "Integration Developer India"
]

print("="*80)
print("  BACKEND CALCULATION DEBUG")
print("="*80)
print()

# Run the backend calculation
user_input = {
    'scope_inputs': test_scope_inputs,
    'selected_roles': test_roles
}

engine = ScopingEngine()

# Step 1: Process scope
print("STEP 1: Processing Scope Definition...")
scope_result = engine.process_scope(user_input)

print(f"\n✓ Total Weightage: {scope_result['total_weightage']}")
print(f"✓ Tier: {scope_result['tier']} - {scope_result['tier_name']}")
print(f"✓ Tier Range: {scope_result['tier_range']}")
print(f"✓ Features In Scope: {scope_result['summary']['in_scope_count']}/{len(test_scope_inputs)}")

# Show individual weightages
print("\n" + "-"*80)
print("INDIVIDUAL FEATURE WEIGHTAGES:")
print("-"*80)
for metric in scope_result['metrics']:
    if metric['in_scope'] == 'YES' and metric['weightage'] > 0:
        print(f"  {metric['name']:<45} Weight: {metric['weightage']:>6.1f}  Details: {metric['details']}")

# Step 2: Calculate effort
print("\n" + "="*80)
print("STEP 2: Calculating Effort Estimation...")
effort_result = engine.calculate_effort()

print(f"\n✓ Total Time (Tier-Adjusted): {effort_result['summary']['total_time_hours']} hours")
print(f"✓ Final Estimate: {effort_result['summary']['final_estimate_hours']} hours")
print(f"✓ Duration: {effort_result['summary']['total_days']:.2f} days ({effort_result['summary']['total_months']:.2f} months)")

# Show category breakdown
print("\n" + "-"*80)
print("EFFORT BY CATEGORY:")
print("-"*80)
for category, data in effort_result['categories'].items():
    if isinstance(data, dict):
        print(f"  {category:<45} {data.get('final_estimate', 0):>8.1f} hours")
    else:
        print(f"  {category:<45} {data:>8.1f} hours")

# Step 3: Calculate FTE
print("\n" + "="*80)
print("STEP 3: Calculating FTE Allocation...")
fte_result = engine.calculate_fte_allocation()

print(f"\n✓ Total Role Hours: {fte_result['total_hours']:.2f} hours")
print(f"✓ Total Days: {fte_result['total_days']:.2f} days")
print(f"✓ Total Months: {fte_result['total_months']:.2f} months")

print("\n" + "-"*80)
print("FTE ALLOCATION BY ROLE:")
print("-"*80)
for role, data in fte_result['by_role'].items():
    print(f"  {role:<45} {data['hours']:>8.1f} hours")

print("\n" + "="*80)
print("SUMMARY FOR COMPARISON:")
print("="*80)
print(f"  Total Weightage:        {scope_result['total_weightage']}")
print(f"  Tier:                   {scope_result['tier_name']}")
print(f"  Effort Hours:           {effort_result['summary']['final_estimate_hours']}")
print(f"  FTE Total Hours:        {fte_result['total_hours']:.2f}")
print(f"  Duration (months):      {effort_result['summary']['total_months']:.2f}")
print("="*80)

print("\n✓ Now compare these values with your Excel/UI results!")
print("\nIf there's a mismatch, check:")
print("  1. Are the input values EXACTLY the same?")
print("  2. Are the selected roles EXACTLY the same?")
print("  3. Check individual feature weightages above")
print("  4. Check effort category breakdown above")
