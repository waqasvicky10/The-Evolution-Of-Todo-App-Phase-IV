@echo off
echo ========================================
echo Starting Frontend Development Server
echo ========================================
echo.

cd /d "%~dp0"

echo Checking dependencies...
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed
        pause
        exit /b 1
    )
)

echo.
echo Starting Next.js development server...
echo Frontend will be available at: http://localhost:3000
echo.
echo Press CTRL+C to stop the server
echo.

call npm run dev

pause
