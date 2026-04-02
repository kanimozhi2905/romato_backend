# Python Installation Guide for Windows

## Step 1: Download Python

1. **Visit the official Python website:**
   - Go to: https://www.python.org/downloads/

2. **Download Python 3.8 or higher:**
   - Click the yellow "Download Python" button (latest version recommended)
   - Or scroll down and choose Python 3.8.x or higher

## Step 2: Install Python

1. **Run the installer:**
   - Double-click the downloaded `.exe` file

2. **⚠️ IMPORTANT - Check this box first:**
   - ✅ **"Add Python to PATH"** - This is CRITICAL!
   - Make sure this checkbox is checked before clicking "Install Now"

3. **Click "Install Now"**
   - Wait for installation to complete (2-3 minutes)

4. **Click "Close"**

## Step 3: Verify Installation

1. **Open a NEW Command Prompt or PowerShell:**
   - Close any open terminals
   - Open new terminal (they need to be restarted to see Python)

2. **Check Python is installed:**
   ```bash
   python --version
   ```
   
   You should see: `Python 3.x.x`

3. **If that doesn't work, try:**
   ```bash
   py --version
   ```

## Step 4: Run Backend Setup

Once Python is installed and verified:

```bash
cd "c:\Food delivery\backend"
.\setup.bat
```

## Alternative: Manual Setup

If the batch script still doesn't work, run these commands manually:

```bash
# Navigate to backend
cd "c:\Food delivery\backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (follow prompts)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## Troubleshooting

### "python is not recognized"

**Solution 1:** Restart your computer after Python installation

**Solution 2:** Add Python to PATH manually:
1. Press Win + R, type `sysdm.cpl`, press Enter
2. Click "Advanced" tab
3. Click "Environment Variables"
4. Under "System variables", find and select "Path"
5. Click "Edit"
6. Click "New" and add:
   - `C:\Python39\` (or your Python installation path)
   - `C:\Python39\Scripts\`
7. Click OK on all windows
8. Restart terminal

### Different Python Version

If you have multiple Python versions:
```bash
# Try using py command
py -m venv venv
py -3.9 -m venv venv  # Replace with your version
```

## Quick Check Commands

After installation, these should all work:
```bash
python --version
pip --version
python -m venv --help
```

## Need Help?

If you're still having issues:
1. Make sure you checked "Add Python to PATH" during installation
2. Try restarting your computer
3. Reinstall Python if needed
4. Make sure you downloaded from python.org (not Microsoft Store)

---

**Once Python is installed successfully, come back and run:**
```bash
cd "c:\Food delivery\backend"
.\setup.bat
```
