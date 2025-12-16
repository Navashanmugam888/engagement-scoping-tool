# FCC Scoping Tool - Calculations Explained

## Overview
This document explains the calculation methodology used by the FCC Scoping Tool backend. All calculations are based on the original Excel formulas.

## Calculation Flow

### 1. Scope Definition Processing
**Purpose**: Determine engagement complexity and implementation tier

**Steps**:
1. **Collect Scope Inputs**: User selects features/dimensions with YES/NO and provides counts
2. **Calculate Weightage**: Each feature has a predefined weightage value
3. **Sum Total Weightage**: Add up all selected features' weightages
4. **Determine Tier**: Based on total weightage:
   - **Tier 1 (Jumpstart)**: 0-100 weightage
   - **Tier 2 (Foundation Plus)**: 101-120 weightage
   - **Tier 3 (Enterprise Foundation)**: 121-160 weightage
   - **Tier 4 (Enterprise Advanced)**: 161+ weightage

### 2. Effort Estimation
**Purpose**: Calculate hours required for each category and task

**Categories** (17 total):
- Project Initiation and Planning
- Requirement Gathering, Read back and Client Sign-off
- Design
- Build and Configure FCC
- Setup Application Features
- Application Customization
- Calculations
- Security
- Historical Data
- Integrations
- Reporting
- Automations
- Testing/Training
- Transition
- Documentations
- Change Management
- Creating and Managing EPM Cloud Infrastructure

**Calculation Logic**:
1. **Base Hours**: Each category has a base hour value
2. **Tier Adjustment**: Additional hours based on tier:
   - Tier 1: Base hours only
   - Tier 2: Base + small adjustment
   - Tier 3: Base + medium adjustment
   - Tier 4: Base + large adjustment
3. **Task-Level Calculations**: For tasks with detail formulas:
   - **Simple Multiplier**: `hours = base_value × count`
   - **Complex ROUND Formula**: `hours = ROUND(count×0.5)×8 + ROUND(count×0.25)×12 + ROUND(count×0.25)×16`
   - **Conditional Logic**: IF statements for threshold-based calculations
4. **Category Total** = Base Hours + Tier Adjustment + Sum of Task Estimates

**Example**:
```
Data Forms (with 10 forms selected):
- Part 1: ROUND(10×0.5) × 8 = 5 × 8 = 40 hours
- Part 2: ROUND(10×0.25) × 12 = 3 × 12 = 36 hours  
- Part 3: ROUND(10×0.25) × 16 = 3 × 16 = 48 hours
- Total: 124 hours
```

### 3. FTE Allocation
**Purpose**: Distribute effort across selected roles

**Method**: SUMPRODUCT formula from Excel
- Each category has predefined percentage allocation per role
- Role Hours = Σ(Category Hours × Role Percentage for that category)
- Calculates hours, days (/8), and months (/30) for each role

**Example**:
```
PM USA allocation:
- Project Planning: 100 hrs × 15% = 15 hrs
- Design: 200 hrs × 10% = 20 hrs
- Build: 300 hrs × 5% = 15 hrs
- Total PM USA: 50 hrs (6.25 days, 0.21 months)
```

### 4. Report Generation
**Outputs**:
1. **JSON Report**: Complete calculation details with all intermediate values
2. **Word Document**: Professional SOW-style report with:
   - Executive Summary
   - Scope Definition
   - Effort Estimation by Category
   - FTE Allocation by Role
   - Assumptions and Notes

## Data Structure

### Frontend to Backend Mapping
The frontend uses short IDs (e.g., `account`, `bus_rules`) which are mapped to Excel names (e.g., `Account`, `Business Rules`) using the `FRONTEND_TO_BACKEND_MAP` dictionary in `api_server.py`.

### Result Format
```json
{
  "scope_definition": {
    "total_weightage": 94.0,
    "tier": 2,
    "tier_name": "Tier 2 - Foundation Plus",
    "selected_roles": ["PM USA", "App Lead India", ...]
  },
  "effort_estimation": {
    "summary": {
      "total_time_hours": 1344.5,
      "total_days": 168.06,
      "total_months": 5.6
    },
    "categories": {
      "Project Initiation and Planning": 64.0,
      "Design": 104.0,
      "Build and Configure FCC": 128.0,
      ...
    }
  },
  "fte_allocation": {
    "by_role": {
      "PM USA": {"hours": 150.5, "days": 18.8, "months": 0.63},
      ...
    },
    "total_hours": 10649.0,
    "total_days": 1331.13,
    "total_months": 44.37
  }
}
```

## Key Formulas

### Excel ROUND Function
Python's `round()` uses banker's rounding. We implement Excel's "round half up":
```python
def excel_round(value, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(value * multiplier + 0.5) / multiplier
```

### Days and Months Conversion
- **Days** = Hours ÷ 8 (8-hour work day)
- **Months** = Days ÷ 30 (30-day month)

## Validation

The backend exactly replicates Excel formulas including:
✅ Tier-based category adjustments  
✅ Task-level detail formulas  
✅ ROUND function behavior  
✅ Conditional calculations  
✅ SUMPRODUCT for FTE allocation  
✅ Summary aggregations

## Notes

1. **All calculations match Excel exactly** - The Python backend was reverse-engineered from the original Excel file
2. **No manual overrides** - All values are calculated, not hardcoded
3. **In-scope gating** - Only selected features contribute to calculations
4. **Extensible** - New categories/tasks can be added to the template
5. **Transparent** - All intermediate values are saved in JSON report

## References

- Excel Source: Original FCC Scoping Tool spreadsheet
- Implementation: `/engagement-scoping-tool/backend/core/`
  - `scope_processor.py` - Step 1
  - `effort_calculator.py` - Step 2  
  - `fte_calculator.py` - Step 3
  - `report_generator.py` - Step 4
