@echo off
REM ALCOS Quick Launcher for Windows

setlocal enabledelayedexpansion

cd /d "%~dp0.."
set PROJECT_ROOT=%cd%

echo.
echo ===================================================================
echo   ALCOS - Agentic Local Core OS
echo   Elite Local Autonomous AI System
echo ===================================================================
echo.

REM Check prerequisites
echo Checking prerequisites...
set /a issues=0

where python >/dev/null 2>&1
if errorlevel 1 (
    echo [X] Python not found
    echo   Install from: https://www.python.org/downloads/
    set /a issues=!issues!+1
) else (
    echo [OK] Python found
)

where node >/dev/null 2>&1
if errorlevel 1 (
    echo [X] Node.js not found
    echo   Install from: https://nodejs.org
    set /a issues=!issues!+1
) else (
    echo [OK] Node.js found
)

if !issues! gtr 0 (
    echo.
    echo Please install missing prerequisites and try again.
    pause
    exit /b 1
)
echo.

REM Setup environment
echo Setting up environment...

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Install Python dependencies
if exist "setup.py" (
    echo Installing Python dependencies...
    pip install -e . >/dev/null 2>&1
    if errorlevel 1 (
        echo Failed to install Python dependencies
        pause
        exit /b 1
    )
)

REM Install Node dependencies if needed
if not exist "frontend\node_modules" (
    echo Installing Node dependencies...
    cd frontend
    call npm install >/dev/null 2>&1
    if errorlevel 1 (
        echo Failed to install Node dependencies
        cd ..
        pause
        exit /b 1
    )
    cd ..
)

echo Environment ready
echo.

REM Start backend
echo Starting backend...
cd "%PROJECT_ROOT%"
start "ALCOS Backend" python -m alcos.api.server > logs\backend.log 2>&1
timeout /t 3 /nobreak

echo Backend starting (check logs\backend.log for details)

REM Start frontend
echo Starting frontend...
cd "%PROJECT_ROOT%\frontend"
start "ALCOS Frontend" cmd /k npm run electron-dev

echo.
echo ===================================================================
echo   ALCOS is starting!
echo ===================================================================
echo   Backend: http://localhost:8000
echo   Frontend: Electron window
echo.
echo   Logs: logs\backend.log
echo   To stop: Close the windows or press Ctrl+C
echo ===================================================================
echo.

pause
