@echo off
echo ========================================
echo Stopping old Gradio processes...
echo ========================================
echo.

cd /d E:\heckathon-2

echo Killing processes on port 7860...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :7860 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Starting Phase III Todo App...
echo ========================================
echo.
echo App will open at: http://localhost:7860
echo Press Ctrl+C to stop
echo.

python gradio_app.py

pause
