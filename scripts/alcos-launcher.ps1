# ALCOS Quick Launcher for Windows PowerShell

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "  ALCOS - Agentic Local Core OS" -ForegroundColor Cyan
Write-Host "  Elite Local Autonomous AI System" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

$issues = 0

$pythonCheck = $null
try {
    $pythonCheck = python --version 2>&1
    Write-Host "[OK] Python found: $pythonCheck" -ForegroundColor Green
} catch {
    Write-Host "[X] Python not found" -ForegroundColor Red
    Write-Host "  Install from: https://www.python.org/downloads/" -ForegroundColor Red
    $issues++
}

$nodeCheck = $null
try {
    $nodeCheck = node --version 2>&1
    Write-Host "[OK] Node.js found: $nodeCheck" -ForegroundColor Green
} catch {
    Write-Host "[X] Node.js not found" -ForegroundColor Red
    Write-Host "  Install from: https://nodejs.org" -ForegroundColor Red
    $issues++
}

if ($issues -gt 0) {
    Write-Host ""
    Write-Host "Please install missing prerequisites and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Setup environment
Write-Host "Setting up environment..." -ForegroundColor Yellow

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Install Python dependencies
if (Test-Path "setup.py") {
    Write-Host "Installing Python dependencies..."
    pip install -e . 2>&1 | Out-Null
}

# Install Node dependencies if needed
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "Installing Node dependencies..."
    Push-Location frontend
    npm install 2>&1 | Out-Null
    Pop-Location
}

Write-Host "Environment ready" -ForegroundColor Green
Write-Host ""

# Start backend
Write-Host "Starting backend..." -ForegroundColor Yellow
$backendProcess = Start-Process python -ArgumentList "-m alcos.api.server" `
    -RedirectStandardOutput "logs\backend.log" `
    -RedirectStandardError "logs\backend.log" `
    -PassThru `
    -WindowStyle Hidden

Start-Sleep -Seconds 3
Write-Host "[OK] Backend starting (PID: $($backendProcess.Id))" -ForegroundColor Green

# Start frontend
Write-Host "Starting frontend..." -ForegroundColor Yellow
Push-Location frontend
Start-Process npm -ArgumentList "run electron-dev"
Pop-Location

Write-Host ""
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "  ALCOS is starting!" -ForegroundColor Cyan
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "  Backend: http://localhost:8000" -ForegroundColor Green
Write-Host "  Frontend: Electron window" -ForegroundColor Green
Write-Host ""
Write-Host "  Logs: logs\backend.log"
Write-Host "  To stop: Close the windows or press Ctrl+C"
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to keep this window open"
