"""
Correct mapping of tasks that have detail-based formulas in Excel
vs tasks that don't
"""

# Tasks that have detail-based Final Estimate formulas (Column F uses Column E)
tasks_with_details_formulas = {
    'Build and Configure FCC': [
        ('Account Alternate Hierarchies', 8),  # C38=8, F38=C38*E38
        ('Multi-Currency', 1),  # C40=1, F40=C40*E40
        ('Reporting Currency', 0.5),  # C41=0.5, F41=C41*E41
        ('Entity Alternate Hierarchies', 4),  # C45=4, F45=C45*E45
        ('Scenario', 1),  # C47=1, F47=C47*E47
        ('Custom Dimensions', 4),  # C49=4, F49=C49*E49
        ('Alternate Hierarchies in Custom Dimensions', 4),  # C50=4, F50=C50*E50
        ('Additional Alias Tables', 1),  # C51=1, F51=C51*E51
    ],
    'Setup Application Features': [
        ('Consolidation Journals', 1),  # Has formula
        ('Journal Templates', 1),  # Has formula
    ],
    'Application Customization': [
        ('Data Forms', 4),  # Has formula (from earlier analysis)
    ],
    'Calculations': [
        ('Business Rules', 8),  # Likely has formula
        ('Member Formula', 1),  # Special formula: ROUND(E*0.5,0)*2 + ...
    ],
    'Security': [
        ('Secured Dimensions', 2),  # Likely has formula
        ('Number of Users', 2),  # Special formula: E*0.2
    ],
    'Historical Data': [
        ('Historical Data Validation', 0),  # Special calculation
        ('Data Validation for Account Alt Hierarchies', 20),  # C86=20, F86=C86*E86
        ('Data Validation for Entity Alt Hierarchies', 20),  # C87=20, F87=C87*E87
        ('Historical Journal Conversion', 20),  # Likely has formula
    ],
    'Integrations': [
        ('Files Based Loads', 16),  # F91=E91*C91
        ('Direct Connect Integrations', 16),  # Has formula
        ('Outbound Integrations', 16),  # Has formula
        ('Pipeline', 16),  # Has formula
        ('Custom Scripting', 16),  # Has formula
    ],
    'Reporting': [
        ('Management Reports', 8),  # Has formula
        ('Consolidation Reports', 4),  # Has formula
        ('Consolidation Journal Reports', 4),  # F100=E100*C100
        ('Intercompany Reports', 8),  # Has formula
        ('Task Manager Reports', 4),  # Has formula
        ('Enterprise Journal Reports', 4),  # Has formula
        ('Smart View Reports', 8),  # Has formula
    ],
    'Automations': [
        ('Automated Data loads', 16),  # Has formula
        ('Automated Consolidations', 8),  # Has formula
        ('Backup and Archival', 12),  # Has formula
        ('Metadata Import', 16),  # Has formula
    ],
    'Testing/Training': [
        ('Unit Testing', 40),  # Has formula
        ('UAT', 40),  # Has formula
        ('SIT', 16),  # Has formula
        ('Parallel Testing', 40),  # Has formula (with Details multiplier)
        ('User Training', 16),  # Has formula
    ],
}

# Tasks that DO NOT have detail formulas (column F is empty or not detail-based)
tasks_without_details_formulas = {
    'Build and Configure FCC': [
        ('Application Configuration', 2),  # No formula
        ('Account', 16),  # No formula - Base only
        ('Rationalization of CoA', 24),  # No formula
        ('Data Source', 0.5),  # No formula
        ('Entity', 8),  # No formula - Base only
        ('Entity Redesign', 8),  # No formula
        ('Movement', 4),  # No formula
        ('Multi-GAAP', 2),  # No formula - Base only
    ],
}

print('Tasks WITH detail formulas (these multiply by Details):')
for category, tasks in tasks_with_details_formulas.items():
    print(f'\n{category}:')
    for task, base_hours in tasks:
        print(f'  {task}: {base_hours}')

print('\n\n' + '='*80)
print('Tasks WITHOUT detail formulas (these contribute 0):')
for category, tasks in tasks_without_details_formulas.items():
    print(f'\n{category}:')
    for task, base_hours in tasks:
        print(f'  {task}: {base_hours}')

print('\n\n' + '='*80)
print('CALCULATION LOGIC:')
print('Final Estimate for task = base_hours * details (if has formula)')
print('Final Estimate for task = 0 (if no formula)')
print('Final Estimate for category = tier-adjusted base + SUM(task Final Estimates)')
