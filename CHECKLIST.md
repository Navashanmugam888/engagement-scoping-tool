# ✅ Integration Checklist

## Phase 1: Setup (COMPLETED ✅)

- [x] Install Python dependencies
  - [x] pandas
  - [x] openpyxl
  - [x] python-docx
  - [x] flask
  - [x] flask-cors
  - [x] requests

- [x] Create Python Flask API server
  - [x] Health check endpoint
  - [x] Roles endpoint
  - [x] Submit endpoint
  - [x] History endpoint
  - [x] Result endpoint
  - [x] Download endpoint

- [x] Update Next.js API routes
  - [x] Submit route
  - [x] History route
  - [x] Result route
  - [x] Download route (new)

- [x] Update frontend pages
  - [x] History page with download
  - [x] Better result display
  - [x] Download button

- [x] Create storage structure
  - [x] output/ directory
  - [x] output/results/ directory

- [x] Configure environment
  - [x] PYTHON_API_URL in .env
  - [x] NEXT_PUBLIC_BACKEND_API_URL in .env

- [x] Create documentation
  - [x] INTEGRATION_GUIDE.md
  - [x] SETUP_GUIDE.md
  - [x] SUMMARY.md
  - [x] ARCHITECTURE.md
  - [x] This checklist

- [x] Create helper scripts
  - [x] start-dev.ps1
  - [x] test_api.py

## Phase 2: Testing (YOUR NEXT STEPS)

### Step 1: Start the Servers

- [ ] Open PowerShell in project root
- [ ] Run: `.\start-dev.ps1`
- [ ] Verify Python API started (new window)
- [ ] Verify Next.js started (current window)

**OR manually:**

- [ ] Terminal 1: `.\.venv\Scripts\python.exe .\engagement-scoping-tool\api_server.py`
- [ ] Terminal 2: `npm run dev`

### Step 2: Test Python API

- [ ] Open browser: `http://localhost:5000/health`
- [ ] Should see: `{"status": "healthy", ...}`

**OR run test suite:**

- [ ] Run: `.\.venv\Scripts\python.exe .\engagement-scoping-tool\test_api.py`
- [ ] All tests should pass

### Step 3: Test Frontend

- [ ] Open: `http://localhost:3001`
- [ ] Login with SSO
- [ ] Navigate to FCCS Scoping: `/fccs-scoping`

### Step 4: Submit Test Scoping

- [ ] Fill out the form:
  - [ ] Select some scope items as "YES"
  - [ ] Enter counts where required
  - [ ] Select at least 2-3 roles
  - [ ] Add optional comments

- [ ] Click "Next" or "Submit"
- [ ] Verify success message appears
- [ ] Note the submission ID

### Step 5: Check History

- [ ] Navigate to: `/scoping-history`
- [ ] Verify your submission appears in table
- [ ] Check columns show:
  - [ ] Submitted date
  - [ ] Tier
  - [ ] Total hours
  - [ ] Total days
  - [ ] Status = "COMPLETED"
  - [ ] Actions (View + Download)

### Step 6: View Result

- [ ] Click "View" button on your submission
- [ ] Dialog should open showing:
  - [ ] User name
  - [ ] Submitted date
  - [ ] Tier information
  - [ ] Total weightage
  - [ ] Total hours/days/months
  - [ ] FTE allocation by role
  - [ ] Comments (if any)
  - [ ] Download button
  - [ ] Close button

### Step 7: Download Report

- [ ] Click "Download" button (either in table or dialog)
- [ ] Word document should download
- [ ] Open the .docx file
- [ ] Verify it contains:
  - [ ] Scope definition
  - [ ] Tier information
  - [ ] Effort breakdown
  - [ ] FTE allocation
  - [ ] Professional formatting

### Step 8: Verify Storage

- [ ] Open file explorer
- [ ] Navigate to: `engagement-scoping-tool\output\results\`
- [ ] Find file: `user_{your_email}.json`
- [ ] Open and verify JSON structure
- [ ] Navigate to: `engagement-scoping-tool\output\`
- [ ] Find Word file: `scoping_result_*.docx`

## Phase 3: Troubleshooting (If Issues)

### Issue: Python API won't start

**Symptoms:**
- Error message in terminal
- Can't access http://localhost:5000/health

**Solutions:**
1. [ ] Check port 5000 is not in use:
   ```powershell
   netstat -ano | findstr :5000
   ```
2. [ ] Kill process if needed:
   ```powershell
   taskkill /PID <pid> /F
   ```
3. [ ] Verify virtual environment:
   ```powershell
   .\.venv\Scripts\python.exe --version
   ```
4. [ ] Check Excel file exists:
   ```powershell
   dir "engagement-scoping-tool\Engagement Scoping Tool - FCC.xlsx"
   ```

### Issue: CORS Errors

**Symptoms:**
- Browser console shows CORS error
- Network tab shows failed requests

**Solutions:**
1. [ ] Verify Flask-CORS is installed:
   ```powershell
   .\.venv\Scripts\pip show flask-cors
   ```
2. [ ] Check `api_server.py` has:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

### Issue: File Not Found

**Symptoms:**
- 404 error when downloading
- "Report not found" message

**Solutions:**
1. [ ] Check output directories exist:
   ```powershell
   dir engagement-scoping-tool\output
   dir engagement-scoping-tool\output\results
   ```
2. [ ] Create if missing:
   ```powershell
   mkdir engagement-scoping-tool\output
   mkdir engagement-scoping-tool\output\results
   ```

### Issue: Next.js Can't Connect to Python

**Symptoms:**
- "Failed to fetch" errors
- Connection refused

**Solutions:**
1. [ ] Verify Python API is running
2. [ ] Check `.env` file has:
   ```
   PYTHON_API_URL=http://localhost:5000
   ```
3. [ ] Restart Next.js server after .env changes

### Issue: No Data in History

**Symptoms:**
- History page is empty
- No submissions showing

**Solutions:**
1. [ ] Verify you're logged in with SSO
2. [ ] Check user email matches submission email
3. [ ] Verify JSON file exists in `output/results/`
4. [ ] Check Python API logs for errors

## Phase 4: Production Deployment (Future)

- [ ] Configure production URLs in .env
- [ ] Set up database (replace JSON storage)
- [ ] Configure file storage (Azure Blob, AWS S3)
- [ ] Add monitoring and logging
- [ ] Set up CI/CD pipeline
- [ ] Configure SSL certificates
- [ ] Set up backup strategy
- [ ] Add rate limiting
- [ ] Configure authentication
- [ ] Set up error tracking

## Success Criteria

✅ **Integration is successful when:**

1. [ ] Python API starts without errors
2. [ ] Health check returns 200 OK
3. [ ] Next.js connects to Python API
4. [ ] Form submission works
5. [ ] Calculations complete successfully
6. [ ] Results appear in history
7. [ ] Word report downloads successfully
8. [ ] JSON files are created
9. [ ] User can view detailed results
10. [ ] Download button works

## Support Resources

- **Quick Start:** `SETUP_GUIDE.md`
- **Architecture:** `ARCHITECTURE.md`
- **Integration Details:** `INTEGRATION_GUIDE.md`
- **Summary:** `SUMMARY.md`

## Getting Help

If you encounter issues:

1. **Check the logs:**
   - Python API terminal
   - Next.js terminal
   - Browser console (F12)

2. **Run the test suite:**
   ```powershell
   .\.venv\Scripts\python.exe .\engagement-scoping-tool\test_api.py
   ```

3. **Verify configuration:**
   - `.env` file settings
   - Port numbers
   - File paths

4. **Review documentation:**
   - Read troubleshooting sections
   - Check API endpoint formats
   - Verify data structures

## Next Steps After Testing

Once everything works:

1. [ ] Test with multiple users
2. [ ] Test with different scope combinations
3. [ ] Verify Word report formatting
4. [ ] Test download across browsers
5. [ ] Performance testing
6. [ ] Plan database migration
7. [ ] Set up production environment
8. [ ] Train users on the system

---

**Current Status:** Setup Complete ✅  
**Next Action:** Start testing (Phase 2)  
**Last Updated:** December 4, 2025
