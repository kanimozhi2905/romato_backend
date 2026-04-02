# Deployment Guide for Food Delivery App

## 🚀 Quick Start: Deploy Frontend to Vercel

### Prerequisites
- ✅ GitHub account
- ✅ Vercel account (free at vercel.com)
- ✅ Backend deployed to Railway/Render (for API)

---

## Option 1: Deploy React Frontend to Vercel ⭐ Recommended

### Step 1: Prepare Your Code

1. **Update API URLs in your React app** to point to your backend:

```javascript
// In client/src/setupProxy.js OR environment variables
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Update all fetch calls to use the API URL
fetch(`${API_URL}/api/auth/login/`, { ... })
```

2. **Create `.env.production` in client folder**:
```
REACT_APP_API_URL=https://your-backend.railway.app
```

3. **Build locally to test**:
```bash
cd client
npm run build
# Check if build folder is created successfully
```

### Step 2: Push to GitHub

Your code is already pushed! ✅

### Step 3: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your GitHub repository: `kanimozhi2905/romato`
4. Configure project:
   - **Framework Preset**: Create React App
   - **Root Directory**: `client` (IMPORTANT!)
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

5. Add Environment Variables:
   ```
   REACT_APP_API_URL = https://your-backend-url.railway.app
   ```

6. Click **"Deploy"**

### Step 4: Update CORS Settings in Django

In your backend `.env` file or settings.py:
```python
CORS_ALLOWED_ORIGINS = [
    'https://your-app.vercel.app',  # Your new Vercel URL
    'http://localhost:3000',
]
```

---

## Option 2: Deploy Full Stack to Railway

### Backend Deployment (Railway)

1. Go to [railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Select your repo: `kanimozhi2905/romato`
4. Set root directory: `backend`
5. Add environment variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=.railway.app,your-app.vercel.app
   MONGODB_URI=your-mongodb-uri
   ```
6. Add start command:
   ```bash
   pip install gunicorn && gunicorn food_delivery.wsgi:application --bind 0.0.0.0:$PORT
   ```

### Frontend Deployment

Follow Option 1 steps above, pointing to Railway backend URL.

---

## Common Errors & Solutions

### ❌ NOT_FOUND Error

**Cause**: Wrong root directory or missing build files

**Solution**:
- Make sure Root Directory is set to `client` in Vercel
- Verify `npm run build` works locally first

### ❌ CORS Error

**Cause**: Backend doesn't allow frontend domain

**Solution**:
```python
# backend/settings.py
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
```

Add your Vercel URL to allowed origins.

### ❌ API 404 Errors

**Cause**: Wrong API URL or proxy configuration

**Solution**:
- Use environment variable for API URL
- Don't rely on localhost in production
- Update all fetch calls to use full backend URL

---

## Testing Before Deployment

1. **Test Build Locally**:
```bash
cd client
npm run build
serve -s build
# Visit http://localhost:5000
```

2. **Check All API Calls**:
- Search for hardcoded `localhost` URLs
- Replace with environment variable

3. **Verify Environment Variables**:
- Check `.env.production` has correct values
- Test with backend deployed to Railway

---

## Post-Deployment Checklist

✅ Frontend loads without errors
✅ Can login/signup
✅ Can add items to cart
✅ Can place orders
✅ Admin panel accessible
✅ Images load correctly
✅ No console errors

---

## Useful Commands

```bash
# Test production build locally
cd client
npm run build
npx serve -s build

# View Vercel logs
vercel logs

# Redeploy to Vercel
git push origin main
```

---

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
