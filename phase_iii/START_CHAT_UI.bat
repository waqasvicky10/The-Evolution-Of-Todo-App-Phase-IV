@echo off
REM Start the Chat UI web server
REM
REM This script starts a simple HTTP server for the chat UI on port 8080

echo ========================================
echo Todo Chat UI - Phase III
echo ========================================
echo.
echo Starting web server on http://localhost:8080
echo.
echo Make sure the Chat API is running on http://localhost:8000
echo.
echo ========================================
echo.

cd /d %~dp0\chat_ui
python -m http.server 8080

pause
