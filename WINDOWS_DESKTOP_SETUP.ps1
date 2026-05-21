# ALCOS Windows Desktop Setup
# This script automatically creates a desktop shortcut to launch ALCOS

param(
    [string]$AuraPath = (Split-Path -Parent $PSScriptRoot)
)

$DesktopPath = [System.IO.Path]::Combine(
    [Environment]::GetFolderPath("Desktop")
)

$LauncherPath = Join-Path $AuraPath "scripts" "alcos-launcher.bat"
$ShortcutPath = Join-Path $DesktopPath "ALCOS.lnk"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "ALCOS Desktop Launcher Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Verify launcher exists
if (-not (Test-Path $LauncherPath)) {
    Write-Host "ERROR: Launcher not found at $LauncherPath" -ForegroundColor Red
    Write-Host "Please ensure alcos-launcher.bat exists in the scripts directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "Launcher path: $LauncherPath" -ForegroundColor Green
Write-Host "Desktop path: $DesktopPath" -ForegroundColor Green
Write-Host ""

# Create shortcut using WScript
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $LauncherPath
$Shortcut.WorkingDirectory = $AuraPath
$Shortcut.Description = "Launch Agentic Local Core OS (ALCOS)"
$Shortcut.IconLocation = "system-run.exe,0"
$Shortcut.WindowStyle = 1  # Normal window
$Shortcut.Save()

Write-Host "✓ Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "  Location: $ShortcutPath" -ForegroundColor Green
Write-Host ""
Write-Host "You can now launch ALCOS by double-clicking the 'ALCOS' icon on your desktop" -ForegroundColor Yellow
Write-Host ""
Write-Host "First launch will:" -ForegroundColor Cyan
Write-Host "  1. Check Python 3.10+ installation" -ForegroundColor Cyan
Write-Host "  2. Check Node.js installation" -ForegroundColor Cyan
Write-Host "  3. Create virtual environment" -ForegroundColor Cyan
Write-Host "  4. Install dependencies" -ForegroundColor Cyan
Write-Host "  5. Start backend server and frontend" -ForegroundColor Cyan
Write-Host ""
