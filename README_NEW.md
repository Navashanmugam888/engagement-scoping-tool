# FCC Engagement Scoping Tool

Automated effort estimation and resource allocation calculator for Oracle EPM Financial Consolidation and Close (FCC) implementations. Generates comprehensive Statement of Work (SOW) reports with scope definition, effort estimation, and team resource allocation.

## Overview

This tool processes engagement scope definitions and automatically calculates:
- **Engagement Weightage**: Based on 71 scope complexity metrics
- **Implementation Tier**: Determines tier level (1-5) from weightage (Tier 1: 0-60, Tier 2: 61-100, Tier 3: 101-150, Tier 4: 151-200, Tier 5: 201-999)
- **Effort Estimation**: Calculates hours per category with tier adjustments (16 categories, total 1892.5 hours for Tier 3)
- **FTE Allocation**: Distributes effort across 13 implementation roles using SUMPRODUCT formula
- **Statement of Work**: Generates comprehensive SOW report as Word document with 3 sections:
  1. Scope of Service (dimensions, features, customizations)
  2. Timings (start/end dates, monthly resource allocation table)
  3. Key Design Decisions (4 defaults + conditional KDD items)

## Quick Start

### 1. Install Dependencies
```bash
pip install openpyxl pandas python-docx
```

### 2. Run Interactive Workflow
```bash
python test_ui.py
```

You will be prompted to:
1. Enter scope definition (in_scope: YES/NO, details: numeric value) for 71 metrics
2. Select implementation roles from 13 available roles (with USA/India locations)
3. Specify output filename

The tool will:
- Calculate engagement weightage (0-999)
- Determine implementation tier (1-5)
- Calculate total effort (hours, days, months)
- Allocate FTE across selected roles
- Generate SOW report as Word document (.docx)

### 3. Review Output
Output files in `output/` directory:
- `*.json`: Detailed JSON report with all calculations
- `*.docx`: Professional Word document with SOW (Scope, Timings, KDD)

## Architecture

### Core Modules

#### `backend/core/scope_processor.py`
Processes user input and calculates engagement weightage.

**Input**: 
```python
{
    'scope_inputs': [
        {'name': 'Account', 'in_scope': 'YES', 'details': 2000},
        {'name': 'Entity', 'in_scope': 'YES', 'details': 25},
        ...  # 71 total metrics
    ],
    'selected_roles': ['PM USA', 'Architect USA', ...]
}
```

**Output**:
```python
{
    'total_weightage': 130.0,
    'tier': 3,
    'tier_name': 'Tier 3 - Enhanced Scope',
    'metrics': [...],  # 71 metrics with calculated weightages
    'selected_roles': [...],
    'summary': {'total_metrics': 71, 'in_scope_count': 51, 'out_scope_count': 20}
}
```

**Key Features**:
- Loads 71 metrics from Scope Definition sheet (Column B)
- For each metric: gets in_scope (YES/NO) from Column C, details from Column D
- Sets `in_scope_flag`: 1 if in_scope='YES', else 0 (CRITICAL gate for all effort)
- Evaluates weightage formulas using FormulaEvaluator (61 formulas + 8 array formulas)
- Sums all metric weightages to get total_weightage
- Determines tier based on weightage range

#### `backend/core/effort_calculator.py`
Calculates effort estimation with tier-based adjustments.

**Input**: scope_result (from ScopeDefinitionProcessor)

**Output**:
```python
{
    'Project Initiation and Planning': {'final_estimate': 18.0, 'in_days': 2.25},
    'Design': {'final_estimate': 42.0, 'in_days': 5.25},
    ...  # 16 categories
    'summary': {
        'total_time_hours': 1892.5,
        'total_days': 236.56,
        'total_months': 7.89
    }
}
```

**Key Features**:
- 92 total tasks: 34 with formulas, 58 that equal 0
- All efforts gated by `in_scope_flag` (if flag=0, effort=0)
- 16 categories with tier-based adjustments (4 scaling patterns)
- **CRITICAL FIX**: Data validation tasks (rows 86-88) use shared "Historical Data Validation" details
  - Excel formulas hardcoded to 'Scope Definition'!D54
  - Python implementation: lines 146-157 use shared dependency
  - Effect: +120 hours to Historical Data category (432 → 552 hours)
- Custom Excel ROUND implementation (round-half-up): `math.floor(value + 0.5)`
- Result: Exactly 1892.5 hours for standard Tier 3 engagement

#### `backend/core/fte_calculator.py`
Calculates role-based FTE effort allocation.

**Input**: 
- effort_estimation: Dict with 16 categories and final_estimate hours
- selected_roles: List of role names (e.g., ['PM USA', 'Architect USA'])

**Output**:
```python
{
    'PM USA': 946.25,
    'PM India': 946.25,
    'Architect USA': 460.50,
    ...
}
```

**Key Formula - SUMPRODUCT**:
```
For each role:
  total_fte = SUM(category_hours[i] × role_allocation%[role][i]) for i in 6-22
```
Where:
- Rows 6-22 in App Tiers Definition represent 17 rows (5 tiers + 12 categories)
- Column I = Hours (references Effort Estimation)
- Columns J-V = Role allocation percentages (0-1)
- Result: Each role gets proportional hours based on their allocation

**Example Calculation**:
- PM USA: 50% allocation across categories
  - Project Initiation (18 × 50%) + Design (42 × 50%) + ... = 946.25 hours
  - Divided by 8 months = 118 hours/month

#### `backend/core/sow_report_generator.py`
Generates comprehensive Statement of Work report.

**Input**: 
- scope_result, effort_estimation, summary, role_fte, selected_roles

**Output**: 
- Word document (.docx) with 3 professional sections

**Section 1: Scope of Service**
- Engagement tier (based on weightage)
- Dynamic dimensions (accounts, hierarchies, entities, currencies, etc.)
- Application features (elimination, journals, consolidation, etc.)
- Application customization (data forms, business rules, member formulas)
- Security and standard dimensions

**Section 2: Timings (Effort Estimation)**
- Start date: TODAY()
- End date: TODAY() + months (rounded)
- Total duration: {months} months
- Category breakdown: All 16 categories with hours and days
- Monthly resource table: Shows each role's monthly hours (total_hours / months)
- Timeline assumptions: 8 hrs/day, 30 days/month

**Section 3: Key Design Decisions (KDD)**
- **4 Default KDDs** (always included):
  1. General Application Configuration
  2. Metadata Configuration
  3. FCC Consolidations and Other Calculations
  4. Reports and Data Form Configuration
- **Conditional KDDs** (included if scope value > 0):
  - KDD05: Ownership Management (if E26 > 0)
  - KDD06: Cash Flow (if E31 > 0)
  - KDD07: Journal Process (if E23 > 0)
  - KDD08: Integrations (if F59 > 0)
  - KDD09: Historical Data (if F53 > 0)
  - KDD10: Automations (if F75 > 0)
  - KDD11: Approval Process (if E34 > 0)
  - KDD12: Task Manager (if E36 > 0)
  - KDD13: Supplemental Data (if E32 > 0)
  - KDD14: Enterprise Journals (if E33 > 0)
  - KDD15: Application Security (if F49 > 0)
  - KDD16: Audit (if E37 > 0)

#### `backend/core/effort_template.py`
Defines the 16 implementation categories.

#### `backend/utils/formula_evaluator.py`
Evaluates Excel-like formulas with dynamic metric values.

**Syntax**: FeatureName[Column]
- FeatureName[InScope] = YES/NO value
- FeatureName[Details] = numeric details value

#### `backend/config.py`
Configuration constants.

- 13 available roles: PM USA/India, Architect USA, Delivery Leads, App Leads, Developers, Integration roles, Reporting Lead, Security Lead
- 5 tier definitions with ranges and names
- Excel file path and sheet names

### Data Files

- `backend/data/formulas_expanded.csv`: 61 metric weightage formulas
- `backend/data/formulas_array_supplement.csv`: 8 supplemental array formulas

## Key Concepts

### in_scope_flag - The Critical Gate
**Most Important Concept**: Binary gate (0/1) that determines whether effort is calculated.

```python
in_scope_flag = 1 if in_scope == 'YES' else 0
```

- All 92 tasks check this flag before calculating effort
- If flag = 0, effort = 0 (regardless of details value)
- This is the primary control for filtering out of-scope work

### Engagement Weightage Calculation
Sum of all metric weightages (0-999) that determines implementation tier.

```
Total Weightage = SUM(metric_weightage for all 71 metrics)
  where: metric_weightage = formula evaluation using in_scope and details values
```

### Tier Adjustment Patterns
16 categories apply tier-based effort adjustments using 4 patterns.

### Historical Data Dependencies - Critical Bug Fix
**Issue**: Data validation tasks (3 tasks) were hardcoded to wrong cell references
- Row 86: Data Validation for Account Alt Hierarchies
- Row 87: Data Validation for Entity Alt Hierarchies
- Row 88: Historical Journal Conversion

**Root Cause**: Excel formulas referenced 'Scope Definition'!D54 (Historical Data Validation details) instead of their own details

**Fix**: Python implementation (effort_calculator.py, lines 146-157) uses shared dependency

**Impact**: +120 hours to Historical Data category when details=2

### Excel ROUND vs Python Rounding
Excel uses "round half up", Python uses "banker's rounding" (round half to even).

**Implementation**:
```python
def excel_round(value, places=0):
    multiplier = 10 ** places
    return math.floor(value * multiplier + 0.5) / multiplier
```

## Workflow - Complete Flow

```
START
  ↓
[Step 1] Scope Processing
  Input: 71 metrics (in_scope: YES/NO, details: number)
  Output: scope_result dict
  ↓
[Step 2] Effort Estimation
  Input: scope_result
  Output: effort_estimation dict (total: 1892.5 hours for Tier 3)
  ↓
[Step 3] FTE Allocation
  Input: effort_estimation + selected_roles
  Output: role_fte dict
  ↓
[Step 4] Report Generation
  Input: scope_result + effort_estimation + role_fte
  Output: Word document (.docx)
  ↓
END (Save to output/ directory)
```

## Running the Tool

### Interactive Test - Full Workflow
```bash
python test_ui.py
```

Prompts for:
1. Scope input (71 metrics)
2. Role selection (13 available roles)
3. Output filename

Output: JSON report + Word document

### Automated Test - Predefined Data
```bash
python test_image_data_simple.py
```

Tests with fixed scope data:
- 51 metrics in scope, 20 out of scope
- Expected result: 1892.5 hours (Tier 3)
- Validates all 16 categories

### FTE Verification Test
```bash
python test_fte_verification.py
```

Tests FTE calculation against expected values:
- All 13 roles calculated
- Validates SUMPRODUCT formula
- Checks exact match with Excel values

## Output Files

Generated in `output/` directory:

**JSON Report** (`*.json`)
- Complete scope definition with calculated weightages
- Effort estimation by category
- Summary: total hours, days, months
- Role FTE allocation

**Word Document** (`*.docx`)
- Professional SOW report (Scope, Timings, KDD)
- Ready for client delivery
- Includes start/end dates, resource tables
- Dynamic scope descriptions

## Testing Best Practices

1. **Always test with known Excel data** to verify calculations match
2. **Run FTE verification** to ensure SUMPRODUCT formula works correctly
3. **Validate report formatting** in generated Word document
4. **Check conditional KDD items** appear based on scope selection
5. **Verify start/end dates** are calculated correctly

## Maintenance Notes

### Critical Items - Do NOT Modify Without Testing
1. Historical Data category formula (lines 146-157 in effort_calculator.py)
2. SUMPRODUCT logic in fte_calculator.py (must use all 17 rows)
3. in_scope_flag gating in all effort calculations
4. Excel ROUND implementation (must use round-half-up)

### Excel File Dependencies
- Scope Definition sheet: 71 metrics in rows 6-100, columns B-D
- Effort Estimation sheet: Category hours in column G
- App Tiers Definition sheet: 17 rows (6-22), roles in rows 4-5, allocation % in columns J-V
- Definitions sheet: KDD descriptions in cells B138-B149

## Version History

### v2.0.0 - Complete SOW Report Generation (Dec 2025)
- Integrated report generator with scoping engine
- Word document generation with python-docx
- Dynamic Scope of Service section
- Timings section with monthly resource allocation
- Key Design Decisions with conditional KDD items
- Complete end-to-end workflow tested and validated

### v1.0.0 - Initial Release (Dec 2025)
- Scope processing with 71 metrics
- Effort estimation with 16 categories
- FTE allocation for 13 roles
- Critical fix: Historical Data dependencies
- SUMPRODUCT formula implementation
- JSON report generation
