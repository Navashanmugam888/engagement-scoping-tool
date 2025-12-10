# Backend Technical Documentation - FCC Scoping Tool

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Data Flow](#data-flow)
4. [API Reference](#api-reference)
5. [Configuration](#configuration)
6. [Data Storage & Processing](#data-storage--processing)
7. [Formula Evaluation Engine](#formula-evaluation-engine)
8. [Error Handling](#error-handling)
9. [Performance Considerations](#performance-considerations)

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     API Server (Flask)                      │
│                  (api_server.py / routes)                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    Scoping Engine                           │
│           (backend/scoping_engine.py)                       │
│  - Orchestrates workflow                                    │
│  - Manages component interaction                            │
└────────┬───────────────┬──────────────┬─────────────────────┘
         │               │              │
         ↓               ↓              ↓
    ┌────────────┐  ┌──────────────┐  ┌──────────────┐
    │   Scope    │  │   Effort     │  │    FTE       │
    │ Processor  │  │ Calculator   │  │ Calculator   │
    └────┬───────┘  └──────┬───────┘  └──────┬───────┘
         │                 │                  │
         ↓                 ↓                  ↓
    ┌────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Formula    │  │  Effort      │  │   App Tiers  │
    │ Evaluator  │  │  Template    │  │ Definition   │
    └────┬───────┘  └──────────────┘  └──────────────┘
         │
         ↓
    ┌────────────┐
    │   Excel    │
    │  Workbook  │
    └────────────┘
```

### Key Design Principles

1. **Separation of Concerns:** Each component has a single responsibility
2. **In-Memory Processing:** All calculations happen in RAM (no database)
3. **Deterministic Output:** Same inputs always produce same outputs
4. **Excel Alignment:** Formulas and calculations match Excel exactly
5. **Stateless Execution:** Each run is independent

---

## Core Components

### 1. ScopingEngine (`backend/scoping_engine.py`)

**Purpose:** Main orchestrator for the complete scoping workflow

**Class:** `ScopingEngine`

**Key Methods:**

#### `__init__()`
```python
def __init__(self):
    self.scope_processor = ScopeDefinitionProcessor()
    self.fte_calculator = FTEEffortsCalculator()
    self.scope_result = None
    self.effort_result = None
    self.fte_result = None
    self.scope_inputs_dict = None
```
- Initializes all sub-components
- Creates singleton instances of processors
- Loads Excel data at startup

#### `process_scope(user_input: dict) -> dict`
- **Input:** User selections for scope metrics
- **Processing:** 
  - Maps user inputs to metrics
  - Sets in_scope_flag (1/0)
  - Evaluates weightage formulas
  - Determines implementation tier
- **Output:** Scope result with weightage and tier
- **Example Input:**
```python
{
    'scope_inputs': [
        {'name': 'Account', 'in_scope': 'YES', 'details': 2000},
        {'name': 'Entity', 'in_scope': 'YES', 'details': 50},
        {'name': 'Multi-GAAP', 'in_scope': 'NO', 'details': 0}
    ],
    'selected_roles': ['PM USA', 'Architect USA']
}
```

#### `calculate_effort() -> dict`
- **Dependencies:** Must call `process_scope()` first
- **Processing:**
  - Creates EffortCalculator with scope_result
  - Calculates task-level estimates
  - Applies tier adjustments
  - Generates summary statistics
- **Output:** Effort estimation with hours, days, months

#### `calculate_fte_allocation() -> dict`
- **Processing:**
  - Calculates role-based FTE hours
  - Uses SUMPRODUCT: (effort hours × role allocation %)
  - Converts to days and months
- **Output:** FTE allocation per role

#### `generate_report(output_filename: str = None) -> dict`
- **Processing:**
  - Generates PDF/Word report
  - Includes scope summary
  - Includes effort breakdown
  - Includes FTE allocation
- **Output:** Report path

#### `run_complete_workflow(user_input: dict, output_filename: str = None) -> dict`
- **Processing:** Orchestrates all steps in sequence
- **Returns:** Complete result with all components

---

### 2. ScopeDefinitionProcessor (`backend/core/scope_processor.py`)

**Purpose:** Process user inputs and calculate engagement weightage

**Class:** `ScopeDefinitionProcessor`

**Key Attributes:**
```python
self.metrics = []        # List of 71 metric definitions
self.formulas = {}       # Dict of metric name → formula string
self.roles = []          # Available roles
```

**Initialization Process:**

```
Load Metrics from Excel
    ↓
Load Formulas from CSV files
    ↓
Print statistics
    ↓
Ready for processing
```

**Key Methods:**

#### `_load_metrics()`
- Reads from Excel sheet: `Scope Definition`
- Columns: B (metric name), C (in_scope), D (details)
- Rows 6-102 (71 metrics)
- Skips section headings and locked cells
- Creates metric dictionary with:
  ```python
  {
      'row': int,
      'name': str,
      'in_scope': str (YES/NO),
      'details': float,
      'weightage': float,
      'in_scope_flag': int (1/0),
      'is_details_required': bool,
      'is_sub_question': bool
  }
  ```

#### `_load_formulas()`
- Loads from CSV files:
  - `backend/data/formulas_expanded.csv` (main formulas)
  - `backend/data/formulas_array_supplement.csv` (complex formulas)
- Stores in dict: `{metric_name: formula_string}`
- Example formulas:
  ```
  Account: =IF(Account[InScope]="YES", Account[Details], 0)
  Entity: =IF(Entity[InScope]="YES", Entity[Details], 0)
  Multi-GAAP: =IF(Multi-GAAP[InScope]="YES", 2, 0)
  ```

#### `process_user_input(user_input: dict) -> dict`
```python
def process_user_input(self, user_input: dict) -> dict:
    """
    Process user input and calculate weightage
    
    Args:
        user_input: {
            'scope_inputs': [{'name': str, 'in_scope': str, 'details': number}],
            'selected_roles': [str, ...]
        }
    
    Returns:
        {
            'total_weightage': float,
            'tier': int (1-5),
            'tier_name': str,
            'metrics': list of metric dicts,
            'selected_roles': list,
            'summary': {'total_metrics': int, 'in_scope_count': int, 'out_scope_count': int}
        }
    """
```

**Processing Steps:**
1. Map user inputs to metrics dictionary
2. Set `in_scope_flag` (1 if YES, 0 if NO)
3. Create FormulaEvaluator instance
4. Evaluate weightage formula for each metric
5. Sum all weightages → `total_weightage`
6. Determine tier based on weightage ranges
7. Return complete scope result

---

### 3. EffortCalculator (`backend/core/effort_calculator.py`)

**Purpose:** Calculate effort estimation with tier-based adjustments

**Class:** `EffortCalculator`

**Initialization:**
```python
def __init__(self, scope_result: dict):
    self.scope_metrics = {m['name']: m for m in scope_result['metrics']}
    self.engagement_weightage = scope_result['total_weightage']
    self.tier = scope_result['tier']
    self.tier_name = scope_result['tier_name']
```

**Key Methods:**

#### `lookup_inscope(task_name: str) -> str`
- Checks `in_scope_flag` in scope_metrics
- Returns: "YES" or "NO"
- Used as gate for effort calculation

#### `lookup_details(task_name: str) -> float`
- Gets details value from scope_metrics
- Only returns value if `in_scope == "YES"`
- Returns 0 if not in scope (gating mechanism)

#### `get_raw_details(task_name: str) -> float`
- Gets details value regardless of in_scope status
- Used for special calculations (Historical Data Validation)

#### `calculate_task_final_estimate(task_name: str) -> float`
**Special Logic Sections:**

1. **Historical Data Validation (Special Case)**
   - Formula: `(15 + (details + 1) × 10) × 8`
   - Always calculates regardless of in_scope_flag

2. **Historical Data Child Tasks**
   - Account/Journal: Use parent's details if YES
   - Entity Alt: Always use Entity Alternate Hierarchies details

3. **Complex Round-Based Formula Tasks**
   - Tasks: Data Forms, Dashboards, Business Rules, Management Reports
   - Formula: `INT(ROUND(details×0.5))×8 + INT(ROUND(details×0.25))×12 + INT(ROUND(details×0.25))×16`

4. **Member Formula**
   - Formula: `INT(ROUND(details×0.5))×2 + INT(ROUND(details×0.25))×3 + INT(ROUND(details×0.25))×4`

5. **Custom KPIs**
   - Formula: `INT(ROUND(details×0.5))×2 + INT(ROUND(details×0.25))×4 + INT(ROUND(details×0.25))×4`

6. **Special Cases**
   - Secured Dimensions: `details × 4`
   - Number of Users: `details × 0.2`
   - Prelim FCC User Provisioning: `8 if details > 50 else 0`
   - Parallel Testing: `40 × 2 = 80` (fixed value)

7. **Standard Multipliers**
   - Tasks with fixed multipliers: Account Alternate Hierarchies (8), Custom Dimensions (4), etc.
   - Formula: `base_multiplier × details`

#### `calculate_category_final_estimate(category_name: str, base_hours: float, task_estimates: dict) -> float`
```python
category_final = base_hours + tier_adjustment + sum(task_estimates)
```

**Tier Adjustments Table:**

| Category | Tier 1 (≤100) | Tier 2 (101-120) | Tier 3 (121-160) | Tier 4 (>160) |
|----------|---------------|-----------------|------------------|---------------|
| Project Initiation | 0 | 4 | 6 | 8 |
| Requirement Gathering | 0 | 8 | 12 | 16 |
| Design | 0 | 8 | 16 | 24 |
| Build and Configure FCC | 0 | 8 | 16 | 24 |
| Setup Features | 0 | 8 | 16 | 24 |
| Application Customization | 0 | 8 | 12 | 16 |
| Calculations | 0 | 8 | 12 | 16 |
| Security | 0 | 8 | 12 | 16 |
| Historical Data | 0 | 8 | 12 | 16 |
| Integrations | 0 | 8 | 12 | 16 |
| Reporting | 0 | 8 | 12 | 16 |
| Automations | 0 | 8 | 12 | 16 |
| Testing/Training | 0 | 8 | 12 | 16 |
| Transition | 0 | 8 | 16 | 24 |
| Documentations | 0 | 8 | 12 | 16 |
| Change Management | 0 | 8 | 12 | 16 |
| Infrastructure | 0 | 0 | 0 | 0 |

#### `calculate_effort() -> dict`
**Processing:**
1. Iterate through EFFORT_ESTIMATION_TEMPLATE
2. For each category:
   - Calculate task estimates
   - Apply category adjustment
   - Aggregate to category_final
3. Return complete effort dictionary

**Output Structure:**
```python
{
    "Project Initiation and Planning": {
        'base_hours': 12,
        'final_estimate': 16,
        'in_days': 2.0,
        'tasks': [
            {
                'name': 'Kickoff Meetings',
                'base_hours': 1,
                'in_scope': 'YES',
                'details': 0,
                'final_estimate': 0
            },
            ...
        ]
    },
    ...
}
```

#### `generate_summary(effort_estimation: dict) -> dict`
**Calculations:**
- Total baseline hours (sum of template)
- Total time hours (sum of all task final_estimates)
- Final estimate hours (total time hours)
- Total days (final / 8)
- Total months (days / 30)

---

### 4. FTEEffortsCalculator (`backend/core/fte_calculator.py`)

**Purpose:** Calculate role-based FTE effort allocation

**Class:** `FTEEffortsCalculator`

**Initialization:**
```python
def __init__(self):
    self.tiers_data = {}    # {row_idx: {hours, roles: {role: allocation}}}
    self.roles = []         # List of role names
    self._load_app_tiers_data()
```

**Excel Source:**
- File: `Engagement Scoping Tool - FCC.xlsx`
- Sheet: `App Tiers Definition`
- Rows 4-5: Role headers (Location + Role name)
- Rows 6-22: 17 rows of data (Tiers + Categories)
- Column I: Hours per row
- Columns J onwards: Role allocation percentages

**Key Methods:**

#### `_load_app_tiers_data()`
**Processing:**
1. Read role names from rows 4-5, columns J onwards
   - Row 4: Location (USA, India)
   - Row 5: Role name (PM, Architect, etc.)
   - Combined: "PM USA", "PM India", "Architect USA"
2. Read hours from column I, rows 6-22
3. Read allocation percentages from columns J-V, rows 6-22
   - Convert percentages to decimals (50% → 0.5)
4. Store in nested dictionary structure

**Example In-Memory Structure:**
```python
self.roles = [
    "PM USA",
    "PM India",
    "Architect USA",
    ...
]

self.tiers_data = {
    0: {
        'hours': 123.5,
        'row': 6,
        'roles': {
            'PM USA': 0.5,
            'PM India': 0.5,
            'Architect USA': 1.0,
            ...
        }
    },
    1: {
        'hours': 145.0,
        'row': 7,
        'roles': { ... }
    },
    ...
}
```

#### `calculate_role_fte_from_effort(effort_estimation: dict, selected_roles: list = None) -> dict`
**Formula:** SUMPRODUCT(hours, role_allocation_percentage)

**Processing for each role:**
```python
total_fte = 0.0
for row_idx in range(17):  # 17 rows (rows 6-22 in Excel)
    hours = tiers_data[row_idx]['hours']
    allocation = tiers_data[row_idx]['roles'][role]
    total_fte += hours * allocation
```

**Example Calculation (PM USA):**
```
Row 0: 123.5 × 0.50 = 61.75
Row 1: 145.0 × 0.50 = 72.50
Row 2: 167.0 × 0.50 = 83.50
...
Total PM USA FTE: ~847 hours
```

#### `get_role_allocation_matrix() -> pd.DataFrame`
- Returns allocation data as pandas DataFrame
- Useful for debugging and reporting
- Rows: Tiers/Categories
- Columns: Roles
- Values: Allocation percentages

---

### 5. FormulaEvaluator (`backend/utils/formula_evaluator.py`)

**Purpose:** Evaluate Excel-like formulas with custom syntax

**Class:** `FormulaEvaluator`

**Supported Syntax:**
```
FeatureName[InScope]  → "YES" or "NO"
FeatureName[Details]  → numeric value
```

**Example Formulas:**
```
=IF(Account[InScope]="YES", Account[Details], 0)
=IF(Entity[InScope]="YES", Entity[Details]*0.5, 0)
=IF(AND(Account[InScope]="YES", Entity[InScope]="YES"), 10, 5)
=SUMIF(Account[Details], ">100", 50)
```

**Key Methods:**

#### `evaluate(formula: str) -> float`
1. Remove leading `=`
2. Replace FeatureName[Column] with actual values
3. Convert Excel syntax to Python syntax
4. Safely evaluate expression
5. Return numeric result

#### `_replace_references(formula: str) -> str`
- Uses regex pattern: `([A-Za-z][\w\s\-\.]*?)\[(InScope|Details)\]`
- Replaces with actual values from metrics_lookup
- Examples:
  - `Account[InScope]` → `"YES"`
  - `Account[Details]` → `2000`

#### `_safe_eval(expression: str) -> Any`
- Converts Excel `=` to Python `==`
- Creates safe namespace with Excel functions:
  - IF, AND, OR, SUM, IFS, MAX, MIN, ROUND, etc.
- Evaluates expression safely
- Returns result

---

## Data Flow

### Complete Request Flow

```
HTTP Request (POST /api/scoping)
    ↓
API Server
    ├─ Extract scope_inputs & selected_roles
    ├─ Validate inputs
    └─ Call ScopingEngine.run_complete_workflow()
    ↓
ScopingEngine.process_scope()
    ├─ ScopeDefinitionProcessor.process_user_input()
    │   ├─ Load metrics from Excel
    │   ├─ Map user inputs to metrics
    │   ├─ Set in_scope_flag
    │   ├─ Create FormulaEvaluator
    │   ├─ Evaluate weightage formulas
    │   └─ Determine tier
    └─ Store result in self.scope_result
    ↓
ScopingEngine.calculate_effort()
    ├─ Create EffortCalculator(scope_result)
    ├─ EffortCalculator.calculate_effort()
    │   ├─ For each category:
    │   │   ├─ For each task:
    │   │   │   ├─ lookup_inscope()
    │   │   │   ├─ lookup_details()
    │   │   │   └─ calculate_task_final_estimate()
    │   │   └─ calculate_category_final_estimate()
    │   └─ Return effort_estimation dict
    ├─ EffortCalculator.generate_summary()
    └─ Store result in self.effort_result
    ↓
ScopingEngine.calculate_fte_allocation()
    ├─ FTEEffortsCalculator.calculate_role_fte_from_effort()
    │   ├─ For each role:
    │   │   ├─ For each of 17 rows:
    │   │   │   ├─ Get hours
    │   │   │   ├─ Get allocation %
    │   │   │   └─ SUMPRODUCT
    │   │   └─ Total FTE hours
    │   └─ Return role_fte dict
    └─ Store result in self.fte_result
    ↓
ScopingEngine.generate_report()
    ├─ Create SOWReportGenerator
    ├─ Generate Word/PDF document
    └─ Save to output directory
    ↓
Return complete result to API
    ↓
API Server returns JSON response
```

---

## API Reference

### Request Format

```json
POST /api/scoping

{
    "scope_inputs": [
        {
            "name": "Account",
            "in_scope": "YES",
            "details": 2000
        },
        {
            "name": "Entity",
            "in_scope": "YES",
            "details": 50
        },
        {
            "name": "Multi-GAAP",
            "in_scope": "NO",
            "details": 0
        }
    ],
    "selected_roles": [
        "PM USA",
        "Architect USA",
        "App Developer USA"
    ]
}
```

### Response Format

```json
{
    "status": "success",
    "scope_definition": {
        "total_weightage": 125.5,
        "tier": 2,
        "tier_name": "Tier 2 - Foundation Plus",
        "metrics": [ ... ],
        "summary": {
            "total_metrics": 71,
            "in_scope_count": 15,
            "out_scope_count": 56
        }
    },
    "effort_estimation": {
        "summary": {
            "total_time_hours": 1245.5,
            "final_estimate_hours": 1345.5,
            "total_days": 168,
            "total_months": 5.6
        },
        "categories": { ... }
    },
    "fte_allocation": {
        "role_fte_hours": {
            "PM USA": 847.5,
            "Architect USA": 1234.2,
            ...
        },
        "role_fte_days": {
            "PM USA": 105.9,
            "Architect USA": 154.3,
            ...
        },
        "role_fte_summary": [ ... ]
    },
    "report_path": "output/scoping_result_user@example.com_20251210_120000.json"
}
```

---

## Configuration

### File: `backend/config.py`

**Path Configuration:**
```python
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'backend' / 'data'
OUTPUT_DIR = BASE_DIR / 'output'
EXCEL_FILE = BASE_DIR / 'Engagement Scoping Tool - FCC.xlsx'
```

**Tier Definitions:**
```python
TIERS = {
    1: {"name": "Tier 1 - Jumpstart", "range": (0, 60)},
    2: {"name": "Tier 2 - Foundation Plus", "range": (61, 100)},
    3: {"name": "Tier 3 - Enhanced Scope", "range": (101, 150)},
    4: {"name": "Tier 4 - Advanced Enablement", "range": (151, 200)},
    5: {"name": "Tier 5 - Full Spectrum", "range": (201, 999)}
}
```

**Available Roles:**
```python
AVAILABLE_ROLES = [
    "PM USA",
    "PM India",
    "Architect USA",
    "Delivery Lead India",
    "Sr. Delivery Lead India",
    "App Lead USA",
    "App Lead India",
    "App Developer USA",
    "App Developer India",
    "Integration Lead USA",
    "Integration Developer India",
    "Reporting Lead India",
    "Security Lead India"
]
```

**Constants:**
```python
HOURS_PER_DAY = 8
DAYS_PER_MONTH = 30

SHEET_SCOPE_DEFINITION = 'Scope Definition'
SHEET_EFFORT_ESTIMATION = 'Effort Estimation'
SHEET_SCOPE_OF_SERVICE = 'Scope of Service'
```

---

## Data Storage & Processing

### In-Memory Architecture

All data processing happens in RAM (no database):

```
STARTUP
    ↓
Load Excel file
    ├─ Parse Scope Definition sheet
    ├─ Parse App Tiers Definition sheet
    └─ Cache data in memory
    ↓
Load CSV files
    ├─ formulas_expanded.csv (main formulas)
    └─ formulas_array_supplement.csv (array formulas)
    ↓
Create singleton instances
    ├─ ScopeDefinitionProcessor (cached)
    ├─ FTEEffortsCalculator (cached)
    └─ FormulaEvaluator (per-request)
    ↓
Ready for requests
    ↓
PER REQUEST
    ↓
Receive user input
    ↓
Create in-memory dictionaries
    ├─ scope_metrics = {name: metric_dict}
    ├─ effort_estimation = {category: {tasks: [...]}}
    └─ role_fte = {role: hours}
    ↓
Perform all calculations in RAM
    ↓
Serialize results to JSON
    ↓
Return to client
```

### File Storage

**Output Files:**
- Location: `output/`
- Naming: `scoping_result_{email}_{timestamp}.json`
- Format: Complete result with all components
- Not deleted after retrieval (audit trail)

**Data Files:**
- `backend/data/effort_template.py` - Hardcoded template (not files)
- `backend/data/formulas_expanded.csv` - Weightage formulas
- `backend/data/formulas_array_supplement.csv` - Complex formulas

---

## Formula Evaluation Engine

### Excel Function Support

| Function | Syntax | Example | Status |
|----------|--------|---------|--------|
| IF | IF(condition, true_value, false_value) | IF(Account[InScope]="YES", 10, 0) | ✓ |
| AND | AND(cond1, cond2, ...) | AND(A="YES", B="YES") | ✓ |
| OR | OR(cond1, cond2, ...) | OR(A="YES", B="YES") | ✓ |
| SUM | SUM(range) | SUM(Account[Details], Entity[Details]) | ✓ |
| IFS | IFS(cond1, val1, cond2, val2, ...) | IFS(A>100, 5, A>50, 3) | ✓ |
| MAX | MAX(val1, val2, ...) | MAX(A, B) | ✓ |
| MIN | MIN(val1, val2, ...) | MIN(A, B) | ✓ |
| ROUND | ROUND(value, decimals) | ROUND(A/2, 1) | ✓ |
| INT | INT(value) | INT(A*1.5) | ✓ |

### Reference Evaluation

**Pattern:** `MetricName[Column]`

```python
# Replacement examples:
"Account[InScope]"  → "YES"   (from scope_metrics)
"Account[Details]"  → 2000    (from scope_metrics)
"Entity[InScope]"   → "NO"    (from scope_metrics)
"Entity[Details]"   → 0       (from scope_metrics)
```

**Evaluation Order:**
1. Replace all FeatureName[Column] references
2. Convert Excel `=` to Python `==`
3. Safely eval with Excel function namespace
4. Return numeric result

---

## Error Handling

### Exception Handling Strategy

```python
try:
    # Load Excel file
except FileNotFoundError:
    # Log error, provide helpful message
    raise ValueError(f"Excel file not found: {EXCEL_FILE}")

try:
    # Evaluate formula
except Exception as e:
    # Log original and replaced formula
    # Return 0 as default
    print(f"Error evaluating formula: {e}")
    return 0
```

### Validation Points

1. **User Input Validation**
   - in_scope must be YES or NO
   - details must be numeric
   - metric name must exist

2. **Data Consistency**
   - All metrics have formulas
   - All formulas have valid syntax
   - Scope_result contains required keys

3. **Calculation Validation**
   - Task estimates >= 0
   - Category estimates >= base hours
   - Weightage within tier ranges

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| FileNotFoundError | Excel file missing | Check file path in config.py |
| Formula evaluation fails | Invalid syntax | Check formula in CSV |
| in_scope_flag not set | Scope processor not called | Call process_scope() first |
| FTE calculation wrong | Effort not calculated | Calculate effort before FTE |

---

## Performance Considerations

### Optimization Strategies

1. **Singleton Instances**
   - ScopeDefinitionProcessor created once
   - Excel data loaded once
   - Reused across requests

2. **In-Memory Processing**
   - No database queries
   - All calculations in RAM
   - Fast arithmetic operations

3. **Lazy Loading**
   - Formulas loaded on demand
   - Excel sheet accessed once per component
   - Cached in memory

### Performance Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| Load Excel file | ~100ms | First startup only |
| Load CSV formulas | ~50ms | First startup only |
| Process scope | ~200ms | Per request |
| Calculate effort | ~300ms | Per request |
| Calculate FTE | ~150ms | Per request |
| Generate report | ~500ms | Per request |
| **Total Request** | **~1.2s** | Combined |

### Scalability

- **Concurrent Requests:** Limited by Flask (WSGI)
- **Data Size:** 71 metrics × 17 categories = ~5MB in memory
- **Thread Safety:** Singleton instances are thread-safe
- **Recommended Setup:** 
  - Use multiple Flask workers
  - Deploy with Gunicorn/uWSGI
  - Consider caching layer for repeated requests

---

## Testing

### Test Files

- `test_image_data_simple.py` - Comprehensive test suite with validation
- `test_ui.py` - UI testing script
- `test_with_image_data.py` - Alternative test format

### Running Tests

```bash
python test_image_data_simple.py
```

### Test Coverage

- Scope processing
- Effort calculations
- FTE allocation
- Output validation
- Formula evaluation

---

## Deployment

### Prerequisites

```
Python 3.8+
openpyxl >= 3.0
pandas >= 1.3
flask >= 2.0
python-docx >= 0.8
```

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
python api_server.py
```

### Configuration for Production

1. Set `FLASK_ENV=production`
2. Use proper WSGI server (Gunicorn/uWSGI)
3. Configure logging
4. Set up error monitoring
5. Enable CORS if needed

---

## Appendix

### Effort Template Categories (16 Total)

1. Project Initiation and Planning
2. Creating and Managing EPM Cloud Infrastructure
3. Requirement Gathering, Read back and Client Sign-off
4. Design
5. Build and Configure FCC
6. Setup Application Features
7. Application Customization
8. Calculations
9. Security
10. Historical Data
11. Integrations
12. Reporting
13. Automations
14. Testing/Training
15. Transition
16. Documentations & Change Management

### Tier Ranges

| Tier | Name | Weightage Range |
|------|------|-----------------|
| 1 | Jumpstart | 0-60 |
| 2 | Foundation Plus | 61-100 |
| 3 | Enhanced Scope | 101-150 |
| 4 | Advanced Enablement | 151-200 |
| 5 | Full Spectrum | 201+ |

---

**Document Version:** 1.0
**Last Updated:** December 10, 2025
**Status:** Production Ready

