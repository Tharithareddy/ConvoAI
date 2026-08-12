@echo off
echo ConvoAI Launcher
echo ===============

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found! Starting ConvoAI...
echo.

python main.py

echo.
echo ConvoAI session ended.
pause