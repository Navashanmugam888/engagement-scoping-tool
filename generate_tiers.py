#!/usr/bin/env python
"""Generate corrected APP_TIERS_DATA with proper role allocations"""

categories = [
    "Project Initiation and Planning",
    "Creating and Managing EPM Cloud Infrastructure",
    "Requirement Gathering, Read back and Client Sign-off",
    "Design",
    "Build and Configure FCC",
    "Setup Application Features",
    "Application Customization",
    "Calculations",
    "Security",
    "Historical Data",
    "Integrations",
    "Reporting",
    "Automations",
    "Testing/Training",
    "Transition",
    "Documentations",
    "Change Management"
]

# Base values (used for most categories)
def get_roles(category_name):
    roles = {
        "PM USA": 0.5,
        "PM India": 0.5,
        "Architect USA": 0.2,
        "Sr. Delivery Lead India": 0.5,  # 50% for all
        "Delivery Lead India": 0.5,
        "App Lead USA": 1,
        "App Lead India": 1,
        "App Developer USA": 1,
        "App Developer India": 1,
        "Integration Lead USA": 0,
        "Integration Developer India": 0,
        "Reporting Lead India": 0,  # 0 by default
        "Security Lead India": 0,   # 0 by default
    }
    
    # Override for specific categories
    if category_name == "Project Initiation and Planning":
        roles["PM USA"] = 0.7
        roles["Architect USA"] = 1
        roles["App Lead USA"] = 0
        roles["App Lead India"] = 0
        roles["App Developer USA"] = 0
        roles["App Developer India"] = 0
        roles["Integration Lead USA"] = 0
        roles["Integration Developer India"] = 0
    elif category_name == "Creating and Managing EPM Cloud Infrastructure":
        roles["Architect USA"] = 0
        roles["App Developer USA"] = 0
        roles["App Developer India"] = 0
        roles["Integration Lead USA"] = 0
        roles["Integration Developer India"] = 0
    elif category_name == "Requirement Gathering, Read back and Client Sign-off":
        roles["Architect USA"] = 1
        roles["App Developer USA"] = 0
        roles["App Developer India"] = 0
        roles["Integration Lead USA"] = 0.2
        roles["Integration Developer India"] = 0.2
    elif category_name == "Design":
        roles["Architect USA"] = 1
        roles["App Developer USA"] = 0
        roles["App Developer India"] = 0
        roles["Integration Lead USA"] = 0.2
        roles["Integration Developer India"] = 0.2
    elif category_name == "Security":
        roles["Integration Lead USA"] = 0.2
        roles["Integration Developer India"] = 0.2
        roles["Security Lead India"] = 1  # 100% for Security
    elif category_name == "Reporting":
        roles["Reporting Lead India"] = 1  # 100% for Reporting
    elif category_name == "Testing/Training":
        roles["Integration Lead USA"] = 0.5
        roles["Integration Developer India"] = 0.5
        roles["Reporting Lead India"] = 0.2  # 20% for Testing/Training
    elif category_name == "Transition":
        roles["Integration Lead USA"] = 0.5
        roles["Integration Developer India"] = 0.5
    elif category_name == "Documentations":
        roles["Integration Lead USA"] = 0.5
        roles["Integration Developer India"] = 0.5
    elif category_name == "Change Management":
        roles["Integration Lead USA"] = 0.5
        roles["Integration Developer India"] = 0.5
    elif category_name == "Integrations":
        roles["Integration Lead USA"] = 1
        roles["Integration Developer India"] = 1
    elif category_name == "Automations":
        roles["Integration Lead USA"] = 1
        roles["Integration Developer India"] = 1
    elif category_name == "Historical Data":
        pass  # Use base values
    elif category_name == "Build and Configure FCC":
        pass  # Use base values
    elif category_name == "Setup Application Features":
        pass  # Use base values
    elif category_name == "Application Customization":
        pass  # Use base values
    elif category_name == "Calculations":
        pass  # Use base values
    
    return roles

# Generate the output
output = "APP_TIERS_DATA = [\n"

for idx, category in enumerate(categories):
    roles = get_roles(category)
    
    roles_str = ""
    for role_name, value in roles.items():
        roles_str += f'            "{role_name}": {value},\n'
    roles_str = roles_str.rstrip(',\n')
    
    output += f'''    {{
        "row_index": {idx},
        "category": "{category}",
        "roles": {{
{roles_str}
        }}
    }}'''
    
    if idx < len(categories) - 1:
        output += ",\n"
    else:
        output += "\n"

output += "]"

# Print output for verification
print(output)
