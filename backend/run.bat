@echo off
echo ========================================
echo Starting Food Delivery Backend Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run server
echo Starting Django development server...
echo Access the API at: http://127.0.0.1:8000/
echo Access admin panel at: http://127.0.0.1:8000/admin/
echo Access API docs at: http://127.0.0.1:8000/api/docs/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
