# 🚀 Deployment Checklist

## ✅ Pre-Deployment (Done Automatically)

- [x] Build configuration created
- [x] Environment variables configured
- [x] Vercel configuration file created
- [x] Production build tested successfully
- [x] All API calls use relative URLs
- [x] Proxy configuration in place

---

## 📋 Step-by-Step Deployment Guide

### Phase 1: Deploy Backend (Required First)

Your Django backend cannot run on Vercel. Deploy it separately:

#### Option A: Railway (Recommended - Easiest)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub account

2. **Deploy Backend**
   ```
   ✓ New Project → Deploy from GitHub
   ✓ Select repository: kanimozhi2905/romato
   ✓ Set root directory: backend
   ```

3. **Add Environment Variables**
   In Railway dashboard, add these variables:
   ```
   SECRET_KEY=django-insecure-change-this-in-production
   DEBUG=False
   ALLOWED_HOSTS=.railway.app,.vercel.app,localhost,127.0.0.1
   MONGODB_URI=mongodb+srv://240171601022_db_user:kani@fooddeliveryai.ghmgxkq.mongodb.net/?appName=Fooddeliveryai
   DB_NAME=food_delivery_db
   JWT_ACCESS_TOKEN_LIFETIME=60
   JWT_REFRESH_TOKEN_LIFETIME=1440
   CORS_ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ```

4. **Configure Start Command**
   ```bash
   pip install -r requirements.txt && pip install gunicorn && gunicorn food_delivery.wsgi:application --bind 0.0.0.0:$PORT
   ```

5. **Deploy & Get URL**
   - Railway will deploy and give you a URL like: `https://romato-production.up.railway.app`
   - Copy this URL - you'll need it for frontend!

#### Option B: Render.com

1. Go to https://render.com
2. New Web Service → Connect GitHub repo
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn food_delivery.wsgi:application --bind 0.0.0.0:$PORT`
6. Add environment variables (same as above)

---

### Phase 2: Deploy Frontend to Vercel

#### Method 1: One-Click Deploy (Easiest)

1. Click this button: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/kanimozhi2905/romato&root-directory=client)

2. Configure in Vercel:
   ```
   Project Name: romato-frontend
   Root Directory: client
   Framework: Create React App
   Build Command: npm run build
   Output Directory: build
   ```

3. Add Environment Variable:
   ```
   Name: REACT_APP_API_URL
   Value: https://your-backend-url.railway.app
   ```

4. Click Deploy!

#### Method 2: Manual Deploy via Dashboard

1. **Go to Vercel**
   - Visit https://vercel.com
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New Project"
   - Import GitHub repository: `kanimozhi2905/romato`

3. **Configure Build**
   ```
   Root Directory: client (CLICK THIS - IT'S IMPORTANT!)
   Framework Preset: Create React App
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **Add Environment Variables**
   In Vercel project settings → Environment Variables:
   ```
   REACT_APP_API_URL = https://your-backend-url.railway.app
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete

#### Method 3: Deploy via CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to client folder
cd client

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

---

## 🔧 Post-Deployment Configuration

### Update Backend CORS

After frontend is deployed, update Django backend CORS settings:

1. **In Railway/Render Dashboard**:
   Add your Vercel URL to CORS_ALLOWED_ORIGINS:
   ```
   CORS_ALLOWED_ORIGINS=https://romato-frontend.vercel.app,http://localhost:3000
   ```

2. **Or in backend/.env**:
   ```python
   CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
   ```

### Test Everything

Visit your deployed Vercel URL and test:

- [ ] Homepage loads
- [ ] Can navigate to products
- [ ] Can add items to cart
- [ ] Can go to checkout
- [ ] Can login/signup
- [ ] Can place order
- [ ] Order success page shows
- [ ] No console errors

---

## 🎯 Quick Reference

### Your URLs After Deployment

```
Frontend (Vercel):     https://romato-xxx.vercel.app
Backend (Railway):     https://romato-production.up.railway.app
Admin Panel:           https://romato-production.up.railway.app/admin/
API Docs:              https://romato-production.up.railway.app/api/docs/
```

### Environment Variables Summary

**Frontend (Vercel):**
```
REACT_APP_API_URL=https://your-backend.railway.app
```

**Backend (Railway):**
```
SECRET_KEY=django-insecure-your-secret-key
DEBUG=False
ALLOWED_HOSTS=.railway.app,.vercel.app
MONGODB_URI=mongodb+srv://...
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
```

---

## 🐛 Troubleshooting

### Problem: NOT_FOUND Error on Vercel

**Solution:**
```
✓ Make sure Root Directory is set to 'client' not 'backend'
✓ Check that package.json exists in client folder
✓ Verify npm run build works locally first
```

### Problem: CORS Error in Browser Console

**Solution:**
```
✓ Add your Vercel URL to backend CORS_ALLOWED_ORIGINS
✓ Restart backend server after adding URL
✓ Clear browser cache and try again
```

### Problem: API Calls Fail (404)

**Solution:**
```
✓ Check REACT_APP_API_URL environment variable is set correctly
✓ Verify backend is running and accessible
✓ Test backend URL directly in browser: https://your-backend.railway.app/api/
```

### Problem: Build Fails on Vercel

**Solution:**
```
✓ Run npm run build locally and fix any errors
✓ Check Node.js version compatibility
✓ Review Vercel build logs for specific error
```

---

## ✅ Success Indicators

You know deployment succeeded when:

1. ✅ Vercel shows "Ready" status (green checkmark)
2. ✅ Can visit https://your-app.vercel.app without errors
3. ✅ See your application homepage with all images loaded
4. ✅ Browser console has no red errors
5. ✅ Can interact with all features (login, cart, checkout)
6. ✅ Backend API responds correctly

---

## 📊 Deployment Status

### Current Status: Ready to Deploy ✅

- [x] Code pushed to GitHub
- [x] Build tested locally
- [x] Configuration files created
- [x] Environment variables documented
- [x] Deployment instructions prepared

### Next Steps

1. Deploy backend to Railway (10 minutes)
2. Deploy frontend to Vercel (5 minutes)
3. Update CORS settings (2 minutes)
4. Test everything (5 minutes)

**Total Time: ~22 minutes**

---

## 📞 Support Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Railway Documentation**: https://docs.railway.app
- **Django Deployment Guide**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Create React App Deployment**: https://create-react-app.dev/docs/deployment/

---

## 🎉 You're Done!

Once everything is deployed and working:

1. Share your Vercel URL with friends!
2. Access admin panel at: `https://your-backend.railway.app/admin/`
3. Monitor deployments in Vercel dashboard
4. View backend logs in Railway dashboard

**Congratulations! Your Food Delivery app is live! 🚀**
