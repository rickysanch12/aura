# ALCOS Windows Setup Guide

## Prerequisites

Before launching ALCOS on Windows, ensure you have:

1. **Python 3.10+** - [Download from python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Node.js** - [Download from nodejs.org](https://nodejs.org/)
   - Includes npm package manager

## Quick Start

### Option 1: Batch File Launcher (Simple)

1. **Create Desktop Shortcut:**
   - Right-click on your desktop
   - Select "New" → "Shortcut"
   - Enter the target path: `cmd.exe /k "C:\path\to\aura\scripts\alcos-launcher.bat"`
   - Replace `C:\path\to\aura` with your actual ALCOS installation path
   - Name it "ALCOS"
   - Click Finish

2. **Run ALCOS:**
   - Double-click the "ALCOS" shortcut on your desktop
   - The launcher will check prerequisites, set up environment, and start the application

### Option 2: PowerShell Launcher (Advanced)

1. **Enable PowerShell Script Execution:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Create Desktop Shortcut:**
   - Right-click on your desktop
   - Select "New" → "Shortcut"
   - Enter: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\path\to\aura\scripts\alcos-launcher.ps1"`
   - Replace `C:\path\to\aura` with your actual ALCOS installation path
   - Name it "ALCOS PowerShell"
   - Click Finish

3. **Run ALCOS:**
   - Double-click the shortcut to launch

### Option 3: Manual Launch

Open Command Prompt and navigate to your ALCOS folder:
```batch
cd path\to\aura
scripts\alcos-launcher.bat
```

## What the Launcher Does

The launcher automatically:
- ✓ Checks Python and Node.js installation
- ✓ Creates Python virtual environment (if needed)
- ✓ Installs Python dependencies from setup.py
- ✓ Installs Node.js dependencies for frontend
- ✓ Starts the FastAPI backend server
- ✓ Launches the Electron desktop application

## Accessing ALCOS

Once running:
- **Frontend:** Electron window opens automatically
- **Backend API:** Available at http://localhost:8000
- **Logs:** Check `logs\backend.log` for backend details

## Troubleshooting

### Python not found
- Ensure Python is installed and added to PATH
- Restart Command Prompt after installing Python

### Node.js not found
- Install Node.js from nodejs.org
- Ensure npm is in your PATH

### Port already in use (8000)
- Another application is using port 8000
- Change the port in `alcos/config.yaml`

### Virtual environment issues
- Delete the `venv` folder and re-run the launcher
- It will recreate the virtual environment

## Code Submissions

Agents in ALCOS can submit code for your review:

1. **View Code Submissions:** http://localhost:8000/code/submissions
2. **Execute Submitted Code:** Use the API endpoint or frontend interface
3. **Clear History:** Clear submissions when done reviewing

## Building for Distribution

To create a standalone executable:

```batch
cd frontend
npm run electron-build
```

This creates installers in the `dist` folder for Windows.

## Support

For issues or questions:
1. Check `logs\backend.log` for error details
2. Verify all prerequisites are installed
3. Ensure ports 8000 and 5173 are available
