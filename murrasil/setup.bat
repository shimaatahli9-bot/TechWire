@echo off
chcp 65001 >nul 2>&1
title Murrasil - Setup

echo.
echo ========================================
echo      Murrasil - Project Setup
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo [INFO] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found

:: Create virtual environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

:: Activate and install dependencies
echo [INFO] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
echo [OK] All dependencies installed

:: Create .env from .env.example if not exists
if not exist ".env" (
    copy .env.example .env >nul
    echo.
    echo ================================================
    echo  [!] .env file created
    echo  [!] Open it and paste your Gemini API key
    echo  [!] Get your key from:
    echo      https://aistudio.google.com/app/apikey
    echo ================================================
    echo.
    pause
    start notepad .env
) else (
    echo [OK] .env file already exists
)

echo.
echo [OK] Setup complete! Now run start.bat
echo.
pause
