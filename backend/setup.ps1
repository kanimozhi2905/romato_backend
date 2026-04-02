# Food Delivery Backend - Complete Setup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Food Delivery Backend - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/7] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    try {
        $pythonVersion = py --version 2>&1
        Write-Host "[OK] Python found (via py): $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Python is NOT installed!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "IMPORTANT: Check 'Add Python to PATH' during installation" -ForegroundColor Yellow
        Write-Host ""
        pause
        exit 1
    }
}
Write-Host ""

# Step 2: Create Virtual Environment
Write-Host "[2/7] Setting up virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Step 3: Activate Virtual Environment
Write-Host "[3/7] Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Step 4: Upgrade pip
Write-Host "[4/7] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "[OK] pip upgraded successfully" -ForegroundColor Green
Write-Host ""

# Step 5: Install Dependencies
Write-Host "[5/7] Installing dependencies (this may take 2-3 minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Some packages may have failed to install" -ForegroundColor Yellow
}
Write-Host ""

# Step 6: Run Migrations
Write-Host "[6/7] Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Database migrations completed" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Migration failed" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""

# Step 7: Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! ✅" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create admin user:" -ForegroundColor White
Write-Host "   python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Load sample data (optional):" -ForegroundColor White
Write-Host "   python manage.py load_sample_data" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Yellow
Write-Host "  • API:     http://127.0.0.1:8000/api/" -ForegroundColor Cyan
Write-Host "  • Admin:   http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "  • Docs:    http://127.0.0.1:8000/api/docs/" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
