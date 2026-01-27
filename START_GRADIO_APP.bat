@echo off
echo ========================================
echo Starting Gradio Todo App
echo ========================================
echo.

REM Check if gradio + deps are installed
python -c "import gradio; import dotenv; import openai; import speech_recognition" 2>nul
if errorlevel 1 (
    echo Installing Gradio and dependencies: gradio, openai, python-dotenv, SpeechRecognition...
    pip install -r requirements-gradio.txt
    echo.
)

echo Starting app...
echo.
echo The app will open at: http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo.

python gradio_app.py

pause
