# TraceVisualizationGUI
 Trace.mat File Visualization GUI


如何打包？
pyinstaller -D TVMainWindow.py

1、使用bat命令行脚本的方式进行打开时，无法进行拖拽(很有可能是超级管理员的权限导致的)；

确实如此(加了管理员启动，就不能拖拽了)：
```shell
@REM %1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
@REM cd /d "%~dp0"
```

以下代码可以直接拖拽
```shell
@echo off
start cmd /c "call C:\Users\FengZhiheng\anaconda3\Scripts\activate.bat&&call activate base&&call cd C:\Users\FengZhiheng\Documents\GitHub\TraceVisualizationGUI &&call python TVMainWindow.py"
```


2、使用pyinstaller进行打包之后，双击exe闪退（已经和GUI文件放在同一个文件路径下了）；