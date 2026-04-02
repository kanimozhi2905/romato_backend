@echo off
echo ========================================
echo   Food Delivery App - Deployment Prep
echo ========================================
echo.

cd client

echo [1/4] Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Creating production build...
call npm run build
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [3/4] Checking build output...
if exist "build\index.html" (
    echo SUCCESS: Build completed successfully!
) else (
    echo ERROR: Build output not found
    pause
    exit /b 1
)

echo.
echo [4/4] Testing production server...
echo Starting local preview on http://localhost:5000
echo Press Ctrl+C to stop
echo.

call npx serve -s build -p 5000

pause
