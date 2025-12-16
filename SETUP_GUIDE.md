# 🚀 FCCS Engagement Scoping Tool - Setup & Quick Start

## 📋 Overview

This application integrates a Next.js frontend with a Python Flask backend to provide automated FCCS implementation scoping and effort estimation.

## ✅ Prerequisites

- **Python 3.12+** (already installed in `.venv`)
- **Node.js 18+** 
- **npm** or **yarn**

## 🔧 Installation

All dependencies are already installed! But if you need to reinstall:

### Python Dependencies

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install Python packages
pip install -r engagement-scoping-tool\requirements.txt
```

### Node.js Dependencies

```powershell
npm install
```

## 🏃 Running the Application

### Option 1: Quick Start (Recommended)

Use the PowerShell script to start both servers:

```powershell
.\start-dev.ps1
```

This will:
1. ✅ Start Python Flask API on `http://localhost:5000` (new window)
2. ✅ Start Next.js frontend on `http://localhost:3001` (current window)

### Option 2: Manual Start

**Terminal 1 - Python API:**

```powershell
.\.venv\Scripts\python.exe .\engagement-scoping-tool\api_server.py
```

**Terminal 2 - Next.js Frontend:**

```powershell
npm run dev
```

## 🧪 Testing the Integration

### 1. Test Python API

```powershell
# Health check
curl http://localhost:5000/health

# Or run the test script
.\.venv\Scripts\python.exe .\engagement-scoping-tool\test_api.py
```

### 2. Test Frontend

1. Open browser: `http://localhost:3001`
2. Login with SSO
3. Navigate to FCCS Scoping: `http://localhost:3001/fccs-scoping`
4. Fill out form and submit
5. Check results in History: `http://localhost:3001/scoping-history`
6. Download Word report

## 📁 Project Structure

```
admin-scoping-app/
├── app/                          # Next.js application
│   ├── (app)/
│   │   ├── fccs-scoping/        # Scoping input form
│   │   │   ├── page.jsx         # Main scoping page
│   │   │   └── scopingData.js   # Scope definitions
│   │   └── scoping-history/     # History & results
│   │       └── page.jsx         # History page
│   └── api/
│       └── scoping/
│           ├── submit/          # Submit scoping data
│           ├── history/         # Get user history
│           ├── result/[id]/     # Get detailed result
│           └── download/[id]/   # Download report
│
├── engagement-scoping-tool/     # Python backend
│   ├── backend/
│   │   ├── core/               # Core calculation engines
│   │   │   ├── scope_processor.py
│   │   │   ├── effort_calculator.py
│   │   │   ├── fte_calculator.py
│   │   │   └── sow_report_generator.py
│   │   ├── data/               # Formula templates
│   │   └── utils/              # Utilities
│   ├── output/                 # Generated reports
│   │   └── results/           # User results (JSON)
│   ├── api_server.py          # Flask API server
│   ├── test_api.py            # API test suite
│   └── requirements.txt       # Python dependencies
│
├── .env                        # Environment configuration
├── start-dev.ps1              # Quick start script
├── INTEGRATION_GUIDE.md       # Detailed integration docs
└── package.json               # Node.js dependencies
```

## 🔄 Data Flow

```
User Input → Frontend (React)
    ↓
Next.js API Routes (Proxy)
    ↓
Python Flask API
    ↓
Scoping Engine (Calculations)
    ↓
JSON Storage + Word Report
    ↓
Return Results → Frontend Display
```

## 🔌 API Endpoints

### Python Flask API (Port 5000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/roles` | Get available roles |
| POST | `/api/scoping/submit` | Submit scoping data |
| GET | `/api/scoping/history` | Get user submissions |
| GET | `/api/scoping/result/{id}` | Get detailed result |
| GET | `/api/scoping/download/{id}` | Download Word report |

### Next.js API Routes (Port 3001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/scoping/submit` | Proxy to Python API |
| GET | `/api/scoping/history` | Proxy to Python API |
| GET | `/api/scoping/result/[id]` | Proxy to Python API |
| GET | `/api/scoping/download/[id]` | Proxy download |

## 💾 Data Storage

Results are stored in JSON files per user:

**Location:** `engagement-scoping-tool/output/results/user_{email}.json`

**Format:**
```json
[
  {
    "submission_id": "user_email_timestamp",
    "user_email": "user@example.com",
    "user_name": "John Doe",
    "submitted_at": "2025-12-04T14:30:00Z",
    "status": "COMPLETED",
    "calculation_result": {
      "tier": "Tier 3 - Enhanced Scope",
      "total_weightage": 125,
      "total_hours": 2400,
      "total_days": 300,
      "total_months": 10
    },
    "files": {
      "json_report": "output/report.json",
      "word_report": "output/report.docx"
    }
  }
]
```

## 🎯 Features

### ✅ Implemented

- [x] Frontend scoping form with dynamic fields
- [x] Role selection
- [x] Backend calculation engine
- [x] Formula processing
- [x] Effort estimation
- [x] FTE allocation by role
- [x] Word report generation
- [x] JSON result storage per user
- [x] History page with filtering by user email (SSO)
- [x] Download functionality for reports
- [x] Result viewing

### 🔜 Future Enhancements

- [ ] Database integration (PostgreSQL)
- [ ] Async processing with queue
- [ ] Real-time status updates via WebSocket
- [ ] Excel file upload for bulk input
- [ ] PDF export option
- [ ] Comparison between submissions
- [ ] Admin dashboard
- [ ] Audit logging

## 🐛 Troubleshooting

### Python API Won't Start

**Error:** Port 5000 already in use

**Solution:**
```powershell
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Next.js Build Errors

**Error:** Module not found

**Solution:**
```powershell
# Clean install
Remove-Item -Recurse -Force node_modules
npm install
```

### CORS Errors

**Error:** Access blocked by CORS policy

**Solution:** Verify Flask-CORS is enabled in `api_server.py`:
```python
from flask_cors import CORS
CORS(app)
```

### File Not Found

**Error:** Word report not found

**Solution:** Ensure output directories exist:
```powershell
mkdir engagement-scoping-tool\output
mkdir engagement-scoping-tool\output\results
```

## 🔐 Environment Variables

Edit `.env` file:

```env
# Python Flask API
PYTHON_API_URL=http://localhost:5000

# For client-side fetch
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:5000

# NextAuth
NEXTAUTH_URL=http://localhost:3001
NEXTAUTH_SECRET=your-secret-here

# Azure AD (for SSO)
AZURE_AD_CLIENT_ID=your-client-id
AZURE_AD_CLIENT_SECRET=your-client-secret
AZURE_AD_TENANT_ID=your-tenant-id
```

## 📚 Documentation

- **Integration Guide:** See `INTEGRATION_GUIDE.md` for detailed architecture
- **Backend Integration:** See `BACKEND_INTEGRATION.md` for original specs
- **API Testing:** Run `test_api.py` for endpoint verification

## 🛠️ Development Workflow

1. **Make Changes** to frontend or backend
2. **Test Locally** using `start-dev.ps1`
3. **Verify** using test scripts
4. **Commit** changes to git
5. **Deploy** to production environment

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review `INTEGRATION_GUIDE.md`
3. Run the test suite: `python engagement-scoping-tool/test_api.py`
4. Contact the development team

## 📄 License

Internal use only - Donyati Technologies

---

**Last Updated:** December 4, 2025
**Version:** 1.0.0
