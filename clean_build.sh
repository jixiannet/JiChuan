@echo off
setlocal

:: ɾ������.spec �ļ�
if exist "����.spec" del "����.spec"

:: ɾ�� build Ŀ¼
if exist "build" rmdir /s /q "build"

:: ɾ�� dist Ŀ¼
if exist "dist" rmdir /s /q "dist"

:: ����������
endlocal