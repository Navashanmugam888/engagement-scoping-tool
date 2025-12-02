"""Debug Reporting category to find 8-hour gap"""

import sys
sys.path.insert(0, '.')

from backend.core.effort_calculator import EffortCalculator
from backend.core.scope_processor import ScopeDefinitionProcessor
from test_image_data_simple import scope_inputs

# Process scope
processor = ScopeDefinitionProcessor(scope_inputs)
scope_result = processor.process()

# Create calculator
calculator = EffortCalculator(scope_result)

# Get all metrics to see details values
print("\n" + "="*100)
print("REPORTING TASKS - DETAILS AND CALCULATIONS")
print("="*100)

reporting_tasks = [
    "Management Reports",
    "Consolidation Reports", 
    "Consolidation Journal Reports",
    "Intercompany Reports",
    "Task Manager Reports",
    "Enterprise Journal Reports",
    "Smart View Reports"
]

total_calc = 0
for task_name in reporting_tasks:
    metric = calculator.scope_metrics.get(task_name)
    if metric:
        details = metric.get('details', 0) if metric.get('details') is not None else 0
        in_scope = "YES" if metric['in_scope_flag'] == 1 else "NO"
        base = 8 if task_name in ["Management Reports", "Intercompany Reports", "Smart View Reports"] else 4
        
        estimate = calculator.calculate_task_final_estimate(task_name)
        
        print(f"\n{task_name}")
        print(f"  In Scope: {in_scope}")
        print(f"  Details: {details}")
        print(f"  Base Hours: {base}")
        print(f"  Final Estimate: {estimate}")
        total_calc += estimate
    else:
        print(f"\n{task_name}: NOT FOUND IN METRICS")

print(f"\n{'='*100}")
print(f"Reporting Tasks Total: {total_calc}")
print(f"Expected (with tier adj): 140")
print(f"Gap: {140 - total_calc}")

# Check category calculation
print(f"\n{'='*100}")
print(f"Category Weightage: {calculator.engagement_weightage}")
print(f"Tier: {calculator.tier_name}")

# Get base category hours
from backend.data.effort_template import get_category_hours
base_reporting = get_category_hours("Reporting")
print(f"Base Reporting Hours: {base_reporting}")

# Calculate what tier adjustment should be applied
w = calculator.engagement_weightage
tier_adj_tuple = (0, 8, 12, 16)  # For Reporting category
if w <= 100:
    tier_adj = tier_adj_tuple[0]
elif w <= 120:
    tier_adj = tier_adj_tuple[1]
elif w <= 160:
    tier_adj = tier_adj_tuple[2]
else:
    tier_adj = tier_adj_tuple[3]

final_category = base_reporting + tier_adj
print(f"Tier Adjustment: {tier_adj}")
print(f"Expected Category Total: {final_category}")

print(f"\n{'='*100}")
print("CALCULATION BREAKDOWN:")
print(f"  Base: {base_reporting}")
print(f"  Tier Adjustment: +{tier_adj}")
print(f"  Expected: {final_category}")
print(f"  Calculated: {total_calc}")
print(f"  Gap: {final_category - total_calc} hours")
