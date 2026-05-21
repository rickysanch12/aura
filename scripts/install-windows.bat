@echo off
REM ALCOS Installation Script for Windows

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR:~0,-9%

echo.
echo ===================================================================
echo  ALCOS Installation for Windows
echo ===================================================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: This script should be run as Administrator for full functionality
    echo Some features (like system service installation) may not work
    echo.
)

REM Install Python dependencies
echo Installing Python dependencies...
cd /d "%PROJECT_ROOT%"
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
if errorlevel 1 (
    echo Error: Failed to upgrade pip
    exit /b 1
)

pip install -e . > nul 2>&1
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)
echo ✓ Python dependencies installed

REM Install Node dependencies
echo Installing Node.js dependencies...
cd /d "%PROJECT_ROOT%frontend"
call npm install > nul 2>&1
if errorlevel 1 (
    echo Error: Failed to install Node dependencies
    exit /b 1
)
echo ✓ Node.js dependencies installed

REM Create start menu shortcut
echo Creating Start Menu shortcut...
set SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\ALCOS.lnk

REM Use PowerShell to create the shortcut
powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; ^
     $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); ^
     $Shortcut.TargetPath = '%SCRIPT_DIR%launcher-windows.bat'; ^
     $Shortcut.WorkingDirectory = '%PROJECT_ROOT%'; ^
     $Shortcut.Description = 'ALCOS - Agentic Local Core OS'; ^
     $Shortcut.Save()" > nul 2>&1

if exist "%SHORTCUT_PATH%" (
    echo ✓ Start Menu shortcut created
) else (
    echo Warning: Could not create Start Menu shortcut
)

REM Create desktop shortcut
echo Creating Desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set DESKTOP_SHORTCUT=%DESKTOP%\ALCOS.lnk

powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; ^
     $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); ^
     $Shortcut.TargetPath = '%SCRIPT_DIR%launcher-windows.bat'; ^
     $Shortcut.WorkingDirectory = '%PROJECT_ROOT%'; ^
     $Shortcut.Description = 'ALCOS - Agentic Local Core OS'; ^
     $Shortcut.Save()" > nul 2>&1

if exist "%DESKTOP_SHORTCUT%" (
    echo ✓ Desktop shortcut created
) else (
    echo Warning: Could not create Desktop shortcut
)

REM Create startup folder entry
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ALCOS.lnk
echo Creating autostart entry...

powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; ^
     $Shortcut = $WshShell.CreateShortcut('%STARTUP%'); ^
     $Shortcut.TargetPath = '%SCRIPT_DIR%launcher-windows.bat'; ^
     $Shortcut.WorkingDirectory = '%PROJECT_ROOT%'; ^
     $Shortcut.Description = 'ALCOS - Agentic Local Core OS'; ^
     $Shortcut.Save()" > nul 2>&1

if exist "%STARTUP%" (
    echo ✓ Autostart entry created
    echo   (ALCOS will launch on next login)
) else (
    echo Warning: Could not create autostart entry
)

echo.
echo ===================================================================
echo  Installation Complete!
echo ===================================================================
echo.
echo You can now launch ALCOS from:
echo   1. Desktop shortcut (ALCOS.lnk)
echo   2. Start Menu (ALCOS)
echo   3. Command line: "%SCRIPT_DIR%launcher-windows.bat"
echo.
echo For more information, see README.md
echo.

endlocal
pause
