# 🚀 Quick Start Guide - Food Delivery Backend

This is your complete guide to getting the Food Delivery Backend up and running in minutes.

## 📋 Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Comes with Python
- **Text Editor** - VS Code, PyCharm, or any editor

## ⚡ Quick Setup (Windows)

### Option 1: Automated Setup (Recommended)

1. **Open Command Prompt or PowerShell**

2. **Navigate to backend directory:**
   ```bash
   cd "c:\Food delivery\backend"
   ```

3. **Run the setup script:**
   ```bash
   setup.bat
   ```

4. **Create admin user when prompted:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set:
   - Email address
   - Name  
   - Password

5. **Start the server:**
   ```bash
   run.bat
   ```

### Option 2: Manual Setup

1. **Open Command Prompt or PowerShell**

2. **Navigate to backend directory:**
   ```bash
   cd "c:\Food delivery\backend"
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment:**
   ```bash
   .\venv\Scripts\activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start server:**
   ```bash
   python manage.py runserver
   ```

## 🎯 Access Points

Once the server is running, you can access:

- **API Base URL**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **ReDoc Documentation**: http://127.0.0.1:8000/api/redoc/

## ✅ Verify Installation

1. **Check if server is running** - You should see:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

2. **Visit API documentation** at http://127.0.0.1:8000/api/docs/

3. **Login to admin panel** at http://127.0.0.1:8000/admin/ with your superuser credentials

## 🧪 Test the API

### Using cURL

**Register a new user:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"password\":\"testpass123\",\"password_confirm\":\"testpass123\"}"
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"testpass123\"}"
```

### Using Postman

1. Download [Postman](https://www.postman.com/downloads/)
2. Create a new request to `http://127.0.0.1:8000/api/auth/register/`
3. Set method to POST
4. In Body tab, select raw and JSON
5. Add:
   ```json
   {
     "name": "Test User",
     "email": "test@example.com",
     "password": "testpass123",
     "password_confirm": "testpass123"
   }
   ```
6. Click Send

## 🗄️ Database

By default, SQLite is used for development. The database file `db.sqlite3` will be created automatically in the backend directory.

### Switch to PostgreSQL (Optional)

1. Install PostgreSQL: https://www.postgresql.org/download/
2. Create a database:
   ```sql
   CREATE DATABASE food_delivery_db;
   ```
3. Update `.env` file:
   ```env
   DB_NAME=food_delivery_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```
4. Install PostgreSQL adapter:
   ```bash
   pip install psycopg2-binary
   ```
5. Update `settings.py` to use PostgreSQL (already configured to read from .env)
6. Run migrations:
   ```bash
   python manage.py migrate
   ```

## 📝 Common Commands

```bash
# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test
```

## 🔧 Troubleshooting

### Port Already in Use

**Error:** `Error: That port is already in use.`

**Solution:** Use a different port:
```bash
python manage.py runserver 8080
```

### Python Not Found

**Error:** `'python' is not recognized as an internal or external command`

**Solution:** 
1. Reinstall Python from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. Restart your terminal

### Permission Denied

**Error:** `Permission denied` when running scripts

**Solution:** Run PowerShell as Administrator or:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Virtual Environment Issues

**Error:** `The virtual environment was not created successfully`

**Solution:**
```bash
python -m pip install --upgrade pip
python -m venv venv --clear
```

## 📦 Project Structure

```
backend/
├── apps/
│   ├── authentication/    # User auth, JWT tokens
│   ├── food/             # Food items & categories
│   ├── cart/             # Shopping cart functionality
│   └── orders/           # Order management
├── food_delivery/        # Django project settings
├── media/                # Uploaded images (auto-created)
├── venv/                 # Virtual environment (auto-created)
├── .env                  # Environment variables
├── .gitignore           # Git ignore rules
├── db.sqlite3           # SQLite database (auto-created)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── README.md            # Full documentation
├── API_TESTING_GUIDE.md # API testing examples
├── setup.bat            # Windows setup script
└── run.bat             # Windows run script
```

## 🔐 Default Configuration

- **DEBUG**: True (development mode)
- **CORS Enabled**: Yes (for localhost:3000)
- **Database**: SQLite
- **JWT Token Lifetime**: 
  - Access: 60 minutes
  - Refresh: 24 hours

## 🎯 Next Steps

1. **Explore API Documentation** at http://127.0.0.1:8000/api/docs/
2. **Login to Admin Panel** and add some categories and food items
3. **Test the Complete Flow**:
   - Register a user
   - Add food items to database via admin
   - Login with the user
   - Add items to cart
   - Place an order
4. **Connect Frontend** - Your React app is already configured to work with this backend!

## 🌟 Key Features

✅ JWT Authentication  
✅ User Registration & Login  
✅ Food Categories Management  
✅ Food Items with Images  
✅ Shopping Cart System  
✅ Order Placement & Tracking  
✅ Admin Panel  
✅ API Documentation  
✅ CORS Support for React  
✅ Input Validation  
✅ Error Handling  

## 📞 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) for API examples
- Visit the API documentation at http://127.0.0.1:8000/api/docs/

## 🎉 Success!

If you've completed all steps, your Food Delivery Backend is ready to use! 

**Happy Coding! 🚀**
