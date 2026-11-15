@echo off
title R Harshitha Portfolio - Local Server
echo ========================================================
echo   Launching R Harshitha's Modern Portfolio Server...
echo ========================================================
echo.
cd /d "%~dp0"
echo Starting server on http://localhost:8000 ...

if exist "C:\Users\harsh\AppData\Local\Programs\Python\Python314\python.exe" (
    start http://localhost:8000
    "C:\Users\harsh\AppData\Local\Programs\Python\Python314\python.exe" server.py
    goto end
)

py -3 --version >nul 2>&1
if %errorlevel% == 0 (
    start http://localhost:8000
    py -3 server.py
    goto end
)

python --version >nul 2>&1
if %errorlevel% == 0 (
    start http://localhost:8000
    python server.py
    goto end
)

echo [Error] Python executable could not be located.
:end
pause
