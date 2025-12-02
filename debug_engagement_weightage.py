import json
from backend.core.scope_processor import ScopeDefinitionProcessor
from backend.core.effort_calculator import EffortCalculator

# Hardcoded test data based on image
test_input = {
    'scope_inputs': [
        {'name': 'Historical Data Validation', 'in_scope': 'YES', 'details': 2},
        {'name': 'Data Validation for Account Alt Hierarchies', 'in_scope': 'YES', 'details': 2},
        {'name': 'Data Validation for Entity Alt Hierarchies', 'in_scope': 'YES', 'details': 2},
        {'name': 'Historical Journal Conversion', 'in_scope': 'YES', 'details': 2},
    ],
    'selected_roles': []
}

processor = ScopeDefinitionProcessor()
scope_result = processor.process_user_input(test_input)

print(f"Total Weightage: {scope_result['total_weightage']}")
print(f"Tier: {scope_result['tier']} - {scope_result['tier_name']}")

# Now check effort calculation
calculator = EffortCalculator(scope_result)
print(f"\nEngagement Weightage used in calculator: {calculator.engagement_weightage}")

# Check Historical Data category calculation
hist_data_base = 60
tier_adjustment = (0, 8, 12, 16)
engagement_w = calculator.engagement_weightage

if engagement_w <= 100:
    hist_data_final = hist_data_base + tier_adjustment[0]
elif engagement_w <= 120:
    hist_data_final = hist_data_base + tier_adjustment[1]
elif engagement_w <= 160:
    hist_data_final = hist_data_base + tier_adjustment[2]
else:
    hist_data_final = hist_data_base + tier_adjustment[3]

print(f"\nHistorical Data calculation:")
print(f"  Base: {hist_data_base}")
print(f"  Engagement Weightage: {engagement_w}")
print(f"  Tier adjustment: {tier_adjustment}")
print(f"  Expected Final: {hist_data_final}")

# Calculate full effort
category_efforts = calculator.calculate_all_efforts()
hist_data_effort = category_efforts.get('Historical Data', {}).get('category_final_estimate', 0)
print(f"  Actual calculated: {hist_data_effort}")
