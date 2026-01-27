@echo off
echo ========================================
echo Phase III Todo App - Final Run
echo ========================================
echo.

cd /d E:\heckathon-2

echo Checking dependencies...
python -c "import gradio; print('Gradio:', gradio.__version__)" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements-gradio.txt
)

echo.
echo Starting Phase III Todo App...
echo App will open at: http://localhost:7860
echo Press Ctrl+C to stop
echo.

python gradio_app.py

pause
