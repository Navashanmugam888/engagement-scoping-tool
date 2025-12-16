# Frontend-Backend Integration Guide

## Overview

This document explains how the Next.js frontend connects with the Python Flask backend for the FCCS Engagement Scoping Tool.

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────────┐
│  Next.js        │         │  Next.js API     │         │  Python Flask API   │
│  Frontend       │────────▶│  Routes          │────────▶│  (Port 5000)        │
│  (Port 3001)    │         │  (Proxy Layer)   │         │                     │
└─────────────────┘         └──────────────────┘         └─────────────────────┘
                                                                    │
                                                                    ▼
                                                          ┌─────────────────────┐
                                                          │  Scoping Engine     │
                                                          │  (Python Backend)   │
                                                          │  - Formulas         │
                                                          │  - Calculations     │
                                                          │  - Report Gen       │
                                                          └─────────────────────┘
                                                                    │
                                                                    ▼
                                                          ┌─────────────────────┐
                                                          │  JSON Storage       │
                                                          │  (User Results)     │
                                                          └─────────────────────┘
```

## Components

### 1. Python Flask API (`engagement-scoping-tool/api_server.py`)

**Purpose**: Wraps the Python scoping engine and provides REST API endpoints

**Endpoints**:

- `GET /health` - Health check
- `GET /api/roles` - Get available roles
- `POST /api/scoping/submit` - Process scoping submission
- `GET /api/scoping/history?email={email}` - Get user submission history
- `GET /api/scoping/result/{submission_id}` - Get detailed result
- `GET /api/scoping/download/{submission_id}` - Download Word report

**Features**:
- Transforms frontend data format to backend format
- Processes scope inputs through the scoping engine
- Stores results in JSON files (per user)
- Generates Word reports
- Handles CORS for Next.js communication

### 2. Next.js API Routes (Proxy Layer)

**Purpose**: Acts as a secure proxy between frontend and Python backend

**Routes**:

- `/api/scoping/submit` - Forwards submission to Python API
- `/api/scoping/history` - Fetches history from Python API
- `/api/scoping/result/[id]` - Gets detailed result from Python API
- `/api/scoping/download/[id]` - Proxies download request to Python API

**Benefits**:
- Centralizes API configuration
- Adds authentication/authorization layer
- Handles errors gracefully
- Can add rate limiting/logging

### 3. Frontend Pages

**FCCS Scoping Page** (`app/(app)/fccs-scoping/page.jsx`):
- User inputs scope items
- Selects roles
- Submits to backend via `/api/scoping/submit`

**Scoping History Page** (`app/(app)/scoping-history/page.jsx`):
- Displays user's submission history
- Shows calculation results
- Downloads Word reports
- Filters by user email (SSO)

## Data Flow

### Submission Flow

1. **User Input**: User fills out scoping form and selects roles
2. **Frontend Validation**: Next.js validates input
3. **API Call**: Frontend calls `/api/scoping/submit` with:
   ```json
   {
     "userEmail": "user@example.com",
     "userName": "John Doe",
     "scopingData": {
       "dimensions-account": { "value": "YES", "count": 0 },
       "dimensions-multiCurrency": { "value": "YES", "count": 5 }
     },
     "selectedRoles": ["PM USA", "PM India"],
     "comments": "Optional comments"
   }
   ```
4. **Next.js Proxy**: Forwards to Python Flask API
5. **Python Processing**:
   - Transforms data format
   - Runs scoping engine calculations
   - Generates reports
   - Saves to JSON file
6. **Response**: Returns calculation results
7. **Frontend Display**: Shows success message with results

### History Flow

1. **User Opens History**: Frontend calls `/api/scoping/history?email={userEmail}`
2. **Next.js Proxy**: Forwards to Python Flask API
3. **Python Retrieval**: Loads user's JSON file
4. **Response**: Returns list of submissions
5. **Frontend Display**: Shows table with results

### Download Flow

1. **User Clicks Download**: Frontend calls `/api/scoping/download/{submissionId}`
2. **Next.js Proxy**: Forwards to Python Flask API
3. **Python Lookup**: Finds Word report file path from JSON
4. **File Transfer**: Streams file through proxy
5. **Browser Download**: User downloads the .docx file

## Storage Structure

### JSON Files Location

```
engagement-scoping-tool/
  output/
    results/
      user_john_at_example_com.json  # One file per user
```

### JSON File Format

```json
[
  {
    "submission_id": "john_at_example_com_20251204_143025",
    "user_email": "john@example.com",
    "user_name": "John Doe",
    "submitted_at": "2025-12-04T14:30:25Z",
    "comments": "Initial scoping",
    "status": "COMPLETED",
    "scoping_data": { ... },
    "selected_roles": ["PM USA", "PM India"],
    "calculation_result": {
      "tier": "Tier 3 - Enhanced Scope",
      "total_weightage": 125,
      "total_hours": 2400,
      "total_days": 300,
      "total_months": 10,
      "fte_allocation": {
        "by_role": {
          "PM USA": { "hours": 800, "days": 100, "months": 3.33 },
          "PM India": { "hours": 1600, "days": 200, "months": 6.67 }
        }
      }
    },
    "files": {
      "json_report": "output/scoping_result_john_at_example_com_20251204_143025.json",
      "word_report": "output/scoping_result_john_at_example_com_20251204_143025.docx"
    }
  }
]
```

## Configuration

### Environment Variables

**`.env` file**:

```env
# Python Flask API URL
PYTHON_API_URL=http://localhost:5000

# For client-side access
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:5000
```

### Python Dependencies

**`engagement-scoping-tool/requirements.txt`**:

```
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=1.0.0
flask>=3.0.0
flask-cors>=4.0.0
```

## Running the Application

### Option 1: Using PowerShell Script (Recommended)

```powershell
.\start-dev.ps1
```

This will:
1. Start Python Flask API (port 5000) in a new window
2. Start Next.js frontend (port 3001) in the current window

### Option 2: Manual Start

**Terminal 1 - Python API**:
```powershell
cd "C:\Users\DhakshnamoorthiTamil\OneDrive - Donyati\mastero ai\admin-scoping-app"
.\.venv\Scripts\python.exe .\engagement-scoping-tool\api_server.py
```

**Terminal 2 - Next.js**:
```powershell
cd "C:\Users\DhakshnamoorthiTamil\OneDrive - Donyati\mastero ai\admin-scoping-app"
npm run dev
```

## Testing the Integration

### 1. Test Python API

Visit: `http://localhost:5000/health`

Expected response:
```json
{
  "status": "healthy",
  "service": "Engagement Scoping API",
  "timestamp": "2025-12-04T..."
}
```

### 2. Test Frontend Connection

1. Navigate to: `http://localhost:3001/fccs-scoping`
2. Fill out the scoping form
3. Select roles
4. Submit
5. Check history page: `http://localhost:3001/scoping-history`
6. Download the report

## SSO Integration

The system uses NextAuth for SSO. User information is automatically captured:

```javascript
const { data: session } = useSession();
// Access user info
session.user.email  // Used for history filtering
session.user.name   // Displayed in results
```

## Troubleshooting

### Python API Not Starting

**Issue**: Port 5000 already in use

**Solution**:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000
# Kill the process
taskkill /PID <process_id> /F
```

### CORS Errors

**Issue**: Frontend can't connect to Python API

**Solution**: Verify Flask-CORS is enabled in `api_server.py`:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # This line enables CORS
```

### File Not Found Errors

**Issue**: Word reports not found

**Solution**: Check that `output` directory exists:
```powershell
cd engagement-scoping-tool
mkdir output
mkdir output\results
```

### Environment Variables Not Loading

**Issue**: Python API URL not configured

**Solution**:
1. Verify `.env` file exists
2. Check variable names match exactly
3. Restart Next.js server after changes

## Future Enhancements

1. **Database Integration**: Replace JSON files with PostgreSQL
2. **Async Processing**: Queue long-running calculations
3. **WebSocket Updates**: Real-time status updates
4. **Excel Upload**: Import scope data from Excel
5. **Result Comparison**: Compare multiple submissions
6. **Admin Dashboard**: View all submissions across users
7. **Export Options**: PDF, Excel formats
8. **Audit Logging**: Track all changes

## API Error Handling

All APIs return consistent error format:

```json
{
  "success": false,
  "error": "Error message here",
  "details": "Stack trace (only in dev mode)"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

## Security Considerations

1. **Authentication**: All API routes check user session
2. **Authorization**: Users can only access their own data
3. **Input Validation**: Backend validates all inputs
4. **File Access**: Download API validates file ownership
5. **CORS**: Restricted to localhost in development

## Contact

For questions or issues, contact the development team.
