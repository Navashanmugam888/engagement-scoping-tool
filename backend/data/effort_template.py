"""
Effort Estimation Template - Default task structure with time allocations
This is the baseline template that gets adjusted based on scope weightage and tier

Test Data Changes (test_image_data_simple.py):
- Multi-GAAP: details changed from 1 to 0
- Data Validation for Account Alt Hierarchies: details changed from 2 to 0
- Data Validation for Entity Alt Hierarchies: details changed from 2 to 0
- Historical Journal Conversion: details changed from 2 to 0
- Intercompany Reports: details changed from 0 to 1

These changes represent adjustments to the engagement scope as per the test scenario.
"""

# Default effort estimation template in hours
# This represents the standard task breakdown for an FCC implementation
EFFORT_ESTIMATION_TEMPLATE = {
    "Project Initiation and Planning": {
        "total": 12,
        "tasks": {
            "Kickoff Meetings": 1,
            "Project Governance": 1,
            "Communication Plan": 1,
            "Resource Allocation": 2,
            "RAID Log": 1,
            "Project Plan": 4,
            "Plan Status Meetings and SteerCo Meeting Schedule": 2,
        }
    },
    "Creating and Managing EPM Cloud Infrastructure": {
        "total": 6,
        "tasks": {
            "Creating and Setting up Oracle EPM Cloud instances": 2,
            "Prelim FCC User Provisioning": 4,
        }
    },
    "Requirement Gathering, Read back and Client Sign-off": {
        "total": 32,
        "tasks": {
            "Requirement Gathering Sessions": 8,
            "Current CoA details": 4,
            "CoA Hierarchies": 4,
            "Current Consolidation Model": 4,
            "Sample Reports": 2,
            "Dimension Details": 4,
            "Develop Requirement Treaceability Matrix": 4,
            "Formal RTM Signoff": 2,
        }
    },
    "Design": {
        "total": 26,
        "tasks": {
            "Design Document": 8,
            "Key Design Decision Document": 8,
            "Internal Peer Review": 4,
            "Design and KDD Reviews": 4,
            "Design Approval from Client": 2,
        }
    },
    "Build and Configure FCC": {
        "total": 88,
        "tasks": {
            "Application Configuration": 2,
            "Account": 16,
            "Account Alternate Hierarchies": 8,
            "Rationalization of CoA": 24,
            "Multi Currency": 1,
            "Reporting Currency": 0.5,
            "Data Source": 0.5,
            "Entity": 8,
            "Entity Redesign": 8,
            "Entity Alternate Hierarchies": 4,
            "Movement": 4,
            "Scenario": 1,
            "Multi-GAAP": 2,
            "Custom Dimensions": 4,
            "Alternate Hierarchies in Custom Dimensions": 4,
            "Additional Alias Tables": 1,
        }
    },
    "Setup Application Features": {
        "total": 79.5,
        "tasks": {
            "Elimination": 0.5,
            "Consolidation Journals": 1,
            "Journal Templates": 1,
            "Ownership Management": 4,
            "Enhanced Organization by Period": 4,
            "Equity Pickup": 8,
            "Partner Elimination": 8,
            "Configurable Consolidation Rules": 8,
            "Cash Flow": 8,
            "Supplemental Data Collection": 8,
            "Enterprise Journals": 8,
            "Approval Process": 8,
            "Historic Overrides": 4,
            "Task Manager": 8,
            "Audit": 1,
        }
    },
    "Application Customization": {
        "total": 8,
        "tasks": {
            "Data Forms": 4,
            "Dashboards": 4,
        }
    },
    "Calculations": {
        "total": 15,
        "tasks": {
            "Business Rules": 8,
            "Member Formula": 1,
            "Ratios": 4,
            "Custom KPIs": 2,
        }
    },
    "Security": {
        "total": 4,
        "tasks": {
            "Secured Dimensions": 2,
            "Number of Users": 2,
        }
    },
    "Historical Data": {
        "total": 60,
        "tasks": {
            "Historical Data Validation": 0,
            "Data Validation for Account Alt Hierarchies": 20,
            "Data Validation for Entity Alt Hierarchies": 20,
            "Historical Journal Conversion": 20,
        }
    },
    "Integrations": {
        "total": 80,
        "tasks": {
            "Files Based Loads": 16,
            "Direct Connect Integrations": 16,
            "Outbound Integrations": 16,
            "Pipeline": 16,
            "Custom Scripting": 16,
        }
    },
    "Reporting": {
        "total": 40,
        "tasks": {
            "Management Reports": 8,
            "Consolidation Reports": 4,
            "Consolidation Journal Reports": 4,
            "Intercompany Reports": 8,
            "Task Manager Reports": 4,
            "Enterprise Journal Reports": 4,
            "Smart View Reports": 8,
        }
    },
    "Automations": {
        "total": 52,
        "tasks": {
            "Automated Data loads": 16,
            "Automated Consolidations": 8,
            "Backup and Archival": 12,
            "Metadata Import": 16,
        }
    },
    "Testing/Training": {
        "total": 152,
        "tasks": {
            "Unit Testing": 40,
            "UAT": 40,
            "SIT": 16,
            "Parallel Testing": 40,
            "User Training": 16,
        }
    },
    "Transition": {
        "total": 80,
        "tasks": {
            "Go Live": 40,
            "Hypercare": 40,
        }
    },
    "Documentations": {
        "total": 24,
        "tasks": {
            "RTM": 8,
            "Design Document": 8,
            "System Configuration Document": 8,
        }
    },
    "Change Management": {
        "total": 32,
        "tasks": {
            "Admin Desktop Procedures": 16,
            "End user Desktop Procedures": 16,
        }
    },
}










# Category mappings for easier grouping
EFFORT_CATEGORIES = {
    "planning": ["Project Initiation and Planning"],
    "infrastructure": ["Creating and Managing EPM Cloud Infrastructure"],
    "requirements": ["Requirement Gathering, Read back and Client Sign-off"],
    "design": ["Design"],
    "build": ["Build and Configure FCC", "Setup Application Features", "Application Customization", "Calculations", "Security"],
    "data": ["Historical Data"],
    "integration": ["Integrations"],
    "reporting": ["Reporting"],
    "automation": ["Automations"],
    "testing": ["Testing/Training"],
    "deployment": ["Transition"],
    "documentation": ["Documentations", "Change Management"]
}


def get_total_baseline_hours():
    """Calculate total baseline hours from template"""
    total = 0
    for category, data in EFFORT_ESTIMATION_TEMPLATE.items():
        total += data["total"]
    return total


def get_category_hours(category_name):
    """Get hours for a specific category"""
    if category_name in EFFORT_ESTIMATION_TEMPLATE:
        return EFFORT_ESTIMATION_TEMPLATE[category_name]["total"]
    return 0


def get_task_hours(category_name, task_name):
    """Get hours for a specific task within a category"""
    if category_name in EFFORT_ESTIMATION_TEMPLATE:
        tasks = EFFORT_ESTIMATION_TEMPLATE[category_name]["tasks"]
        if task_name in tasks:
            return tasks[task_name]
    return 0


def print_template_summary():
    """Print a summary of the effort estimation template"""
    print("="*100)
    print("EFFORT ESTIMATION TEMPLATE - BASELINE HOURS")
    print("="*100)
    
    total_hours = 0
    
    for category, data in EFFORT_ESTIMATION_TEMPLATE.items():
        print(f"\n{category}: {data['total']} hours")
        print("-" * 80)
        for task, hours in data["tasks"].items():
            print(f"  {task:<60} {hours:>6} hrs")
        total_hours += data["total"]
    
    print("\n" + "="*100)
    print(f"TOTAL BASELINE HOURS: {total_hours}")
    print("="*100)


if __name__ == "__main__":
    print_template_summary()
