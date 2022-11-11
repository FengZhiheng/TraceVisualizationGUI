@echo off

@REM %1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
@REM cd /d "%~dp0"

start cmd /c "call C:\Users\FengZhiheng\anaconda3\Scripts\activate.bat&&call activate base&&call cd C:\Users\FengZhiheng\Documents\GitHub\TraceVisualizationGUI &&call python TVMainWindow.py"