@echo off
title Push Harshitha Portfolio to GitHub
echo ========================================================
echo   Pushing Portfolio to https://github.com/Harshitha-cymk/Harshitha
echo ========================================================
echo.
cd /d "%~dp0"

set "GIT_CMD=C:\Users\harsh\AppData\Local\Microsoft\WinGet\Packages\Git.MinGit_Microsoft.Winget.Source_8wekyb3d8bbwe\cmd\git.exe"

echo Checking remote origin...
"%GIT_CMD%" remote set-url origin https://github.com/Harshitha-cymk/Harshitha.git

echo.
echo Attempting to push branch 'main' to GitHub...
echo.

"%GIT_CMD%" push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ----------------------------------------------------
    echo Authentication is required by GitHub.
    echo If you have a Personal Access Token (PAT), you can paste it below:
    echo (You can create one at https://github.com/settings/tokens with 'repo' scope)
    echo ----------------------------------------------------
    set /p "GITHUB_TOKEN=Paste your GitHub Personal Access Token (or press Enter to exit): "
    if defined GITHUB_TOKEN (
        "%GIT_CMD%" push https://Harshitha-cymk:%GITHUB_TOKEN%@github.com/Harshitha-cymk/Harshitha.git main
    )
)

echo.
echo ========================================================
echo Process finished.
echo ========================================================
pause
