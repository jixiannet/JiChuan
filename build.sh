#!/bin/bash

# ���� PyInstaller ����
PYINSTALLER_ARGS="--onefile --icon=logo.png --name='����'"

# ִ�� PyInstaller
pyinstaller $PYINSTALLER_ARGS main.py

# �����ű�
exit 0
