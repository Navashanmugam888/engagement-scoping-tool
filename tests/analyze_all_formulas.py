"""
Map of tasks with their Excel formulas from Effort Estimation sheet
"""

# Tasks with Final Estimate formulas (Column F has a formula)
tasks_with_formulas = {
    # Build and Configure FCC
    'Account Alternate Hierarchies': ('=C38*E38', 8, 'base * details'),
    'Multi-Currency': ('=C40*E40', 1, 'base * details'),
    'Reporting Currency': ('=C41*E41', 0.5, 'base * details'),
    'Entity Alternate Hierarchies': ('=C45*E45', 4, 'base * details'),
    'Scenario': ('=C47*E47', 1, 'base * details'),
    'Custom Dimensions': ('=C49*E49', 4, 'base * details'),
    'Alternate Hierarchies in Custom Dimensions': ('=C50*E50', 4, 'base * details'),
    'Additional Alias Tables': ('=C51*E51', 1, 'base * details'),
    
    # Setup Application Features
    'Journal Templates': ('=C56*E56', 1, 'base * details'),
    'Configurable Consolidation Rules': ('=C61*E61', 8, 'base * details'),
    
    # Application Customization
    'Data Forms': ('=ROUND(E71*0.5,0)*8 + ROUND(E71*0.25,0)*12 + ROUND(E71*0.25,0)*16', 4, 'complex scaling'),
    'Dashboards': ('=ROUND(E72*0.5,0)*8 + ROUND(E72*0.25,0)*12 + ROUND(E72*0.25,0)*16', 4, 'complex scaling'),
    
    # Calculations
    'Business Rules': ('=ROUND(E75*0.5,0)*8 + ROUND(E75*0.25,0)*12 + ROUND(E75*0.25,0)*16', 8, 'complex scaling'),
    'Member Formula': ('=ROUND(E76*0.5,0)*2 + ROUND(E76*0.25,0)*3 + ROUND(E76*0.25,0)*4', 1, 'complex scaling'),
    'Custom KPIs': ('=ROUND(E78*0.5,0)*2 + ROUND(E78*0.25,0)*4 + ROUND(E78*0.25,0)*4', 2, 'complex scaling'),
    
    # Security
    'Secured Dimensions': ('=E81*4', 2, 'details * 4'),
    'Number of Users': ('=E82*0.2', 2, 'details * 0.2'),
    
    # Historical Data
    'Historical Data Validation': ('=(15 +(E85+1) * 10)*8', 0, 'special formula'),
    'Data Validation for Account Alt Hierarchies': ('=C86*E86', 20, 'base * details'),
    'Data Validation for Entity Alt Hierarchies': ('=C87*E87', 20, 'base * details'),
    'Historical Journal Conversion': ('=C88*E88', 20, 'base * details'),
    
    # Integrations
    'Files Based Loads': ('=E91*C91', 16, 'details * base'),
    'Direct Connect Integrations': ('=E92*C92', 16, 'details * base'),
    'Outbound Integrations': ('=E93*C93', 16, 'details * base'),
    'Pipeline': ('=E94*C94', 16, 'details * base'),
    'Custom Scripting': ('=E95*C95', 16, 'details * base'),
    
    # Reporting
    'Management Reports': ('=ROUND(E98*0.5,0)*8 + ROUND(E98*0.25,0)*12 + ROUND(E98*0.25,0)*16', 8, 'complex scaling'),
    'Consolidation Reports': ('=E99*C99', 4, 'details * base'),
    'Consolidation Journal Reports': ('=E100*C100', 4, 'details * base'),
    'Intercompany Reports': ('=E101*C101', 8, 'details * base'),
    'Task Manager Reports': ('=E102*C102', 4, 'details * base'),
    'Enterprise Journal Reports': ('=E103*C103', 4, 'details * base'),
    'Smart View Reports': ('=E104*C104', 8, 'details * base'),
    
    # Testing/Training
    'Parallel Testing': ('=C116*2', 40, 'base * 2 (fixed from D116)'),
    
    # Note: Row 16 - Prelim FCC User Provisioning has: =IF(E16>50,8,0)
    'Prelim FCC User Provisioning': ('=IF(E16>50,8,0)', 4, 'conditional: if details > 50 then 8 else 0'),
}

# Column E (Details) lookup patterns:
# - Most use: =IF(D[row]="YES",'Scope Definition'!D[col], 0)
# - Some are direct cell references

# Tasks WITHOUT formulas in Column F (contribute 0):
tasks_without_formulas = [
    'Kickoff Meetings',
    'Project Governance',
    'Communication Plan',
    'Resource Allocation',
    'RAID Log',
    'Project Plan',
    'Plan Status Meetings and SteerCo Meeting Schedule',
    'Creating and Setting up Oracle EPM Cloud instances',
    'Requirement Gathering Sessions',
    'Current CoA details',
    'CoA Hierarchies',
    'Current Consolidation Model',
    'Sample Reports',
    'Dimension Details',
    'Develop Requirement Treaceability Matrix',
    'Formal RTM Signoff',
    'Design Document',
    'Key Design Decision Document',
    'Internal Peer Review',
    'Design and KDD Reviews',
    'Design Approval from Client',
    'Application Configuration',
    'Account',
    'Rationalization of CoA',
    'Data Source',
    'Entity',
    'Entity Redesign',
    'Movement',
    'Multi-GAAP',
    'Elimination',
    'Consolidation Journals',
    'Ownership Management',
    'Enhanced Organization by Period',
    'Equity Pickup',
    'Partner Elimination',
    'Cash Flow',
    'Supplemental Data Collection',
    'Enterprise Journals',
    'Approval Process',
    'Historic Overrides',
    'Task Manager',
    'Audit',
    'Ratios',
    'Unit Testing',
    'UAT',
    'SIT',
    'User Training',
    'Go Live',
    'Hypercare',
    'RTM',
    'Design Document',
    'System Configuration Document',
    'Admin Desktop Procedures',
    'End user Desktop Procedures',
    'Automated Data loads',
    'Automated Consolidations',
    'Backup and Archival',
    'Metadata Import',
]

print('TASKS WITH FORMULAS (34 total):')
print()
for task, (formula, base, description) in sorted(tasks_with_formulas.items()):
    print(f'{task:45s} Base={base:4} Formula Type: {description}')

print()
print(f'TASKS WITHOUT FORMULAS ({len(tasks_without_formulas)} total):')
print('These contribute 0 to effort')

print()
print('='*80)
print('KEY FINDINGS:')
print('='*80)
print()
print('1. Complex Scaling (ROUND formula):')
print('   - Data Forms, Dashboards, Business Rules, Management Reports')
print('   - Formula: =ROUND(details*0.5,0)*8 + ROUND(details*0.25,0)*12 + ROUND(details*0.25,0)*16')
print()
print('2. Special Scaling:')
print('   - Secured Dimensions: =details*4')
print('   - Number of Users: =details*0.2')
print('   - Member Formula: =ROUND(E*0.5,0)*2 + ROUND(E*0.25,0)*3 + ROUND(E*0.25,0)*4')
print('   - Custom KPIs: =ROUND(E*0.5,0)*2 + ROUND(E*0.25,0)*4 + ROUND(E*0.25,0)*4')
print()
print('3. Conditional:')
print('   - Prelim FCC User Provisioning: =IF(details>50, 8, 0)')
print()
print('4. Special Calculation:')
print('   - Historical Data Validation: =(15 + (details+1)*10)*8')
print()
print('5. Default:')
print('   - Most tasks: =base*details')
