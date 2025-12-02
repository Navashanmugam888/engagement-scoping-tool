import json

with open('output/test_from_image.json') as f:
    data = json.load(f)
    
print('EFFORT ESTIMATION BREAKDOWN BY CATEGORY:')
print()

total_in_days = 0
for category, details in data['effort_estimation']['categories'].items():
    if isinstance(details, dict) and 'in_days' in details:
        in_days_val = details.get('in_days', 0)
        final_est = details.get('final_estimate', 0)
        print(f'{category}:')
        print(f'  Final Estimate: {final_est} hours')
        print(f'  In Days: {in_days_val}')
        total_in_days += in_days_val
        print()

print(f'Total In Days: {total_in_days}')
print(f'Total Hours (In Days * 8): {round(total_in_days * 8, 2)}')
print()
print('SUMMARY FROM JSON:')
summary = data['effort_estimation']['summary']
for key, val in summary.items():
    print(f'{key}: {val}')
