# Troubleshooting Guide

## Common Issues and Solutions

### 1. Permission Denied Error When Submitting Scoping Data

**Error Message:**
```
PermissionError: [Errno 13] Permission denied: 'Engagement Scoping Tool - FCC.xlsx'
```

**Cause:** The Excel template file is currently open in Microsoft Excel or another application.

**Solution:**
1. Close the file `Engagement Scoping Tool - FCC.xlsx` in Excel
2. Make sure no other application has the file open
3. Try your submission again

**Why this happens:** Python needs to read the Excel file to process your scoping data. When Excel has the file open, it locks the file and prevents other applications from accessing it.

---

### 2. Field Mapping Warnings

**Warning Message:**
```
Warning: No mapping found for 'field_name', using fallback: 'Field Name'
```

**Cause:** The frontend is using a field ID that doesn't have a mapping in the backend.

**Solution:** This has been fixed by adding alternative frontend IDs to the mapping dictionary. If you still see warnings:
1. Restart the Python backend server
2. Clear your browser cache
3. Try submitting again

**Note:** These warnings don't prevent the calculation from working, but having proper mappings ensures data accuracy.

---

### 3. Backend Not Responding

**Symptoms:**
- Frontend shows "Failed to submit scope"
- Connection timeout errors
- API calls fail with network errors

**Solution:**
1. Check if the Python backend is running:
   ```powershell
   cd "engagement-scoping-tool"
   python api_server.py
   ```
2. Verify the backend is accessible at `http://localhost:5000`
3. Check the console for error messages
4. Make sure port 5000 is not being used by another application

---

### 4. Form Data Lost When Switching Tabs

**Issue:** Previously, form data would be lost when switching browser tabs.

**Solution:** ✅ FIXED - Form data is now automatically saved to browser sessionStorage and restored when you return to the page.

**Note:** Data persists only in the current browser session. If you close the browser completely, you'll need to start fresh.

---

### 5. Input Field Not Auto-Focusing

**Issue:** Previously, you had to manually click the input field after selecting "YES".

**Solution:** ✅ FIXED - Input fields now automatically receive focus when you select "YES" on items that have count fields.

---

### 6. Calculation Results Mismatch

**Issue:** Frontend showing different results than backend test.

**Common Causes:**
1. **Different input data** - Make sure you're entering the exact same values in both tests
2. **Old cached data** - Clear browser cache and sessionStorage
3. **Backend not restarted** - Restart Python backend after code changes

**How to verify:**
1. Run backend test: `python test_ui.py`
2. Note the weightage and tier from backend
3. Submit through frontend with SAME inputs
4. Compare results - they should match!

**Debug tip:** Check the backend console logs to see what data is being received from frontend.

---

## Starting the Application

### Backend (Python API)
```powershell
cd "c:\Users\DhakshnamoorthiTamil\OneDrive - Donyati\mastero ai\admin-scoping-app\engagement-scoping-tool"
python api_server.py
```

**Expected output:**
```
* Running on http://127.0.0.1:5000
* Loaded X formulas
* Loaded Y metrics
```

### Frontend (Next.js)
```powershell
cd "c:\Users\DhakshnamoorthiTamil\OneDrive - Donyati\mastero ai\admin-scoping-app"
npm run dev
```

**Expected output:**
```
ready - started server on 0.0.0.0:3000
```

---

## Important Files

### Excel Template
**Location:** `engagement-scoping-tool/Engagement Scoping Tool - FCC.xlsx`
**Purpose:** Contains formulas and weightage calculations
**Warning:** ⚠️ Must be CLOSED when running the application!

### User Results Storage
**Location:** `engagement-scoping-tool/output/results/user_{email}.json`
**Purpose:** Stores all submission history for each user

### Generated Reports
**Location:** `engagement-scoping-tool/output/`
**Files:** 
- `scoping_result_{user}_{timestamp}.json` - JSON report
- `scoping_result_{user}_{timestamp}.docx` - Word report

---

## Getting Help

If you encounter an issue not covered here:

1. Check the backend console for error messages
2. Check the browser console (F12) for frontend errors
3. Review the error logs in the terminal
4. Verify all dependencies are installed:
   ```powershell
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   npm install
   ```

---

## Quick Fixes Checklist

Before submitting a scoping request:
- [ ] Backend server is running
- [ ] Excel file is closed
- [ ] Browser is on `http://localhost:3000`
- [ ] You're logged in with valid credentials
- [ ] At least one role is selected
- [ ] At least one scope item is marked as "YES"

---

Last Updated: December 5, 2025
