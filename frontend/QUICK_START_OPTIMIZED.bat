@echo off
echo ========================================
echo Quick Start - Optimized Frontend
echo ========================================
echo.

cd /d E:\heckathon-2\frontend

echo Checking dependencies...
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install --prefer-offline --no-audit
)

echo.
echo Clearing Next.js cache for faster startup...
if exist ".next" (
    rmdir /s /q .next 2>nul
)

echo.
echo Starting dev server with optimizations...
echo.
echo TIP: First startup may take 10-30 seconds
echo      Subsequent startups will be faster (3-10 seconds)
echo.
echo The app will open at: http://localhost:3000
echo Press Ctrl+C to stop
echo.

REM Start dev server
call npm run dev

pause
