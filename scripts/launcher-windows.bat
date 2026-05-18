@echo off
REM ALCOS Desktop Launcher for Windows

setlocal enabledelayedexpansion

REM Get the directory of this script
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR:~0,-9%

echo.
echo ===================================================================
echo  ALCOS - Agentic Local Core OS Launcher
echo ===================================================================
echo.

REM Check if virtual environment exists
if not exist "%PROJECT_ROOT%venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run install.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call "%PROJECT_ROOT%venv\Scripts\activate.bat"

REM Check if Node is available
where /q node
if errorlevel 1 (
    echo Warning: Node.js not found in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo Starting ALCOS system...
echo.

REM Start backend in a new window
echo Starting backend server...
start "ALCOS Backend" cmd /k "cd /d "%PROJECT_ROOT%" && python -m alcos.api.server"

REM Wait a bit for backend to start
timeout /t 3 /nobreak

REM Start frontend in a new window
echo Starting frontend...
cd /d "%PROJECT_ROOT%frontend"
start "ALCOS Frontend" cmd /k "npm run electron-dev"

echo.
echo ===================================================================
echo  ALCOS Started!
echo  Backend: http://localhost:8000
echo  Frontend: Electron window should open automatically
echo ===================================================================
echo.

endlocal
pause
