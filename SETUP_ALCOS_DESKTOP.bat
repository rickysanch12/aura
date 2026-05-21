@echo off
REM ALCOS Desktop Setup Batch Wrapper
REM This file can be double-clicked to run the PowerShell setup script

setlocal enabledelayedexpansion

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

REM Change to the aura directory
cd /d "%SCRIPT_DIR%aura"

REM Run PowerShell script with proper execution policy
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%WINDOWS_DESKTOP_SETUP.ps1"

pause
