# Start Python Flask API and Next.js Frontend
# This script starts both servers for the scoping application

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Starting Engagement Scoping Tool     " -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Python Flask API in a new window
Write-Host "Starting Python Flask API..." -ForegroundColor Green
$pythonPath = Join-Path $scriptDir ".venv\Scripts\python.exe"
$apiPath = Join-Path $scriptDir "backend_scoping_test\api_server.py"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$pythonPath' '$apiPath'" -WindowStyle Normal

# Wait a bit for the API to start
Write-Host "Waiting for Python API to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start Next.js Frontend
Write-Host "Starting Next.js Frontend..." -ForegroundColor Green
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Services Starting...                 " -ForegroundColor Cyan
Write-Host "  - Python API: http://localhost:5000  " -ForegroundColor Yellow
Write-Host "  - Next.js App: http://localhost:3001 " -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Run Next.js in the current window
npm run dev
