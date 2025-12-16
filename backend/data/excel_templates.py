"""
Excel-Free Definitions Module

This module contains all the templates and configurations that were previously 
loaded from the Excel file "Engagement Scoping Tool - FCC.xlsx".

NO LOGIC CHANGES - These are pure data extracted from Excel templates.
The system works identically - just using Python data instead of Excel sheets.
"""

# =============================================================================
# SCOPE DEFINITION TEMPLATE (71 metrics from Excel 'Scope Definition' sheet)
# =============================================================================
# Template columns: row (from Excel), name, is_details_required, is_sub_question
# This defines which metrics exist and their properties
METRICS_TEMPLATE = [
    {"row": 6, "name": "Account", "is_details_required": True, "is_sub_question": False},
    {"row": 7, "name": "Account Alternate Hierarchies", "is_details_required": True, "is_sub_question": True},
    {"row": 8, "name": "Rationalization of CoA", "is_details_required": False, "is_sub_question": True},
    {"row": 9, "name": "Multi-Currency", "is_details_required": True, "is_sub_question": False},
    {"row": 10, "name": "Reporting Currency", "is_details_required": True, "is_sub_question": False},
    {"row": 11, "name": "Entity", "is_details_required": True, "is_sub_question": False},
    {"row": 12, "name": "Entity Redesign", "is_details_required": False, "is_sub_question": True},
    {"row": 13, "name": "Entity Alternate Hierarchies", "is_details_required": True, "is_sub_question": True},
    {"row": 14, "name": "Scenario", "is_details_required": True, "is_sub_question": False},
    {"row": 15, "name": "Multi-GAAP", "is_details_required": False, "is_sub_question": False},
    {"row": 16, "name": "Custom Dimensions", "is_details_required": True, "is_sub_question": False},
    {"row": 17, "name": "Alternate Hierarchies in Custom Dimensions", "is_details_required": True, "is_sub_question": True},
    {"row": 18, "name": "Additional Alias Tables", "is_details_required": True, "is_sub_question": False},
    {"row": 21, "name": "Elimination", "is_details_required": False, "is_sub_question": False},
    {"row": 22, "name": "Custom Elimination Requirement", "is_details_required": False, "is_sub_question": False},
    {"row": 23, "name": "Consolidation Journals", "is_details_required": False, "is_sub_question": False},
    {"row": 24, "name": "Journal Templates", "is_details_required": True, "is_sub_question": True},
    {"row": 25, "name": "Parent Currency Journals", "is_details_required": False, "is_sub_question": True},
    {"row": 26, "name": "Ownership Management", "is_details_required": False, "is_sub_question": False},
    {"row": 27, "name": "Enhanced Organization by Period", "is_details_required": False, "is_sub_question": True},
    {"row": 28, "name": "Equity Pickup", "is_details_required": False, "is_sub_question": True},
    {"row": 29, "name": "Partner Elimination", "is_details_required": False, "is_sub_question": True},
    {"row": 30, "name": "Configurable Consolidation Rules", "is_details_required": False, "is_sub_question": True},
    {"row": 31, "name": "Cash Flow", "is_details_required": False, "is_sub_question": False},
    {"row": 32, "name": "Supplemental Data Collection", "is_details_required": False, "is_sub_question": False},
    {"row": 33, "name": "Enterprise Journals", "is_details_required": False, "is_sub_question": False},
    {"row": 34, "name": "Approval Process", "is_details_required": False, "is_sub_question": False},
    {"row": 35, "name": "Historic Overrides", "is_details_required": False, "is_sub_question": False},
    {"row": 36, "name": "Task Manager", "is_details_required": False, "is_sub_question": False},
    {"row": 37, "name": "Audit", "is_details_required": False, "is_sub_question": False},
    {"row": 40, "name": "Data Forms", "is_details_required": True, "is_sub_question": False},
    {"row": 41, "name": "Dashboards", "is_details_required": True, "is_sub_question": False},
    {"row": 44, "name": "Business Rules", "is_details_required": True, "is_sub_question": False},
    {"row": 45, "name": "Member Formula", "is_details_required": True, "is_sub_question": False},
    {"row": 46, "name": "Ratios", "is_details_required": False, "is_sub_question": False},
    {"row": 47, "name": "Custom KPIs", "is_details_required": True, "is_sub_question": False},
    {"row": 50, "name": "Secured Dimensions", "is_details_required": True, "is_sub_question": False},
    {"row": 51, "name": "Number of Users", "is_details_required": True, "is_sub_question": False},
    {"row": 54, "name": "Historical Data Validation", "is_details_required": True, "is_sub_question": False},
    {"row": 55, "name": "Data Validation for Account Alt Hierarchies", "is_details_required": False, "is_sub_question": False},
    {"row": 56, "name": "Data Validation for Entity Alt Hierarchies", "is_details_required": False, "is_sub_question": False},
    {"row": 57, "name": "Historical Journal Conversion", "is_details_required": False, "is_sub_question": False},
    {"row": 60, "name": "Files Based Loads", "is_details_required": True, "is_sub_question": False},
    {"row": 61, "name": "Direct Connect Integrations", "is_details_required": True, "is_sub_question": False},
    {"row": 62, "name": "Outbound Integrations", "is_details_required": True, "is_sub_question": False},
    {"row": 63, "name": "Pipeline", "is_details_required": True, "is_sub_question": False},
    {"row": 64, "name": "Custom Scripting", "is_details_required": True, "is_sub_question": False},
    {"row": 67, "name": "Management Reports", "is_details_required": True, "is_sub_question": False},
    {"row": 68, "name": "Consolidation Reports", "is_details_required": True, "is_sub_question": False},
    {"row": 69, "name": "Consolidation Journal Reports", "is_details_required": True, "is_sub_question": False},
    {"row": 70, "name": "Intercompany Reports", "is_details_required": True, "is_sub_question": False},
    {"row": 71, "name": "Task Manager Reports", "is_details_required": True, "is_sub_question": False},
    {"row": 72, "name": "Enterprise Journal Reports", "is_details_required": True, "is_sub_question": False},
    {"row": 73, "name": "Smart View Reports", "is_details_required": True, "is_sub_question": False},
    {"row": 76, "name": "Automated Data loads", "is_details_required": False, "is_sub_question": False},
    {"row": 77, "name": "Automated Consolidations", "is_details_required": False, "is_sub_question": False},
    {"row": 78, "name": "Backup and Archival", "is_details_required": False, "is_sub_question": False},
    {"row": 79, "name": "Metadata Import", "is_details_required": False, "is_sub_question": False},
    {"row": 82, "name": "Unit Testing", "is_details_required": False, "is_sub_question": False},
    {"row": 83, "name": "UAT", "is_details_required": False, "is_sub_question": False},
    {"row": 84, "name": "SIT", "is_details_required": False, "is_sub_question": False},
    {"row": 85, "name": "Parallel Testing", "is_details_required": True, "is_sub_question": False},
    {"row": 86, "name": "User Training", "is_details_required": False, "is_sub_question": False},
    {"row": 89, "name": "Go Live", "is_details_required": False, "is_sub_question": False},
    {"row": 90, "name": "Hypercare", "is_details_required": False, "is_sub_question": False},
    {"row": 93, "name": "RTM", "is_details_required": False, "is_sub_question": False},
    {"row": 94, "name": "Design Document", "is_details_required": False, "is_sub_question": False},
    {"row": 95, "name": "System Configuration Document", "is_details_required": False, "is_sub_question": False},
    {"row": 98, "name": "Admin Desktop Procedures", "is_details_required": False, "is_sub_question": False},
    {"row": 99, "name": "End User Desktop Procedures", "is_details_required": False, "is_sub_question": False},
    {"row": 102, "name": "Project Management", "is_details_required": False, "is_sub_question": False},
]


# =============================================================================
# APP TIERS DEFINITION TEMPLATE (from Excel 'App Tiers Definition' sheet)
# =============================================================================
# Role names extracted from rows 4-5 (Location + Role Name)
APP_TIERS_ROLES = [
    "PM USA",
    "PM India",
    "Architect USA",
    "Sr. Delivery Lead India",
    "Delivery Lead India",
    "App Lead USA",
    "App Lead India",
    "App Developer USA",
    "App Developer India",
    "Integration Lead USA",
    "Integration Developer India",
    "Reporting Lead India",
    "Security Lead India"
]

# Tier allocation template: Role percentages for each category (rows 6-22)
# Hours are dynamically retrieved from effort estimation
# This defines only how hours are distributed across roles for each implementation category
# row_index is needed to maintain the 17-row structure for SUMPRODUCT calculation
APP_TIERS_DATA = [
    {
        "row_index": 0,
        "category": "Project Initiation and Planning",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 1,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 0,
            "App Lead India": 0,
            "App Developer USA": 0,
            "App Developer India": 0,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 1,
        "category": "Creating and Managing EPM Cloud Infrastructure",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 0,
            "App Developer India": 0,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 2,
        "category": "Requirement Gathering, Read back and Client Sign-off",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 1,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 0,
            "App Developer India": 0,
            "Integration Lead USA": 0.2,
            "Integration Developer India": 0.2,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 3,
        "category": "Design",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 1,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 0,
            "App Developer India": 0,
            "Integration Lead USA": 0.2,
            "Integration Developer India": 0.2,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 4,
        "category": "Build and Configure FCC",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 5,
        "category": "Setup Application Features",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 6,
        "category": "Application Customization",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 7,
        "category": "Calculations",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 8,
        "category": "Security",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0.2,
            "Integration Developer India": 0.2,
            "Reporting Lead India": 0,
            "Security Lead India": 1
        }
    },
    {
        "row_index": 9,
        "category": "Historical Data",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 10,
        "category": "Integrations",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 1,
            "Integration Developer India": 1,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 11,
        "category": "Reporting",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0,
            "Integration Developer India": 0,
            "Reporting Lead India": 1,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 12,
        "category": "Automations",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 1,
            "Integration Developer India": 1,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 13,
        "category": "Testing/Training",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0.5,
            "Integration Developer India": 0.5,
            "Reporting Lead India": 0.2,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 14,
        "category": "Transition",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0.5,
            "Integration Developer India": 0.5,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 15,
        "category": "Documentations",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0.5,
            "Integration Developer India": 0.5,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    },
    {
        "row_index": 16,
        "category": "Change Management",
        "roles": {
            "PM USA": 0.5,
            "PM India": 0.5,
            "Architect USA": 0.2,
            "Sr. Delivery Lead India": 0.5,
            "Delivery Lead India": 0.5,
            "App Lead USA": 1,
            "App Lead India": 1,
            "App Developer USA": 1,
            "App Developer India": 1,
            "Integration Lead USA": 0.5,
            "Integration Developer India": 0.5,
            "Reporting Lead India": 0,
            "Security Lead India": 0
        }
    }
]


# =============================================================================
# KDD DEFINITIONS TEMPLATE (from Excel 'Definitions' sheet, rows 138-149)
# =============================================================================
# Key Design Decisions that get included based on scope definition values
KDD_DEFINITIONS = {
    "KDD05": "Ownership Management",
    "KDD06": "Cash Flow",
    "KDD07": "Journal Process",
    "KDD08": "Integrations",
    "KDD09": "Historical Data Source and Validations",
    "KDD10": "Automations",
    "KDD11": "Approval Process",
    "KDD12": "Task Manager",
    "KDD13": "Supplemental Data Collection",
    "KDD14": "Enterprise Journals",
    "KDD15": "Application Security",
    "KDD16": "Audit",
}

# Mapping: which scope cell determines which KDD
# Format: (scope_metric_name, kdd_key, row_in_excel)
KDD_CONDITIONAL_MAPPINGS = [
    ("Ownership Management", "KDD05", 138),
    ("Cash Flow", "KDD06", 139),
    ("Consolidation Journals", "KDD07", 140),
    ("Files Based Loads", "KDD08", 141),
    ("Historical Data Validation", "KDD09", 142),
    ("Automated Data loads", "KDD10", 143),
    ("Approval Process", "KDD11", 144),
    ("Task Manager", "KDD12", 145),
    ("Supplemental Data Collection", "KDD13", 146),
    ("Enterprise Journals", "KDD14", 147),
    ("Secured Dimensions", "KDD15", 148),
    ("Audit", "KDD16", 149),
]
