# Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             USER BROWSER                                     │
│                         http://localhost:3001                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ User fills form
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          NEXT.JS FRONTEND                                    │
│  ┌─────────────────────┐                    ┌──────────────────────┐       │
│  │  FCCS Scoping Page  │                    │  Scoping History     │       │
│  │  /fccs-scoping      │                    │  /scoping-history    │       │
│  │                     │                    │                      │       │
│  │  • Scope Inputs     │                    │  • View Results      │       │
│  │  • Role Selection   │                    │  • Download Reports  │       │
│  │  • Submit Button    │                    │  • Filter by User    │       │
│  └─────────────────────┘                    └──────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ API Calls
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NEXT.JS API ROUTES (Proxy)                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │ /api/scoping/    │  │ /api/scoping/    │  │ /api/scoping/    │         │
│  │ submit           │  │ history          │  │ download/[id]    │         │
│  │                  │  │                  │  │                  │         │
│  │ POST             │  │ GET              │  │ GET              │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Forward to Python
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PYTHON FLASK API SERVER                                   │
│                    http://localhost:5000                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  api_server.py - Flask Routes                                        │  │
│  │                                                                       │  │
│  │  POST /api/scoping/submit      → Process submission                 │  │
│  │  GET  /api/scoping/history     → Get user history                   │  │
│  │  GET  /api/scoping/result/{id} → Get detailed result                │  │
│  │  GET  /api/scoping/download/{id} → Send Word file                   │  │
│  │  GET  /api/roles               → Get available roles                │  │
│  │  GET  /health                  → Health check                        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Process data
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SCOPING ENGINE (Python Backend)                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  backend/scoping_engine.py                                          │   │
│  │                                                                      │   │
│  │  1. ScopingEngine.process_scope()                                   │   │
│  │     ├─→ ScopeDefinitionProcessor                                    │   │
│  │     │    └─→ Calculate engagement weightage                         │   │
│  │     └─→ Determine implementation tier                               │   │
│  │                                                                      │   │
│  │  2. ScopingEngine.calculate_effort()                                │   │
│  │     └─→ EffortCalculator                                            │   │
│  │          └─→ Apply formulas from Excel                              │   │
│  │                                                                      │   │
│  │  3. ScopingEngine.calculate_fte()                                   │   │
│  │     └─→ FTEEffortsCalculator                                        │   │
│  │          └─→ Allocate hours by role                                 │   │
│  │                                                                      │   │
│  │  4. ScopingEngine.generate_report()                                 │   │
│  │     └─→ SOWReportGenerator                                          │   │
│  │          ├─→ Create JSON report                                     │   │
│  │          └─→ Generate Word document                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Save results
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA STORAGE                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  JSON Files (Per User)                                              │   │
│  │  engagement-scoping-tool/output/results/                            │   │
│  │                                                                      │   │
│  │  user_john_at_example_com.json                                      │   │
│  │  └─→ Array of submissions                                           │   │
│  │      ├─→ submission_id                                              │   │
│  │      ├─→ user_email                                                 │   │
│  │      ├─→ calculation_result                                         │   │
│  │      └─→ files (json_report, word_report)                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Word Reports                                                        │   │
│  │  engagement-scoping-tool/output/                                     │   │
│  │                                                                      │   │
│  │  scoping_result_user_email_timestamp.docx                           │   │
│  │  └─→ Professional SOW document                                      │   │
│  │      ├─→ Scope definition                                           │   │
│  │      ├─→ Tier information                                           │   │
│  │      ├─→ Effort breakdown                                           │   │
│  │      └─→ FTE allocation                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW EXAMPLE                                  │
└─────────────────────────────────────────────────────────────────────────────┘

User Input:
  {
    "scopingData": {
      "dimensions-account": { "value": "YES", "count": 0 },
      "dimensions-multiCurrency": { "value": "YES", "count": 5 }
    },
    "selectedRoles": ["PM USA", "PM India"],
    "userEmail": "john@example.com"
  }

      ↓ Transform to backend format

Backend Input:
  {
    "scope_inputs": [
      { "name": "Account", "in_scope": "YES", "details": 0 },
      { "name": "Multi Currency", "in_scope": "YES", "details": 5 }
    ],
    "selected_roles": ["PM USA", "PM India"]
  }

      ↓ Process through engine

Calculation Result:
  {
    "tier": "Tier 3 - Enhanced Scope",
    "total_weightage": 125,
    "total_hours": 2400,
    "total_days": 300,
    "total_months": 10,
    "fte_allocation": {
      "PM USA": { "hours": 800, "days": 100 },
      "PM India": { "hours": 1600, "days": 200 }
    }
  }

      ↓ Store & Return

Stored:
  - JSON: output/results/user_john_at_example_com.json
  - Word: output/scoping_result_john_at_example_com_20251204.docx

Returned to Frontend:
  - Success message
  - Submission ID
  - Calculation summary
  - File paths

User sees:
  - Success toast
  - Entry in history table
  - Download button available
```

## Key Points

1. **Frontend (Next.js)**: 
   - User interface for input and viewing results
   - Uses SSO for authentication
   - Filters history by user email

2. **API Proxy (Next.js API Routes)**:
   - Secure layer between frontend and backend
   - Handles authentication
   - Can add rate limiting/logging

3. **Backend (Python Flask)**:
   - Wraps existing scoping engine
   - Transforms data formats
   - Processes calculations
   - Generates reports

4. **Storage (JSON + Word)**:
   - One JSON file per user
   - Word reports generated on demand
   - Easy to query and display

5. **Security**:
   - SSO authentication via NextAuth
   - Users only see their own submissions
   - Email-based filtering
