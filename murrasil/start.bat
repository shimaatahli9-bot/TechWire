@echo off
chcp 65001 >nul 2>&1
title Murrasil - Running

echo.
echo ========================================
echo      Murrasil - Starting Server
echo ========================================
echo.

:: Check venv exists
if not exist "venv" (
    echo [ERROR] Setup not done yet. Run setup.bat first
    pause
    exit /b 1
)

:: Check .env exists
if not exist ".env" (
    echo [ERROR] .env file not found. Run setup.bat first
    pause
    exit /b 1
)

:: Activate venv
call venv\Scripts\activate.bat

:: Read PORT from .env (default 8000)
set PORT=8000
for /f "tokens=2 delims==" %%a in ('findstr "PORT" .env 2^>nul') do set PORT=%%a

echo [INFO] Starting server on port %PORT%...
echo [INFO] Browser will open automatically in a few seconds...
echo.
echo [Press Ctrl+C to stop]
echo.

:: Open browser after 3 seconds delay (in background)
start /b cmd /c "timeout /t 3 /nobreak >nul 2>&1 && start http://127.0.0.1:%PORT%"

:: Start FastAPI server
python main.py

pause
