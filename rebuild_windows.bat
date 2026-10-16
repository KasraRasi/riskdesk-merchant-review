@echo off
cd /d "%~dp0"
py analyze.py
if errorlevel 1 (echo Run with Python 3 installed. & pause & exit /b 1)
py dashboard.py
copy /Y outputs\riskdesk_demo.html index.html
start "" "%~dp0index.html"
pause
