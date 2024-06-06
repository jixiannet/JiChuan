@echo off
setlocal

:: 设置 PyInstaller 参数
set PYINSTALLER_ARGS=--onefile --icon="logo.png" --name="即传"

:: 执行 PyInstaller
pyinstaller %PYINSTALLER_ARGS% main.py

:: 结束批处理
endlocal