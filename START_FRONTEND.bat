@echo off
echo ========================================
echo Starting Frontend (Next.js)
echo ========================================
echo.

cd /d E:\heckathon-2\frontend

echo Checking dependencies...
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting frontend server...
echo The app will open at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
