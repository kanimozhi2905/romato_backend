@echo off
echo ========================================
echo Python Installation Checker
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is already installed!
    python --version
    echo.
    goto :setup_backend
)

REM Try py command
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python is already installed (via py command)!
    py --version
    echo.
    goto :setup_backend
)

echo [ERROR] Python is NOT installed on your system!
echo.
echo Please follow these steps:
echo.
echo 1. Download Python from: https://www.python.org/downloads/
echo.
echo 2. Run the installer
echo.
echo 3. IMPORTANT: Check "Add Python to PATH" during installation!
echo.
echo 4. After installation, close this window and open a NEW terminal
echo.
echo 5. Then run: .\setup.bat
echo.
pause
exit /b 1

:setup_backend
echo ========================================
echo Setting up Food Delivery Backend
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [1/6] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
) else (
    echo [1/6] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [3/6] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

REM Install dependencies
echo [4/6] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies may have failed to install
    echo Retrying without quiet mode...
    pip install -r requirements.txt
)
echo.

REM Run migrations
echo [5/6] Running database migrations...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run migrations!
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete! ✅
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Create an admin user:
echo    python manage.py createsuperuser
echo.
echo 2. Load sample data (optional):
echo    python manage.py load_sample_data
echo.
echo 3. Start the server:
echo    python manage.py runserver
echo.
echo 4. Access points:
echo    - API: http://127.0.0.1:8000/api/
echo    - Admin: http://127.0.0.1:8000/admin/
echo    - Docs: http://127.0.0.1:8000/api/docs/
echo.
echo ========================================
pause
