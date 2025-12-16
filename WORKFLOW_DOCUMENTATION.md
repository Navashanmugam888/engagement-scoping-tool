# FCCS Scoping Application - Workflow Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Frontend Workflow](#frontend-workflow)
4. [Backend Workflow](#backend-workflow)
5. [Data Flow](#data-flow)
6. [Historical Data Calculation Logic](#historical-data-calculation-logic)
7. [API Endpoints](#api-endpoints)
8. [Field Configuration](#field-configuration)

---

## System Overview

The FCCS (Financial Consolidation and Close) Scoping Application is a web-based tool that helps estimate project effort for Oracle FCCS implementations. It consists of:

- **Frontend**: Next.js application with React components
- **Backend**: Python Flask API server
- **Database**: PostgreSQL for storing scoping history
- **Calculation Engine**: Python-based effort calculator with tier-based adjustments

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                    (Next.js + React)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/JSON
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   API LAYER (Next.js)                        │
│              /api/scoping/submit (route.js)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP POST (Port 5000)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│               PYTHON BACKEND (Flask)                         │
│                  api_server.py                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │               │
        ▼              ▼               ▼
┌──────────────┐ ┌──────────┐ ┌─────────────┐
│ ScopingEngine│ │ PostgreSQL│ │ Report      │
│ (Process)    │ │ Database  │ │ Generator   │
└──────┬───────┘ └───────────┘ └─────────────┘
       │
       ▼
┌──────────────────────────────┐
│   EffortCalculator           │
│   (17 Categories)            │
└──────────────────────────────┘
```

---

## Frontend Workflow

### 1. User Interface Components

#### Main Page: `/app/(app)/fccs-scoping/page.jsx`
- Renders the scoping form with all sections
- Manages form state using React hooks
- Validates user input
- Handles form submission

#### Configuration: `/app/(app)/fccs-scoping/scopingData.js`
Defines all scoping sections and their fields:

```javascript
{
    id: "account",                    // Unique identifier
    label: "Account",                 // Display name
    hasCount: true,                   // true = input field, false = checkbox only
    subItems: [...]                   // Optional child items
}
```

**Field Types:**
- `hasCount: true` → Shows input field for entering numeric details
- `hasCount: false` → Shows only YES/NO checkbox

### 2. User Interaction Flow

```
User Opens Page
     ↓
Fills Scope Definition
     ↓
Selects Implementation Roles
     ↓
Clicks "Calculate Scoping"
     ↓
Frontend Validates Input
     ↓
Sends POST to /api/scoping/submit
```

### 3. Data Preparation (Frontend)

The frontend prepares data in this format:

```javascript
{
    email: "user@example.com",
    scope_inputs: [
        {
            name: "Account",
            in_scope: "YES",        // or "NO"
            details: 500            // numeric value or 0
        },
        {
            name: "Entity Redesign",
            in_scope: "NO",
            details: 0              // Always 0 for hasCount:false fields
        }
        // ... 71 total metrics
    ],
    selected_roles: [
        "PM USA",
        "PM India",
        "Architect USA"
        // ... selected roles
    ]
}
```

---

## Backend Workflow

### 1. API Server: `api_server.py`

**Endpoint:** `POST /api/scope`

**Process:**
1. Receives JSON payload from frontend
2. Validates required fields (email, scope_inputs, selected_roles)
3. Calls ScopingEngine to process the scope
4. Saves result to PostgreSQL database
5. Generates PDF report (optional)
6. Returns calculation results as JSON

### 2. Scoping Engine: `backend/scoping_engine.py`

**Main Function:** `process_scope(scope_inputs, selected_roles)`

**Steps:**

```python
Step 1: Load Configuration
    ├── Load 71 metrics from Scope Definition
    ├── Load formulas from CSV files
    └── Load 13 available roles

Step 2: Calculate Weightage
    ├── Apply formulas to scope_inputs
    ├── Sum total weightage
    └── Determine Implementation Tier (1-4)

Step 3: Calculate Effort
    ├── For each of 17 categories
    │   ├── Get base hours from effort template
    │   ├── Apply tier adjustment
    │   ├── Calculate task-specific hours
    │   └── Sum category total
    └── Calculate grand total

Step 4: Generate Report
    ├── Format results
    ├── Calculate days and months
    └── Return comprehensive result object
```

### 3. Effort Calculator: `backend/core/effort_calculator.py`

**Main Function:** `calculate_task_final_estimate(task_name)`

**17 Categories:**
1. Project Initiation and Planning
2. Creating and Managing EPM Cloud Infrastructure
3. Requirement Gathering, Read back and Client Sign-off
4. Design
5. Build and Configure FCC
6. Setup Application Features
7. Application Customization
8. Calculations
9. Security
10. **Historical Data** ⭐
11. Integrations
12. Reporting
13. Automations
14. Testing/Training
15. Transition
16. Documentations
17. Change Management

**Calculation Formula (Standard Task):**
```python
final_estimate = base_hours + tier_adjustment + (task_hours * details)
```

**Tier Adjustments:**
- Tier 1 (Basic): +0 hours
- Tier 2 (Standard): +8 hours
- Tier 3 (Enhanced): +12 hours
- Tier 4 (Advanced): +16 hours

---

## Historical Data Calculation Logic

### Overview
Historical Data is the most complex category with special calculation rules.

### Tasks in Historical Data Category:

1. **Historical Data Validation** (Parent)
2. **Data Validation for Account Alt Hierarchies** (Child 1)
3. **Data Validation for Entity Alt Hierarchies** (Child 2)
4. **Historical Journal Conversion** (Child 3)

### Input Configuration:

| Task | Frontend Field | Has Input? |
|------|---------------|------------|
| Historical Data Validation | Input field | ✅ YES (user enters numeric details) |
| Account Alt Hierarchies | Checkbox only | ❌ NO (YES/NO only) |
| Entity Alt Hierarchies | Checkbox only | ❌ NO (YES/NO only) |
| Journal Conversion | Checkbox only | ❌ NO (YES/NO only) |

### Calculation Rules:

#### 1. Historical Data Validation (Parent)
```python
# ALWAYS calculates when details > 0
if details > 0:
    hours = (15 + (details + 1) × 10) × 8
```

**Example:**
- Details = 20
- Calculation: (15 + 21 × 10) × 8 = (15 + 210) × 8 = 1,800 hours

#### 2. Data Validation for Account Alt Hierarchies
```python
# Only calculates when in_scope = "YES"
# Uses PARENT's details
if in_scope == "YES":
    parent_details = get_details("Historical Data Validation")
    hours = 20 × parent_details
else:
    hours = 0
```

**Example:**
- In Scope: YES
- Parent Details: 20
- Calculation: 20 × 20 = 400 hours

#### 3. Data Validation for Entity Alt Hierarchies ⭐ SPECIAL
```python
# ALWAYS calculates when "Entity Alternate Hierarchies" has details
# Uses "Entity Alternate Hierarchies" from DIMENSIONS section
entity_alt_details = get_details("Entity Alternate Hierarchies")  # From Dimensions
if entity_alt_details > 0:
    hours = 20 × entity_alt_details
else:
    hours = 0
```

**Example:**
- In Scope: NO (doesn't matter!)
- Entity Alternate Hierarchies (Dimensions): 3
- Calculation: 20 × 3 = 60 hours

**Why is this special?**
This task is linked to the "Entity Alternate Hierarchies" dimension. Even if the user selects NO for this task, it still calculates based on the dimension value. This represents the effort needed to validate entity alternate hierarchies when they exist in the system.

#### 4. Historical Journal Conversion
```python
# Only calculates when in_scope = "YES"
# Uses PARENT's details
if in_scope == "YES":
    parent_details = get_details("Historical Data Validation")
    hours = 20 × parent_details
else:
    hours = 0
```

**Example:**
- In Scope: YES
- Parent Details: 20
- Calculation: 20 × 20 = 400 hours

### Complete Example Calculation:

**Input:**
```javascript
Dimensions:
  - Entity Alternate Hierarchies: YES, details = 3

Historical Data:
  - Historical Data Validation: YES, details = 20
  - Account Alt Hierarchies: YES (checkbox)
  - Entity Alt Hierarchies: NO (checkbox)
  - Journal Conversion: YES (checkbox)
```

**Calculation:**
```
Base + Tier = 60 + 12 = 72 hours

Historical Data Validation:
  (15 + (20+1) × 10) × 8 = 1,800 hours

Account Alt:
  20 × 20 = 400 hours (uses parent's details)

Entity Alt:
  20 × 3 = 60 hours (uses Entity Alternate Hierarchies from Dimensions)

Journal:
  20 × 20 = 400 hours (uses parent's details)

TOTAL = 72 + 1,800 + 400 + 60 + 400 = 2,732 hours
```

---

## Data Flow

### 1. Submission Flow

```
User Input (Frontend)
    ↓
Next.js API Route (/api/scoping/submit)
    ↓
Python Flask Server (Port 5000)
    ↓
ScopingEngine.process_scope()
    ↓
    ├─→ ScopeProcessor (Calculate Weightage & Tier)
    ├─→ EffortCalculator (Calculate Hours)
    ├─→ FTECalculator (Calculate Resources)
    └─→ ReportGenerator (Format Results)
    ↓
Save to PostgreSQL
    ↓
Return JSON Response
    ↓
Display Results (Frontend)
```

### 2. Database Storage

**Table: `scoping_submissions`**

```sql
CREATE TABLE scoping_submissions (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    scope_inputs JSONB NOT NULL,
    selected_roles JSONB NOT NULL,
    result JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Stored Data:**
- User email
- Complete scope inputs (71 metrics)
- Selected roles
- Full calculation results
- Timestamp

### 3. Response Format

```json
{
    "success": true,
    "result": {
        "total_hours": 2732.0,
        "total_days": 341.5,
        "total_months": 11.38,
        "weightage": 112.0,
        "tier": "Tier 3 - Enhanced Scope",
        "categories": [
            {
                "name": "Historical Data",
                "base_hours": 60,
                "tier_adjustment": 12,
                "final_estimate": 2732,
                "in_days": 341.5,
                "tasks": [
                    {
                        "name": "Historical Data Validation",
                        "in_scope": "YES",
                        "details": 20,
                        "final_estimate": 1800
                    }
                    // ... more tasks
                ]
            }
            // ... 16 more categories
        ],
        "roles": [
            {
                "role": "PM USA",
                "allocation": 20,
                "hours_allocated": 546.4
            }
            // ... more roles
        ]
    },
    "submission_id": "scoping_20251209_143022_abc123"
}
```

---

## API Endpoints

### 1. Submit Scoping

**Endpoint:** `POST http://localhost:5000/api/scope`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "scope_inputs": [
        {
            "name": "Account",
            "in_scope": "YES",
            "details": 500
        }
        // ... 71 metrics total
    ],
    "selected_roles": [
        "PM USA",
        "PM India"
        // ... selected roles
    ]
}
```

**Response (Success - 200):**
```json
{
    "success": true,
    "result": { /* calculation results */ },
    "submission_id": "scoping_20251209_143022_abc123"
}
```

**Response (Error - 400/500):**
```json
{
    "error": "Error message description"
}
```

### 2. Get Scoping History

**Endpoint:** `GET /api/scoping/history`

**Query Parameters:**
```
email: user@example.com (optional)
limit: 10 (optional)
```

**Response:**
```json
{
    "success": true,
    "submissions": [
        {
            "id": 123,
            "user_email": "user@example.com",
            "created_at": "2025-12-09T14:30:22",
            "total_hours": 2732.0,
            "tier": "Tier 3"
        }
        // ... more submissions
    ]
}
```

### 3. Download Report

**Endpoint:** `GET /api/scoping/download/:id`

**Response:** PDF file download

---

## Field Configuration

### How to Configure Fields

#### Frontend (`scopingData.js`)
```javascript
{
    id: "field_name",           // Unique identifier
    label: "Display Name",      // Shown to user
    hasCount: true,             // true = input, false = checkbox only
    subItems: [...]             // Optional nested items
}
```

#### Backend (`test_ui.py` for testing)
```python
('Display Name', True, False, 'Section Name')
#                ↑
#                True = requires details
#                False = YES/NO only
```

### Special Cases

#### 1. Fields with Input (hasCount: true)
- Account
- Multi-Currency
- Entity
- Historical Data Validation
- Business Rules
- etc.

#### 2. Fields without Input (hasCount: false)
- Rationalization of CoA
- Entity Redesign
- Multi-GAAP
- Elimination
- All Historical Data child tasks
- etc.

#### 3. Fields with SubItems
```javascript
{
    id: "account",
    label: "Account",
    hasCount: true,
    subItems: [
        { id: "acc_alt_hier", label: "Account Alternate Hierarchies", hasCount: true },
        { id: "rat_coa", label: "Rationalization of CoA", hasCount: false }
    ]
}
```

**Rendering:**
- Parent and all children show as checkboxes
- Input fields only appear for items with `hasCount: true`

---

## Testing

### 1. Interactive Testing

**File:** `test_ui.py`

Run interactive mode:
```bash
python test_ui.py
```

This allows manual testing of the calculation engine by entering scope inputs interactively.

### 2. API Testing

**File:** `test_api.py`

Test the API endpoints:
```bash
python test_api.py
```

### 3. Image Data Testing

**File:** `test_image_data_simple.py`

Test with predefined sample data:
```bash
python test_image_data_simple.py
```

---

## Deployment

### Frontend (Next.js)
```bash
npm run dev          # Development
npm run build        # Production build
npm start            # Production server
```

### Backend (Flask)
```bash
python api_server.py
# Runs on http://localhost:5000
```

### Database Setup
```bash
# Run migration script
psql -U postgres -d scoping_db -f migrations/create_scoping_submissions.sql
```

---

## Troubleshooting

### Common Issues

#### 1. Historical Data Calculation Wrong
- ✅ Check "Entity Alternate Hierarchies" value in Dimensions section
- ✅ Verify Historical Data Validation has numeric details
- ✅ Ensure child tasks are properly marked as YES/NO

#### 2. Frontend Not Showing Input Field
- ✅ Check `hasCount: true` in `scopingData.js`
- ✅ Verify field ID matches backend expectations

#### 3. API Connection Failed
- ✅ Ensure Flask server is running on port 5000
- ✅ Check CORS settings in `api_server.py`
- ✅ Verify database connection

#### 4. Tier Calculation Incorrect
- ✅ Review formulas in `formulas_expanded.csv`
- ✅ Check weightage calculation in `ScopeProcessor`
- ✅ Verify tier boundaries in configuration

---

## Key Takeaways

### For Developers

1. **Historical Data is Special**: It has unique calculation rules that differ from other categories
2. **Entity Alt Links to Dimensions**: Always pulls from "Entity Alternate Hierarchies" field
3. **Two Field Types**: Input fields (`hasCount: true`) vs checkboxes only (`hasCount: false`)
4. **Tier-Based Adjustments**: All categories get base hours plus tier adjustment
5. **Formula-Driven Weightage**: Weightage determines tier, which affects all calculations

### For Users

1. **Only One Input in Historical Data**: Only "Historical Data Validation" needs a number
2. **Entity Alt Always Calculates**: Based on "Entity Alternate Hierarchies" dimension value
3. **71 Metrics Total**: Complete the entire scope definition for accurate results
4. **Select Relevant Roles**: Role selection affects resource allocation
5. **Results are Estimates**: Final hours are guidelines based on industry standards

---

## Contact & Support

For questions or issues:
- Review this documentation first
- Check the `README.md` for setup instructions
- Review `CALCULATIONS_EXPLAINED.md` for formula details
- Check `INTEGRATION_GUIDE.md` for API details

---

**Last Updated:** December 9, 2025
**Version:** 1.0
