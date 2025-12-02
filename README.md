# Engagement Scoping Tool - FCC Implementation

A Python-based effort estimation engine for Financial Consolidation and Close (FCC) implementations on Oracle EPM Cloud.

## Overview

This tool calculates implementation effort estimation based on engagement scope and complexity metrics. It processes user input through a scope definition sheet, evaluates weightage formulas, and generates effort estimates aligned with Excel calculations.

## Project Structure

```
scoping_tool/
├── backend/                          # Core calculation engine
│   ├── config.py                    # Configuration and constants
│   ├── scoping_engine.py            # Main entry point
│   ├── core/
│   │   ├── scope_processor.py       # Scope definition processing and weightage calculation
│   │   └── effort_calculator.py     # Effort estimation with tier-based adjustments
│   ├── data/
│   │   ├── effort_template.py       # Task structure and defaults
│   │   ├── formulas_expanded.csv    # Weightage calculation formulas
│   │   └── formulas_array_supplement.csv  # Array formula supplements
│   └── utils/
│       └── formula_evaluator.py     # Excel formula evaluation engine
├── Engagement Scoping Tool - FCC.xlsx  # Source Excel workbook
├── test_image_data_simple.py        # Comprehensive test with validation
├── test_ui.py                       # UI testing script
└── test_with_image_data.py          # Alternative test format
```

## Key Features

### 1. Scope Definition Processor
- Loads metrics from Excel Scope Definition sheet
- Processes user inputs (in_scope, details values)
- Sets in_scope_flag (0/1) as critical gate for effort calculation
- Evaluates weightage formulas for each metric
- Calculates total engagement weightage and determines implementation tier

### 2. Effort Calculator
- Calculates task-level effort estimates with specialized formulas:
  - Complex scaling formulas (Data Forms, Dashboards, Business Rules, Management Reports)
  - Special multipliers (Secured Dimensions, Number of Users)
  - Conditional logic (Prelim FCC User Provisioning)
  - Historical Data Validation with special calculation
  - Data validation tasks that reuse Historical Data Validation's details value
  - Standard multiplication tasks
- Applies tier-based adjustments to category base hours (16 categories with 4 patterns)
- Aggregates task estimates and applies engagement weightage adjustments
- Returns effort in hours, days (hours/8), and months (days/30)

### 3. Formula Evaluator
- Parses and evaluates Excel-like formulas with FeatureName[Column] syntax
- Supports IF, AND, OR, SUM, IFS functions
- Implements Excel ROUND function (round half up) vs Python's banker's rounding
- Safe evaluation with namespace restrictions

### 4. Tier-Based Scaling
- 5 implementation tiers based on engagement weightage (0-999):
  - Tier 1: Jumpstart (0-60 weightage)
  - Tier 2: Foundation Plus (61-100)
  - Tier 3: Enhanced Scope (101-150)
  - Tier 4: Advanced Enablement (151-200)
  - Tier 5: Full Spectrum (201+)

## Critical Logic Details

### Historical Data Category Fix
The data validation tasks (rows 86-88 in Excel) use **hardcoded references** to Historical Data Validation's details value:
- **Data Validation for Account Alt Hierarchies**: `20 × historical_data_validation_details`
- **Data Validation for Entity Alt Hierarchies**: `20 × historical_data_validation_details`
- **Historical Journal Conversion**: `20 × historical_data_validation_details`

This is intentional - they are dependent on Historical Data Validation's scope, not independent metrics.

### In Scope Flag
The `in_scope_flag` (0/1) is the critical gate that determines effort contribution:
- Set by ScopeDefinitionProcessor based on user's 'in_scope' input (YES/NO)
- Used by EffortCalculator to gate all effort calculations
- When flag=0, task contributes 0 effort regardless of details value

### Excel ROUND Implementation
Python's `round()` uses banker's rounding (round half to even), but Excel uses round half up. The custom `excel_round()` function implements:
```python
math.floor(value * multiplier + 0.5) / multiplier
```

## Usage

### Basic Example
```python
from backend.core.scope_processor import ScopeDefinitionProcessor
from backend.core.effort_calculator import EffortCalculator

# Process user input
processor = ScopeDefinitionProcessor()
scope_result = processor.process_user_input({
    'scope_inputs': [
        {'name': 'Historical Data Validation', 'in_scope': 'YES', 'details': 2},
        {'name': 'Data Forms', 'in_scope': 'YES', 'details': 5},
        # ... more metrics
    ],
    'selected_roles': ['PM USA', 'Architect USA']
})

# Calculate effort
calculator = EffortCalculator(scope_result)
effort = calculator.calculate_effort()
summary = calculator.generate_summary(effort)

print(f"Total Hours: {summary['total_time_hours']}")
print(f"Total Days: {summary['total_days']}")
print(f"Total Months: {summary['total_months']}")
print(f"Tier: {summary['tier_name']}")
```

## Testing

Run the comprehensive test with validation:
```bash
python test_image_data_simple.py
```

This test includes all 71 metrics and validates that the calculated effort matches Excel values exactly (1892.5 hours).

## Excel Integration

The tool maintains exact parity with the Excel workbook:
- Column mappings and named ranges preserved
- Tier adjustment schedules match Excel lookup tables
- Formula calculations (including ROUND behavior) replicate Excel exactly
- Named ranges: EngagementWeightage, FeatureCleanRange, InScopeFlagRange

## Configuration

Edit `backend/config.py` to customize:
- Hours per day (default: 8)
- Days per month (default: 30)
- Tier definitions and ranges
- Available roles for implementation
- Excel file path and sheet names

## Performance Considerations

- Metric weightage formulas are evaluated for each user input processing
- Formula evaluation uses safe_eval with restricted namespace
- All calculations are deterministic and can be cached

## Future Enhancements

- API endpoint for integration with project management tools
- Real-time effort tracking against estimates
- Role-based resource allocation
- Multi-tier project scenarios
- Export to PDF/Excel reports
