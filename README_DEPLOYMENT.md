# Food Delivery Application - Deployment Instructions

## 🎯 Quick Deploy to Vercel

### Step 1: Click to Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/kanimozhi2905/romato&root-directory=client)

### Step 2: Configure in Vercel Dashboard

When deploying, use these settings:

```
Root Directory: client
Framework Preset: Create React App
Build Command: npm run build
Output Directory: build
Install Command: npm install
```

### Step 3: Add Environment Variables

In Vercel project settings, add:

```
REACT_APP_API_URL = https://your-backend-url.railway.app
```

(Replace with your actual backend URL after deploying the Django backend)

---

## 📋 Manual Deployment Steps

### Option A: Deploy Frontend to Vercel (Recommended)

#### 1. Prepare Backend First

Your Django backend needs to be deployed separately. Recommended platforms:

- **Railway** (railway.app) - Easy Django deployment
- **Render** (render.com) - Free tier available
- **PythonAnywhere** - Django-friendly

**Backend Deployment Checklist:**
- ✅ Deploy backend to Railway/Render
- ✅ Get your backend URL (e.g., `https://myapp.railway.app`)
- ✅ Update CORS settings in Django to allow your Vercel domain
- ✅ Test backend API is accessible

#### 2. Deploy Frontend to Vercel

**Via Vercel Dashboard:**

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import GitHub repo: `kanimozhi2905/romato`
4. Set Root Directory: `client` ⚠️ **IMPORTANT**
5. Framework: Create React App (auto-detected)
6. Build Command: `npm run build`
7. Output Directory: `build`
8. Add environment variable: `REACT_APP_API_URL`
9. Click Deploy!

**Via Vercel CLI:**

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to client folder
cd client

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### 3. Update Backend CORS

After getting your Vercel URL, update Django settings:

```python
# backend/settings.py
CORS_ALLOWED_ORIGINS = [
    'https://your-app.vercel.app',  # Your Vercel URL
    'http://localhost:3000',
]
```

---

### Option B: Deploy Everything to Railway (Alternative)

If you want everything in one place:

#### 1. Create Railway Account

Go to [railway.app](https://railway.app)

#### 2. Deploy Backend

1. New Project → Deploy from GitHub
2. Select repo: `romato`
3. Set root directory: `backend`
4. Add environment variables:
   ```
   SECRET_KEY=django-insecure-your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=.railway.app,.vercel.app
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/fooddelivery
   ```
5. Start command:
   ```bash
   pip install gunicorn && gunicorn food_delivery.wsgi:application --bind 0.0.0.0:$PORT
   ```

#### 3. Deploy Frontend on Railway

1. Add another service → Empty Service
2. Set root directory: `client`
3. Build command: `npm run build`
4. Start command: `npx serve -s build`
5. Add variable: `RAILWAY_PORT=5000`

---

## 🔧 Pre-Deployment Testing

### Test Production Build Locally

```bash
# Navigate to client folder
cd client

# Install dependencies
npm install

# Create production build
npm run build

# Serve the build locally
npx serve -s build -p 5000

# Visit http://localhost:5000
```

### Verify All API Calls

Check that no hardcoded localhost URLs exist:

```bash
# Search for problematic URLs
grep -r "localhost:8000" src/
grep -r "127.0.0.1:8000" src/
```

All API calls should use environment variables:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
fetch(`${API_URL}/api/...`)
```

---

## 🐛 Common Issues & Solutions

### Issue 1: NOT_FOUND Error

**Problem**: Vercel can't find build files

**Solution**:
- Make sure Root Directory is set to `client`
- Verify `npm run build` completes successfully
- Check that `build` folder exists after build

### Issue 2: CORS Errors

**Problem**: Backend blocks frontend requests

**Solution**:
```python
# backend/settings.py
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')

# Add your Vercel URL to .env file
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### Issue 3: API 404 Errors

**Problem**: Can't connect to backend

**Solution**:
- Ensure backend is deployed and running
- Check REACT_APP_API_URL environment variable
- Verify backend URL is accessible (test in browser)

### Issue 4: Build Fails

**Problem**: npm build fails on Vercel

**Solution**:
- Check Node.js version compatibility
- Review build logs in Vercel dashboard
- Test build locally first: `npm run build`

---

## ✅ Post-Deployment Checklist

After deployment, verify:

- [ ] Homepage loads correctly
- [ ] Can navigate between pages
- [ ] Login/Signup works
- [ ] Can add items to cart
- [ ] Can place orders
- [ ] Admin panel accessible (via direct URL)
- [ ] Images load properly
- [ ] No console errors
- [ ] Mobile responsive works

---

## 🔗 Useful Links

### Your Application
- **Frontend (after deploy)**: Will be `https://romato-xxx.vercel.app`
- **Backend (local)**: http://localhost:8000
- **Admin Panel (local)**: http://localhost:8000/admin/

### Documentation
- [Vercel Docs](https://vercel.com/docs)
- [Create React App Deployment](https://create-react-app.dev/docs/deployment/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Railway Docs](https://docs.railway.app)

### Support
- Vercel Discord: https://vercel.com/discord
- Railway Support: https://railway.app/discord

---

## 📊 Current Project Structure

```
romato/
├── client/              ← Deploy this to Vercel
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── build/          ← Generated after npm run build
├── backend/            ← Deploy to Railway/Render
│   ├── apps/
│   ├── food_delivery/
│   ├── manage.py
│   └── requirements.txt
└── DEPLOYMENT_INSTRUCTIONS.md
```

---

## 🎉 Success Indicators

You'll know deployment succeeded when:

1. ✅ Vercel shows "Ready" status
2. ✅ Can visit your Vercel URL without errors
3. ✅ See your application homepage
4. ✅ Browser console has no red errors
5. ✅ Can interact with all features

---

**Last Updated**: April 2, 2026
**Repository**: https://github.com/kanimozhi2905/romato
