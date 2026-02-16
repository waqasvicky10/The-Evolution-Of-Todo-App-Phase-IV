@echo off
echo ========================================
echo Starting Full Stack Todo App
echo ========================================
echo.

echo Starting Backend (FastAPI)...
start "Todo Backend" cmd /k "cd backend && call venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo Starting Frontend (Next.js)...
start "Todo Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo App should be running at: http://localhost:3000
echo Backend API at: http://localhost:8000
echo ========================================
echo.

echo Opening browser...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo Press any key to exit this launcher (servers will keep running)...
pause
