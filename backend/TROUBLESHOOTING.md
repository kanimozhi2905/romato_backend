# Troubleshooting Guide

Common issues and their solutions for the Food Delivery Backend.

---

## Installation Issues

### Issue: Python Not Found

**Error:** `'python' is not recognized as an internal or external command`

**Solutions:**

1. **Verify Python Installation:**
   ```bash
   python --version
   ```

2. **Add Python to PATH:**
   - Open "Environment Variables" in Windows
   - Add Python installation path to PATH
   - Example: `C:\Python39\` and `C:\Python39\Scripts\`

3. **Reinstall Python:**
   - Download from https://www.python.org/
   - ✅ Check "Add Python to PATH" during installation

---

### Issue: Virtual Environment Creation Fails

**Error:** `The virtual environment was not created successfully`

**Solutions:**

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Create venv with clear flag
python -m venv venv --clear

# If still failing, try without ensurepip
python -m venv venv --without-pip
```

---

### Issue: Pip Install Fails

**Error:** `Could not install packages due to EnvironmentError`

**Solutions:**

```bash
# Try with --user flag
pip install --user -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt

# Clear pip cache
pip cache purge
pip install -r requirements.txt
```

---

### Issue: Dependency Conflicts

**Error:** `ERROR: Cannot install ... because these package versions have conflicting dependencies`

**Solutions:**

```bash
# Use --no-deps flag (careful!)
pip install --no-deps -r requirements.txt

# Or upgrade all packages
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## Database Issues

### Issue: Migration Errors

**Error:** `django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 module`

**Solution:** You're trying to use PostgreSQL but haven't installed it. Either:
- Install: `pip install psycopg2-binary`
- Or stick with SQLite (default)

---

**Error:** `table already exists`

**Solution:**
```bash
# Fake initial migration
python manage.py migrate --fake-initial

# Or reset database (development only!)
del db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

---

### Issue: Database Locked

**Error:** `database is locked`

**Solutions:**

1. Close all terminals running Django
2. Delete the database lock file:
   ```bash
   del db.sqlite3-journal
   ```
3. Restart server

---

## Server Issues

### Issue: Port Already in Use

**Error:** `Error: That port is already in use`

**Solutions:**

```bash
# Use different port
python manage.py runserver 8080

# Or kill the process using port 8000
# Windows PowerShell:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

---

### Issue: Allowed Hosts Error

**Error:** `Invalid HTTP_HOST header: 'localhost:8000'. You may need to add 'localhost' to ALLOWED_HOSTS`

**Solution:** Update `.env` file:
```env
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Authentication Issues

### Issue: JWT Token Not Working

**Error:** `Authorization header must be Bearer scheme`

**Solution:** Ensure correct header format:
```
Authorization: Bearer your_token_here
```
NOT:
```
Authorization: your_token_here
```

---

**Error:** `Token is invalid or expired`

**Solution:**
1. Token might be expired - login again
2. Or refresh token using `/api/auth/token/refresh/`
3. Check JWT settings in `.env`

---

### Issue: Can't Register User

**Error:** `Email already registered`

**Solution:** Email must be unique. Use different email or delete existing user:
```bash
python manage.py shell
>>> from apps.authentication.models import User
>>> User.objects.filter(email='test@example.com').delete()
```

---

## CORS Issues

### Issue: Frontend Can't Connect

**Error:** `Access to fetch at ... has been blocked by CORS policy`

**Solutions:**

1. **Check backend is running:** http://127.0.0.1:8000/

2. **Update CORS settings in `.env`:**
   ```env
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```

3. **Restart Django server** after changing .env

4. **Check frontend URL matches exactly** (including http/https)

---

## Cart Issues

### Issue: Cart Not Updating

**Possible Causes:**
- User not authenticated
- Food item doesn't exist or unavailable
- Invalid quantity

**Debug Steps:**
1. Check if user is logged in (token exists)
2. Verify food item exists: `GET /api/foods/{id}/`
3. Check error response message

---

**Error:** `Cart not found`

**Solution:** Cart is auto-created on first add. If getting this error:
```bash
# Manually create cart via API
POST /api/cart/add/
{
  "food_item_id": 1,
  "quantity": 1
}
```

---

## Order Issues

### Issue: Can't Place Order

**Error:** `Cart is empty`

**Solution:** Add items to cart first before placing order.

---

**Error:** `Invalid pincode` or `Invalid phone number`

**Solution:** Ensure correct format:
- Phone: 10 digits (e.g., `9876543210`)
- Pincode: 6 digits (e.g., `123456`)

---

### Issue: Order Status Not Updating

**Error:** `Only admins can update order status`

**Solution:** Only admin users can update order status. Login with admin account.

Check if user is admin:
```bash
python manage.py shell
>>> from apps.authentication.models import User
>>> user = User.objects.get(email='your@email.com')
>>> user.is_admin
```

---

## File Upload Issues

### Issue: Images Not Uploading

**Error:** `The submitted file is empty` or `Upload a valid image`

**Solutions:**

1. **Check file size** - must be > 0 bytes
2. **Check file format** - must be valid image (jpg, png, etc.)
3. **Check media folder permissions** - should be writable
4. **Content-Type header** - use multipart/form-data

**Correct cURL for image upload:**
```bash
curl -X POST http://127.0.0.1:8000/api/foods/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "name=Test Pizza" \
  -F "description=Test" \
  -F "price=199" \
  -F "category_id=1" \
  -F "image=@/path/to/image.jpg"
```

---

## Admin Panel Issues

### Issue: Can't Access Admin Panel

**Error:** `DoesNotExist at /admin/` or login doesn't work

**Solution:** Create superuser:
```bash
python manage.py createsuperuser
```

Follow prompts for email, name, password.

---

### Issue: Changes Not Reflecting in Admin

**Solution:**
1. Hard refresh browser (Ctrl+Shift+R)
2. Clear browser cache
3. Check if changes saved in database

---

## Performance Issues

### Issue: Slow API Responses

**Solutions:**

1. **Enable Django debug toolbar to profile:**
   ```bash
   pip install django-debug-toolbar
   ```

2. **Check for N+1 queries** - use select_related/prefetch_related

3. **Add database indexes** on frequently queried fields

4. **Enable pagination** - already enabled by default

---

### Issue: Memory Leaks

**Symptoms:** Server gets slower over time

**Solutions:**
1. Restart development server periodically
2. Check for unclosed database connections
3. Use Django's memory profiling tools

---

## Common Error Messages

### "Method Not Allowed"

**Cause:** Using wrong HTTP method

**Solution:** Check API documentation for correct method:
- GET for retrieving data
- POST for creating
- PUT/PATCH for updating
- DELETE for removing

---

### "Authentication credentials were not provided"

**Cause:** Missing or invalid token

**Solution:**
```bash
# Include Authorization header
Authorization: Bearer your_access_token
```

---

### "Permission denied"

**Cause:** Insufficient permissions

**Solutions:**
- Some endpoints require admin (`is_admin=True`)
- Check user permissions in admin panel
- Some endpoints require authentication

---

### "Not Found" (404)

**Cause:** Resource doesn't exist or wrong URL

**Solutions:**
1. Check URL spelling
2. Verify resource exists
3. Check ID is correct

---

## Debugging Tips

### Enable Debug Mode

In `.env`:
```env
DEBUG=True
```

This shows detailed error messages.

---

### Check Django Logs

Run server with verbose logging:
```bash
python manage.py runserver --verbosity 2
```

---

### Use Django Shell

```bash
python manage.py shell
```

Test queries directly:
```python
from apps.food.models import FoodItem
FoodItem.objects.all()

from apps.cart.models import Cart
Cart.objects.all()
```

---

### Test with cURL

Always test API directly before debugging frontend:

```bash
# Test login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123"}'
```

---

## Getting More Help

### Check Documentation
1. README.md - Full documentation
2. API_TESTING_GUIDE.md - API examples
3. PROJECT_SUMMARY.md - Feature list

### Django Resources
- Official Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Stack Overflow: Tag `django-rest-framework`

### Common Commands for Debugging

```bash
# Check Django version
python -m django --version

# List all migrations
python manage.py showmigrations

# Check database tables
python manage.py dbshell
> .tables  # SQLite
> \dt      # PostgreSQL

# View SQL for a query
from apps.food.models import FoodItem
print(str(FoodItem.objects.all().query))

# Clear all data (development only!)
python manage.py flush
```

---

## Quick Checklist

When something doesn't work:

- [ ] Is Django server running?
- [ ] Is virtual environment activated?
- [ ] Are dependencies installed?
- [ ] Is database migrated?
- [ ] Is CORS configured correctly?
- [ ] Is the correct HTTP method being used?
- [ ] Are authentication headers included?
- [ ] Is the URL correct?
- [ ] Is the data in correct format?
- [ ] Have you checked the error logs?

---

## Still Having Issues?

1. **Search the error message** online
2. **Check GitHub issues** for similar problems
3. **Review the code** for typos
4. **Start fresh** - new virtual environment
5. **Ask for help** with specific error details

---

**Remember:** Most issues are configuration-related. Double-check your setup! 🛠️
