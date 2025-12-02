"""
Manual calculation based on your image data to understand Excel's logic
"""

print("=== MANUAL EFFORT CALCULATION FROM EXCEL LOGIC ===")
print()

# Your image data
scope_inputs = {
    'Account': 2000,
    'Account Alternate Hierarchies': 2,
    'Multi-Currency': 5,
    'Reporting Currency': 2,
    'Entity': 25,
    'Entity Alternate Hierarchies': 2,
    'Scenario': 2,
    'Multi-GAAP': 1,
    'Custom Dimensions': 2,
    'Alternate Hierarchies in Custom Dimensions': 2,
    'Additional Alias Tables': 1,
    'Consolidation Journals': 0,  # YES but 0 details
    'Journal Templates': 1,
    'Elimination': 0,
    'Business Rules': 3,
    'Member Formula': 20,
    'Data Forms': 5,
    'Ratios': 0,
    'Secured Dimensions': 1,
    'Number of Users': 20,
    'Historical Data Validation': 2,
    'Data Validation for Account Alt Hierarchies': 0,
    'Data Validation for Entity Alt Hierarchies': 0,
    'Historical Journal Conversion': 0,
    'Files Based Loads': 2,
    'Direct Connect Integrations': 1,
    'Outbound Integrations': 0,
    'Pipeline': 0,
    'Custom Scripting': 2,
    'Management Reports': 5,
    'Consolidation Reports': 0,
    'Consolidation Journal Reports': 1,
    'Intercompany Reports': 1,
    'Task Manager Reports': 0,
    'Enterprise Journal Reports': 0,
    'Smart View Reports': 3,
    'Automated Data loads': 0,
    'Automated Consolidations': 0,
    'Backup and Archival': 0,
    'Metadata Import': 0,
    'Unit Testing': 0,
    'UAT': 0,
    'SIT': 0,
    'Parallel Testing': 3,
    'User Training': 0,
    'Go Live': 0,
    'Hypercare': 0,
    'RTM': 0,
    'Design Document': 0,
    'System Configuration Document': 0,
    'Admin Desktop Procedures': 0,
    'End User Desktop Procedures': 0,
}

# From effort_template.py base hours
base_hours = {
    'Build and Configure FCC': {
        'Account': 16,
        'Account Alternate Hierarchies': 8,
        'Multi-Currency': 1,
        'Reporting Currency': 0.5,
        'Entity': 8,
        'Entity Alternate Hierarchies': 4,
        'Scenario': 1,
        'Multi-GAAP': 2,
        'Custom Dimensions': 4,
        'Alternate Hierarchies in Custom Dimensions': 4,
        'Additional Alias Tables': 1,
    },
    'Setup Application Features': {
        'Consolidation Journals': 1,
        'Journal Templates': 1,
        'Elimination': 0.5,
    },
    'Application Customization': {
        'Data Forms': 4,
    },
    'Calculations': {
        'Business Rules': 8,
        'Member Formula': 1,
        'Ratios': 4,
    },
    'Security': {
        'Secured Dimensions': 2,
        'Number of Users': 2,
    },
    'Historical Data': {
        'Historical Data Validation': 0,  # Calculated
        'Data Validation for Account Alt Hierarchies': 20,
        'Data Validation for Entity Alt Hierarchies': 20,
        'Historical Journal Conversion': 20,
    },
    'Integrations': {
        'Files Based Loads': 16,
        'Direct Connect Integrations': 16,
        'Outbound Integrations': 16,
        'Pipeline': 16,
        'Custom Scripting': 16,
    },
    'Reporting': {
        'Management Reports': 8,
        'Consolidation Reports': 4,
        'Consolidation Journal Reports': 4,
        'Intercompany Reports': 8,
        'Task Manager Reports': 4,
        'Enterprise Journal Reports': 4,
        'Smart View Reports': 8,
    },
}

print("Let me check the Excel formulas for task-level Final Estimate calculation...")
print()
print("Looking at your expected 1892.5 hours, this suggests:")
print("- The calculation is NOT multiplying task base hours by detail values for all tasks")
print("- Some tasks have special formulas")
print()

engagement_weightage = 141.0  # From your previous run

print(f"Engagement Weightage: {engagement_weightage}")
print("Tier 3 - Enhanced Scope (100-150 range)")
print()
print("Expected totals from your image:")
print("  Hours: 1892.5")
print("  Days: 236.5625")
print("  Months: 7.88 (approximately)")
print()

# Verify Days and Months calculation
days = 1892.5 / 8
months = days / 30

print(f"Verification:")
print(f"  1892.5 / 8 = {days}")
print(f"  {days} / 30 = {round(months, 2)}")
print()
print("This matches! So the issue is calculating the 1892.5 hours correctly")
