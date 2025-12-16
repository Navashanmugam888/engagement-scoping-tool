#!/usr/bin/env python
"""Script to update role allocations in excel_templates.py"""

file_path = 'backend_scoping_test/backend/data/excel_templates.py'

with open(file_path, 'r') as f:
    lines = f.readlines()

# Track which category we're in
output_lines = []
current_category = None
category_index = 0

for i, line in enumerate(lines):
    # Track current category by looking for "category": "..."
    if '"category":' in line and '"row_index":' in lines[i-1]:
        category_match = line.split('"category": "')[1].split('"')[0]
        current_category = category_match
        category_index = int(lines[i-2].split('"row_index": ')[1].split(',')[0])
    
    # Sr. Delivery Lead India: 50% for all categories
    if '"Sr. Delivery Lead India"' in line and 'roles' in lines[max(0, i-5):i]:
        output_lines.append('            "Sr. Delivery Lead India": 0.5,\n')
        continue
    
    # Reporting Lead India: 100% for Reporting, 20% for Testing/Training, 0% rest
    if '"Reporting Lead India"' in line and 'roles' in lines[max(0, i-5):i]:
        if current_category == "Reporting":
            output_lines.append('            "Reporting Lead India": 1,\n')
        elif current_category == "Testing/Training":
            output_lines.append('            "Reporting Lead India": 0.2,\n')
        else:
            output_lines.append('            "Reporting Lead India": 0,\n')
        continue
    
    # Security Lead India: 100% for Security, 0% rest
    if '"Security Lead India"' in line and 'roles' in lines[max(0, i-5):i]:
        if current_category == "Security":
            output_lines.append('            "Security Lead India": 1,\n')
        else:
            output_lines.append('            "Security Lead India": 0,\n')
        continue
    
    output_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(output_lines)

print("Role allocations updated successfully!")
