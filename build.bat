@echo off
setlocal

:: ���� PyInstaller ����
set PYINSTALLER_ARGS=--onefile --icon="logo.png" --name="����"

:: ִ�� PyInstaller
pyinstaller %PYINSTALLER_ARGS% main.py

:: ����������
endlocal