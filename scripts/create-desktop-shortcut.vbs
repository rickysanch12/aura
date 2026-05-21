' VBScript to create desktop shortcut for ALCOS
' Run from Command Prompt: cscript scripts\create-desktop-shortcut.vbs

Set objShell = CreateObject("WScript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(strPath)

Set objLink = objShell.CreateShortcut(strDesktop & "\ALCOS.lnk")
objLink.TargetPath = "cmd.exe"
objLink.Arguments = "/k """ & strPath & "\scripts\alcos-launcher.bat"""
objLink.WorkingDirectory = strPath
objLink.Description = "Agentic Local Core OS - Elite local autonomous AI system"
objLink.IconLocation = strPath & "\frontend\assets\icon.png,0"
objLink.Save

WScript.Echo "Desktop shortcut created successfully!"
WScript.Echo "Look for 'ALCOS' on your desktop."
