#!/bin/bash

# 设置 PyInstaller 参数
PYINSTALLER_ARGS="--onefile --icon=logo.png --name='即传'"

# 执行 PyInstaller
pyinstaller $PYINSTALLER_ARGS main.py

# 结束脚本
exit 0
