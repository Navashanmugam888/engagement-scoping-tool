"""
Interactive Test UI for Scoping Tool Backend
Allows manual testing of scope inputs and generates reports
"""

from backend.scoping_engine import ScopingEngine
from backend.config import AVAILABLE_ROLES
from datetime import datetime
import json


def print_header(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def get_yes_no(prompt):
    """Get YES/NO input"""
    while True:
        response = input(f"{prompt} (YES/NO): ").strip().upper()
        if response in ['YES', 'NO', 'Y', 'N']:
            return 'YES' if response in ['YES', 'Y'] else 'NO'
        print("Invalid input. Please enter YES or NO.")


def get_number(prompt, allow_zero=True):
    """Get numeric input"""
    while True:
        try:
            value = input(f"{prompt}: ").strip()
            if not value and allow_zero:
                return 0
            num = int(value)
            if num < 0:
                print("Please enter a positive number.")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter a number.")


def select_roles():
    """Interactive role selection"""
    print_header("SELECT IMPLEMENTATION ROLES")
    print("\nAvailable Roles:")
    for i, role in enumerate(AVAILABLE_ROLES, 1):
        print(f"  {i:2d}. {role}")
    
    print("\nEnter role numbers separated by commas (e.g., 1,3,5)")
    print("Or press Enter to use default: PM USA, PM India, Architect USA")
    
    while True:
        selection = input("\nYour selection: ").strip()
        
        if not selection:
            return ['PM USA', 'PM India', 'Architect USA']
        
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            if all(1 <= i <= len(AVAILABLE_ROLES) for i in indices):
                return [AVAILABLE_ROLES[i-1] for i in indices]
            else:
                print(f"Please enter numbers between 1 and {len(AVAILABLE_ROLES)}")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")


def input_scope_quick():
    """Quick test mode with sample data matching Engagement Scoping Tool - FCC.xlsx"""
    print_header("QUICK TEST MODE")
    print("\nUsing sample scope configuration from FCC Implementation Scope:")
    print("  • Account: YES")
    print("  • Multi-Currency: YES (details: 5)")
    print("  • Reporting Currency: YES (details: 2)")
    print("  • Entity: YES (details: 3)")
    print("  • Consolidation Journals: YES")
    print("  • Cash Flow: YES")
    print("  • All other features: NO")
    
    input("\nPress Enter to continue...")
    
    scope_inputs = [
        # DIMENSIONS
        {'name': 'Account', 'in_scope': 'YES', 'details': 0},
        {'name': 'Account Alternate Hierarchies', 'in_scope': 'NO', 'details': 0},
        {'name': 'Rationalization of CoA', 'in_scope': 'NO', 'details': 0},
        {'name': 'Multi-Currency', 'in_scope': 'YES', 'details': 5},
        {'name': 'Reporting Currency', 'in_scope': 'YES', 'details': 2},
        {'name': 'Entity', 'in_scope': 'YES', 'details': 3},
        {'name': 'Entity Redesign', 'in_scope': 'NO', 'details': 0},
        {'name': 'Entity Alternate Hierarchies', 'in_scope': 'NO', 'details': 0},
        {'name': 'Scenario', 'in_scope': 'NO', 'details': 0},
        {'name': 'Multi-GAAP', 'in_scope': 'NO', 'details': 0},
        {'name': 'Custom Dimensions', 'in_scope': 'NO', 'details': 0},
        {'name': 'Alternate Hierarchies in Custom Dimensions', 'in_scope': 'NO', 'details': 0},
        {'name': 'Additional Alias Tables', 'in_scope': 'NO', 'details': 0},
        
        # APPLICATION FEATURES
        {'name': 'Elimination', 'in_scope': 'NO', 'details': 0},
        {'name': 'Custom Elimination Requirement', 'in_scope': 'NO', 'details': 0},
        {'name': 'Consolidation Journals', 'in_scope': 'YES', 'details': 0},
        {'name': 'Journal Templates', 'in_scope': 'NO', 'details': 0},
        {'name': 'Parent Currency Journals', 'in_scope': 'NO', 'details': 0},
        {'name': 'Ownership Management', 'in_scope': 'NO', 'details': 0},
        {'name': 'Enhanced Organization by Period', 'in_scope': 'NO', 'details': 0},
        {'name': 'Equity Pickup', 'in_scope': 'NO', 'details': 0},
        {'name': 'Partner Elimination', 'in_scope': 'NO', 'details': 0},
        {'name': 'Configurable Consolidation Rules', 'in_scope': 'NO', 'details': 0},
        {'name': 'Cash Flow', 'in_scope': 'YES', 'details': 0},
        {'name': 'Supplemental Data Collection', 'in_scope': 'NO', 'details': 0},
        {'name': 'Enterprise Journals', 'in_scope': 'NO', 'details': 0},
        {'name': 'Approval Process', 'in_scope': 'NO', 'details': 0},
        {'name': 'Historic Overrides', 'in_scope': 'NO', 'details': 0},
        {'name': 'Task Manager', 'in_scope': 'NO', 'details': 0},
        {'name': 'Audit', 'in_scope': 'NO', 'details': 0},
        
        # APPLICATION CUSTOMIZATION
        {'name': 'Data Forms', 'in_scope': 'NO', 'details': 0},
        {'name': 'Dashboards', 'in_scope': 'NO', 'details': 0},
        
        # CALCULATIONS
        {'name': 'Business Rules', 'in_scope': 'NO', 'details': 0},
        {'name': 'Member Formula', 'in_scope': 'NO', 'details': 0},
        {'name': 'Ratios', 'in_scope': 'NO', 'details': 0},
        {'name': 'Custom KPIs', 'in_scope': 'NO', 'details': 0},
        
        # SECURITY
        {'name': 'Secured Dimensions', 'in_scope': 'NO', 'details': 0},
        {'name': 'Number of Users', 'in_scope': 'NO', 'details': 0},
        
        # HISTORICAL DATA
        {'name': 'Historical Data Validation', 'in_scope': 'NO', 'details': 0},
        {'name': 'Data Validation for Account Alt Hierarchies', 'in_scope': 'NO', 'details': 0},
        {'name': 'Data Validation for Entity Alt Hierarchies', 'in_scope': 'NO', 'details': 0},
        {'name': 'Historical Journal Conversion', 'in_scope': 'NO', 'details': 0},
        
        # INTEGRATIONS
        {'name': 'Files Based Loads', 'in_scope': 'NO', 'details': 0},
        {'name': 'Direct Connect Integrations', 'in_scope': 'NO', 'details': 0},
        {'name': 'Outbound Integrations', 'in_scope': 'NO', 'details': 0},
        {'name': 'Pipeline', 'in_scope': 'NO', 'details': 0},
        {'name': 'Custom Scripting', 'in_scope': 'NO', 'details': 0},
        
        # REPORTING
        {'name': 'Management Reports', 'in_scope': 'NO', 'details': 0},
        {'name': 'Consolidation Reports', 'in_scope': 'NO', 'details': 0},
        {'name': 'Consolidation Journal Reports', 'in_scope': 'NO', 'details': 0},
        {'name': 'Intercompany Reports', 'in_scope': 'NO', 'details': 0},
        {'name': 'Task Manager Reports', 'in_scope': 'NO', 'details': 0},
        {'name': 'Enterprise Journal Reports', 'in_scope': 'NO', 'details': 0},
        {'name': 'Smart View Reports', 'in_scope': 'NO', 'details': 0},
        
        # AUTOMATIONS
        {'name': 'Automated Data loads', 'in_scope': 'NO', 'details': 0},
        {'name': 'Automated Consolidations', 'in_scope': 'NO', 'details': 0},
        {'name': 'Backup and Archival', 'in_scope': 'NO', 'details': 0},
        {'name': 'Metadata Import', 'in_scope': 'NO', 'details': 0},
        
        # TESTING/TRAINING
        {'name': 'Unit Testing', 'in_scope': 'NO', 'details': 0},
        {'name': 'UAT', 'in_scope': 'NO', 'details': 0},
        {'name': 'SIT', 'in_scope': 'NO', 'details': 0},
        {'name': 'Parallel Testing', 'in_scope': 'NO', 'details': 0},
        {'name': 'User Training', 'in_scope': 'NO', 'details': 0},
        
        # TRANSITION
        {'name': 'Go Live', 'in_scope': 'NO', 'details': 0},
        {'name': 'Hypercare', 'in_scope': 'NO', 'details': 0},
        
        # DOCUMENTATIONS
        {'name': 'RTM', 'in_scope': 'NO', 'details': 0},
        {'name': 'Design Document', 'in_scope': 'NO', 'details': 0},
        {'name': 'System Configuration Document', 'in_scope': 'NO', 'details': 0},
        
        # CHANGE MANAGEMENT
        {'name': 'Admin Desktop Procedures', 'in_scope': 'NO', 'details': 0},
        {'name': 'End User Desktop Procedures', 'in_scope': 'NO', 'details': 0},
        
        # PROJECT MANAGEMENT
        {'name': 'Project Management', 'in_scope': 'NO', 'details': 0}
    ]
    
    return scope_inputs


def input_scope_interactive():
    """Interactive mode - input all metrics from Scope Definition"""
    print_header("INTERACTIVE MODE")
    print("\nYou will be asked about each feature.")
    print("For features requiring details, enter a number (0-50 typically).")
    print("\nTip: Enter 'q' at any time to quit.\n")
    
    # Metrics organized by section with hierarchy - from Engagement Scoping Tool - FCC.xlsx
    # Format: (metric_name, requires_details, is_subsection, section_name)
    # True = requires_details (has [Details] in formula), False = YES/NO only
    
    metrics_structure = [
        # DIMENSIONS
        ('Dimensions', None, True, 'DIMENSIONS'),
        ('Account', True, False, 'Dimensions'),
        ('Account Alternate Hierarchies', True, False, 'Dimensions'),
        ('Rationalization of CoA', False, False, 'Dimensions'),
        ('Multi-Currency', True, False, 'Dimensions'),
        ('Reporting Currency', True, False, 'Dimensions'),
        ('Entity', True, False, 'Dimensions'),
        ('Entity Redesign', False, False, 'Dimensions'),
        ('Entity Alternate Hierarchies', True, False, 'Dimensions'),
        ('Scenario', True, False, 'Dimensions'),
        ('Multi-GAAP', False, False, 'Dimensions'),
        ('Custom Dimensions', True, False, 'Dimensions'),
        ('Alternate Hierarchies in Custom Dimensions', True, False, 'Dimensions'),
        ('Additional Alias Tables', True, False, 'Dimensions'),
        
        # APPLICATION FEATURES
        ('Application Features', None, True, 'APPLICATION FEATURES'),
        ('Elimination', False, False, 'Application Features'),
        ('Custom Elimination Requirement', False, False, 'Application Features'),
        ('Consolidation Journals', False, False, 'Application Features'),
        ('Journal Templates', True, False, 'Application Features'),
        ('Parent Currency Journals', False, False, 'Application Features'),
        ('Ownership Management', False, False, 'Application Features'),
        ('Enhanced Organization by Period', False, False, 'Application Features'),
        ('Equity Pickup', False, False, 'Application Features'),
        ('Partner Elimination', False, False, 'Application Features'),
        ('Configurable Consolidation Rules', False, False, 'Application Features'),
        ('Cash Flow', False, False, 'Application Features'),
        ('Supplemental Data Collection', False, False, 'Application Features'),
        ('Enterprise Journals', False, False, 'Application Features'),
        ('Approval Process', False, False, 'Application Features'),
        ('Historic Overrides', False, False, 'Application Features'),
        ('Task Manager', False, False, 'Application Features'),
        ('Audit', False, False, 'Application Features'),
        
        # APPLICATION CUSTOMIZATION
        ('Application Customization', None, True, 'APPLICATION CUSTOMIZATION'),
        ('Data Forms', True, False, 'Application Customization'),
        ('Dashboards', True, False, 'Application Customization'),
        
        # CALCULATIONS
        ('Calculations', None, True, 'CALCULATIONS'),
        ('Business Rules', True, False, 'Calculations'),
        ('Member Formula', True, False, 'Calculations'),
        ('Ratios', False, False, 'Calculations'),
        ('Custom KPIs', False, False, 'Calculations'),
        
        # SECURITY
        ('Security', None, True, 'SECURITY'),
        ('Secured Dimensions', True, False, 'Security'),
        ('Number of Users', True, False, 'Security'),
        
        # HISTORICAL DATA
        ('Historical Data', None, True, 'HISTORICAL DATA'),
        ('Historical Data Validation', True, False, 'Historical Data'),
        ('Data Validation for Account Alt Hierarchies', False, False, 'Historical Data'),
        ('Data Validation for Entity Alt Hierarchies', False, False, 'Historical Data'),
        ('Historical Journal Conversion', False, False, 'Historical Data'),
        
        # INTEGRATIONS
        ('Integrations', None, True, 'INTEGRATIONS'),
        ('Files Based Loads', True, False, 'Integrations'),
        ('Direct Connect Integrations', True, False, 'Integrations'),
        ('Outbound Integrations', True, False, 'Integrations'),
        ('Pipeline', True, False, 'Integrations'),
        ('Custom Scripting', True, False, 'Integrations'),
        
        # REPORTING
        ('Reporting', None, True, 'REPORTING'),
        ('Management Reports', True, False, 'Reporting'),
        ('Consolidation Reports', True, False, 'Reporting'),
        ('Consolidation Journal Reports', True, False, 'Reporting'),
        ('Intercompany Reports', True, False, 'Reporting'),
        ('Task Manager Reports', True, False, 'Reporting'),
        ('Enterprise Journal Reports', True, False, 'Reporting'),
        ('Smart View Reports', True, False, 'Reporting'),
        
        # AUTOMATIONS
        ('Automations', None, True, 'AUTOMATIONS'),
        ('Automated Data loads', False, False, 'Automations'),
        ('Automated Consolidations', False, False, 'Automations'),
        ('Backup and Archival', False, False, 'Automations'),
        ('Metadata Import', False, False, 'Automations'),
        
        # TESTING/TRAINING
        ('Testing/Training', None, True, 'TESTING/TRAINING'),
        ('Unit Testing', False, False, 'Testing/Training'),
        ('UAT', False, False, 'Testing/Training'),
        ('SIT', False, False, 'Testing/Training'),
        ('Parallel Testing', True, False, 'Testing/Training'),
        ('User Training', False, False, 'Testing/Training'),
        
        # TRANSITION
        ('Transition', None, True, 'TRANSITION'),
        ('Go Live', False, False, 'Transition'),
        ('Hypercare', False, False, 'Transition'),
        
        # DOCUMENTATIONS
        ('Documentations', None, True, 'DOCUMENTATIONS'),
        ('RTM', False, False, 'Documentations'),
        ('Design Document', False, False, 'Documentations'),
        ('System Configuration Document', False, False, 'Documentations'),
        
        # CHANGE MANAGEMENT
        ('Change Management', None, True, 'CHANGE MANAGEMENT'),
        ('Admin Desktop Procedures', False, False, 'Change Management'),
        ('End User Desktop Procedures', False, False, 'Change Management'),
        
        # PROJECT MANAGEMENT
        ('Project Management', None, True, 'PROJECT MANAGEMENT'),
        ('Project Management', False, False, 'Project Management'),
    ]
    
    scope_inputs = []
    current_section = None
    
    for metric_name, requires_details, is_header, section_name in metrics_structure:
        # Print section header if needed
        if is_header and requires_details is None:
            print_header(section_name)
            current_section = section_name
            continue
        
        # Indent subsection items
        indent = "     " if section_name != metric_name else ""
        print(f"\n{indent}{metric_name}:")
        in_scope = get_yes_no(f"{indent}  In Scope?")
        
        details = 0
        if in_scope == 'YES' and requires_details:
            details = get_number(f"{indent}  How many? (0-50, Enter for 0)", allow_zero=True)
        
        scope_inputs.append({
            'name': metric_name,
            'in_scope': in_scope,
            'details': details
        })
    
    return scope_inputs


def display_results(report):
    """Display formatted results"""
    scope = report['scope_definition']
    effort = report['effort_estimation']
    
    print_header("SCOPING RESULTS")
    
    print(f"\n📊 SCOPE DEFINITION")
    print(f"   Total Weightage: {scope['total_weightage']}")
    print(f"   Implementation Tier: {scope['tier']} - {scope['tier_name']}")
    print(f"   Weightage Range: {scope['tier_range'][0]}-{scope['tier_range'][1]}")
    print(f"   Features In Scope: {scope['summary']['in_scope_count']}/{scope['summary']['total_metrics']}")
    
    print(f"\n⏱️  EFFORT ESTIMATION")
    print(f"   Total Time (Tier-Adjusted): {effort['summary']['total_time_hours']} hours")
    print(f"   Final Estimate: {effort['summary']['final_estimate_hours']} hours")
    print(f"   Duration: {effort['summary']['total_days']} days")
    print(f"   Duration: {effort['summary']['total_months']} months")
    
    print(f"\n👥 TEAM")
    print(f"   Selected Roles: {len(scope['selected_roles'])}")
    for role in scope['selected_roles']:
        print(f"     • {role}")
    
    # Show top effort categories
    categories = effort['categories']
    category_efforts = [(name, data['final_estimate']) for name, data in categories.items() if data['final_estimate'] > 0]
    category_efforts.sort(key=lambda x: x[1], reverse=True)
    
    if category_efforts:
        print(f"\n📋 TOP EFFORT CATEGORIES")
        for i, (name, hours) in enumerate(category_efforts[:5], 1):
            print(f"   {i}. {name}: {hours} hours")


def main():
    """Main interactive test UI"""
    print_header("FCC ENGAGEMENT SCOPING TOOL - TEST UI")
    print("\nWelcome to the Interactive Testing Interface!")
    print("\nThis tool helps you test the scoping backend with custom inputs.")
    
    # Select mode
    print("\nSelect test mode:")
    print("  1. Quick Test (pre-configured sample data)")
    print("  2. Interactive Mode (input all 71 metrics)")
    print("  3. Exit")
    
    while True:
        choice = input("\nYour choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    if choice == '3':
        print("\nExiting...")
        return
    
    # Get scope inputs
    if choice == '1':
        scope_inputs = input_scope_quick()
    else:
        scope_inputs = input_scope_interactive()
    
    # Select roles
    selected_roles = select_roles()
    
    # Prepare input
    user_input = {
        'scope_inputs': scope_inputs,
        'selected_roles': selected_roles
    }
    
    # Run scoping engine
    print_header("PROCESSING")
    print("\n⏳ Running scoping engine...")
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f'manual_test_report_{timestamp}.json'
    
    engine = ScopingEngine()
    report = engine.run_complete_workflow(user_input, report_filename)
    
    print("✓ Processing complete!")
    
    # Display results
    display_results(report)
    
    print_header("REPORT SAVED")
    print(f"\n✓ Full report saved to: output/{report_filename}")
    print("\nYou can review the complete JSON report for detailed breakdown.")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
