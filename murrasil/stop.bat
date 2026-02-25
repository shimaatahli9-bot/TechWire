@echo off
chcp 65001 >nul 2>&1
title Murrasil - Stop

echo [INFO] Stopping server...
taskkill /f /im python.exe >nul 2>&1
echo [OK] Murrasil stopped
timeout /t 2 /nobreak >nul
