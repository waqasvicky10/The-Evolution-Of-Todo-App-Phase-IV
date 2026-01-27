@echo off
echo Killing any existing Gradio processes on port 7860...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :7860') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)
echo Done. You can now run the app.
pause
