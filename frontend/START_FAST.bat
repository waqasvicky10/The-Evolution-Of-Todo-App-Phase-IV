@echo off
echo ========================================
echo Fast Frontend Startup (Turbopack)
echo ========================================
echo.

cd /d E:\heckathon-2\frontend

echo Clearing cache for fresh start...
if exist ".next" (
    rmdir /s /q .next 2>nul
    echo ✓ Cache cleared
)

echo.
echo Starting with Turbopack (FASTEST)...
echo Expected startup: 2-5 seconds
echo.
echo App will open at: http://localhost:3000
echo Press Ctrl+C to stop
echo.

call npm run dev

pause
