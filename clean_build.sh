@echo off
setlocal

:: 删除即传.spec 文件
if exist "即传.spec" del "即传.spec"

:: 删除 build 目录
if exist "build" rmdir /s /q "build"

:: 删除 dist 目录
if exist "dist" rmdir /s /q "dist"

:: 结束批处理
endlocal