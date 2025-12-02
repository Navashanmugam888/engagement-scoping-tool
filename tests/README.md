# FCC Engagement Scoping Tool - Backend

## Overview
Enterprise-grade backend for Oracle EPM FCC implementation scoping and effort estimation.

## Project Structure

```
scoping_tool/
├── backend/
│   ├── __init__.py
│   ├── config.py                 # Configuration and constants
│   ├── scoping_engine.py         # Main orchestrator
│   ├── core/
│   │   ├── scope_processor.py    # Scope definition processing
│   │   └── effort_calculator.py  # Effort estimation calculation
│   ├── utils/
│   │   └── formula_evaluator.py  # Excel formula evaluation
│   └── data/
│       ├── effort_template.py    # Baseline effort template (790.5 hrs)
│       ├── formulas_expanded.csv # Main formulas (52)
│       └── formulas_array_supplement.csv # Array formulas (8)
├── output/                       # Generated reports
├── run_example.py                # Example usage
└── Engagement Scoping Tool - FCC.xlsx

```

## Workflow

### Step 1: Scope Definition
- **Input**: User selects In Scope (YES/NO) and Details for 71 metrics
- **Process**: 
  - Formula evaluation using 60 formulas
  - Calculate weightage for each metric
  - Determine In Scope Flag (1 or 0)
  - Calculate Feature Clean names
- **Output**: 
  - Total Engagement Weightage (e.g., 130)
  - Implementation Tier (1-5)
  - Metrics with calculated weightage

### Step 2: Effort Estimation
- **Input**: Scope result from Step 1
- **Process**:
  - Tier-based adjustments to baseline hours
  - Task-specific formula calculations
  - XLOOKUP simulation for in-scope tasks
- **Output**:
  - Total Time: Tier-adjusted hours
  - Final Estimate: Sum of all task hours
  - Duration: Days and Months

### Tier Definitions
| Tier | Name | Weightage Range |
|------|------|-----------------|
| 1 | Jumpstart | 0-60 |
| 2 | Foundation Plus | 61-100 |
| 3 | Enhanced Scope | 101-150 |
| 4 | Advanced Enablement | 151-200 |
| 5 | Full Spectrum | 201-999 |

## Usage

### Basic Usage
```python
from backend.scoping_engine import ScopingEngine

# Prepare user input
user_input = {
    'scope_inputs': [
        {'name': 'Account', 'in_scope': 'YES', 'details': 2000},
        {'name': 'Multi-Currency', 'in_scope': 'YES', 'details': 5},
        # ... more metrics
    ],
    'selected_roles': ['PM USA', 'PM India', 'Architect USA']
}

# Run complete workflow
engine = ScopingEngine()
report = engine.run_complete_workflow(user_input)

# Access results
print(f"Weightage: {report['scope_definition']['total_weightage']}")
print(f"Tier: {report['scope_definition']['tier_name']}")
print(f"Hours: {report['effort_estimation']['summary']['final_estimate_hours']}")
print(f"Days: {report['effort_estimation']['summary']['total_days']}")
print(f"Months: {report['effort_estimation']['summary']['total_months']}")
```

### Load from Excel (Testing)
```python
python run_example.py
```

## Output Format

### Scope Definition Result
```json
{
  "total_weightage": 130,
  "tier": 3,
  "tier_name": "Tier 3 - Enhanced Scope",
  "tier_range": [101, 150],
  "selected_roles": ["PM USA", "PM India"],
  "summary": {
    "total_metrics": 71,
    "in_scope_count": 51,
    "out_scope_count": 20
  },
  "metrics": [...]
}
```

### Effort Estimation Result
```json
{
  "summary": {
    "engagement_weightage": 130,
    "tier": 3,
    "tier_name": "Tier 3 - Enhanced Scope",
    "total_time_hours": 992.5,
    "final_estimate_hours": 1892.5,
    "total_days": 236.56,
    "total_months": 7.89
  },
  "categories": {...}
}
```

## Key Features

✅ **Formula Evaluation**: Evaluates 60 Excel formulas with IF, AND, OR, IFS, SUM functions  
✅ **Tier-Based Calculation**: Automatic tier determination and adjustments  
✅ **XLOOKUP Simulation**: Maps scope metrics to effort tasks  
✅ **Role Management**: 13 predefined implementation roles  
✅ **Clean Architecture**: Separation of concerns with modular design  
✅ **JSON Reports**: Machine-readable output for frontend integration  

## Constants

- **Baseline Template**: 790.5 hours (17 categories, 86 tasks)
- **Hours per Day**: 8
- **Days per Month**: 30
- **Total Formulas**: 60 (52 + 8 array formulas)
- **Total Metrics**: 71 (excluding section headings)

## Next Steps (50% Complete)

Remaining workflow:
- [ ] Resource allocation based on selected roles
- [ ] Timeline generation with dependencies
- [ ] Risk assessment based on complexity
- [ ] Cost estimation with rate cards
- [ ] Export to PowerPoint/PDF presentation
