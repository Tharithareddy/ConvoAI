@echo off
echo ConvoAI Web UI Setup
echo ====================

echo.
echo Setting up the ConvoAI Web Interface...
echo This will install dependencies and start both backend and frontend servers.
echo.

echo Step 1: Installing Python dependencies for backend...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies!
    echo Please make sure Python and pip are installed.
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Node.js dependencies for frontend...
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install Node.js dependencies!
    echo Please make sure Node.js and npm are installed.
    echo Download from: https://nodejs.org
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To start ConvoAI Web UI:
echo   1. Run 'start_backend.bat' in one terminal
echo   2. Run 'start_frontend.bat' in another terminal
echo   3. Open http://localhost:3000 in your browser
echo.
pause