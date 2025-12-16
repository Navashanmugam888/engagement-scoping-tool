# PowerShell script to start the new backend (backend_scoping_test)
Write-Host "Starting Backend Scoping Server..." -ForegroundColor Green

# Navigate to backend directory
Set-Location -Path "backend_scoping_test"

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Please create one first:" -ForegroundColor Red
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Check if requirements are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
python -c "import flask, flask_cors" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start the Flask server
Write-Host "`nStarting Flask API Server on port 5000..." -ForegroundColor Green
Write-Host "Backend URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

python api_server.py
