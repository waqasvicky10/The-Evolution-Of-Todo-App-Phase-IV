@echo off
echo ========================================
echo Fast Frontend Startup - Clean Install
echo ========================================
echo.

cd /d E:\heckathon-2\frontend

echo Step 1: Removing old cache...
if exist ".next" (
    rmdir /s /q .next
    echo ✓ Removed .next cache
) else (
    echo - No .next cache found
)

echo.
echo Step 2: Checking node_modules...
if not exist "node_modules" (
    echo Installing dependencies (this may take a few minutes)...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✓ Dependencies installed
) else (
    echo ✓ node_modules exists
)

echo.
echo Step 3: Starting optimized dev server...
echo The app will open at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
