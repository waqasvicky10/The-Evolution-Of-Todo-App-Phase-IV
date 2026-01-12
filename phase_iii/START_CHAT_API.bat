@echo off
REM Start the FastAPI Chat API Server
REM
REM This script starts the Phase III chat API on port 8000
REM Make sure to set your ANTHROPIC_API_KEY environment variable first

echo ========================================
echo Todo Chat API - Phase III
echo ========================================
echo.
echo Starting FastAPI server on http://localhost:8000
echo.
echo ========================================
echo.

REM Start the server
cd /d %~dp0
python -m uvicorn chat_api.main:app --reload --host 0.0.0.0 --port 8000

REM Start the server
cd /d %~dp0
python -m uvicorn chat_api.main:app --reload --host 0.0.0.0 --port 8000

pause
