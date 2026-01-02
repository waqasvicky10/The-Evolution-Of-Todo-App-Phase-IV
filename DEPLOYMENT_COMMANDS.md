# 🚀 Deployment Commands - Ready to Execute

**Status**: ✅ Git initialized and committed
**Commit**: Phase II Complete - Full-Stack Todo App
**Files**: 72 files, 14,370 insertions

---

## ✅ STEP 1: Git - COMPLETED

Your code is committed and ready to push!

```
Commit: 1cc2e0f
Message: Phase II Complete - Full-Stack Todo App with Auth
Files: 72 files changed
```

---

## 🔥 STEP 2: Push to GitHub - DO THIS NOW

### 2.1 Create GitHub Repository

1. Go to: **https://github.com/new**
2. Repository name: `todo-app-phase2` (or your choice)
3. Description: `Full-stack todo app with Next.js, FastAPI, and PostgreSQL`
4. Keep it **Public** (or Private if you prefer)
5. **DO NOT** initialize with README (we already have one)
6. Click **"Create repository"**

### 2.2 Push Your Code

GitHub will show you commands. Copy your repository URL, then run:

```bash
cd E:\heckathon-2

# Add your GitHub repository (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/johndoe/todo-app-phase2.git
git branch -M main
git push -u origin main
```

---

## 🎯 STEP 3: Deploy Backend to Render

### 3.1 Create Render Account & Deploy

1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended)
4. Authorize Render

### 3.2 Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"**
3. Find and select your `todo-app-phase2` repository
4. Click **"Connect"**

### 3.3 Configure Service

**Basic Settings:**
```
Name: todo-api-phase2
Environment: Python 3
Region: Oregon (US West) - or closest to you
Branch: main
Root Directory: backend
```

**Build & Start:**
```
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3.4 Environment Variables

Click **"Environment"** → **"Add Environment Variable"**

Add these (one at a time):

```
DATABASE_URL = [Get from Neon - see below]
SECRET_KEY = [Generate - see below]
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
CORS_ORIGINS = https://placeholder.vercel.app
ENVIRONMENT = production
```

**Get DATABASE_URL:**
1. Go to: https://console.neon.tech
2. Sign up / Sign in
3. Create new project
4. Copy connection string (use **pooled** connection)
5. Paste as DATABASE_URL

**Generate SECRET_KEY:**
Run in terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy output and paste as SECRET_KEY

**Note**: We'll update CORS_ORIGINS after deploying frontend

### 3.5 Deploy Backend

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. **SAVE YOUR BACKEND URL**: `https://todo-api-phase2.onrender.com`

### 3.6 Run Database Migrations

After deployment completes:
1. Go to your service page
2. Click **"Shell"** in left sidebar
3. Wait for shell to connect (~10 seconds)
4. Run this command:
   ```bash
   alembic upgrade head
   ```
5. Should see: `Running upgrade -> 001, create users and tasks tables`

### 3.7 Verify Backend

Open in browser: `https://todo-api-phase2.onrender.com/health`

Should see: `{"status":"healthy"}`

---

## 🎨 STEP 4: Deploy Frontend to Vercel

### 4.1 Create Vercel Account & Deploy

1. Go to: **https://vercel.com**
2. Click **"Start Deploying"**
3. Sign up with **GitHub**
4. Click **"Add New..."** → **"Project"**

### 4.2 Import Project

1. Find and click **"Import"** on your `todo-app-phase2` repository
2. If not showing, click **"Adjust GitHub App Permissions"** and grant access

### 4.3 Configure Project

**Project Settings:**
```
Project Name: todo-app-phase2
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build (default)
Output Directory: .next (default)
Install Command: npm install (default)
```

**Environment Variables:**
Click **"Environment Variables"** and add:

```
Name:  NEXT_PUBLIC_API_BASE_URL
Value: https://todo-api-phase2.onrender.com
```

(Use YOUR actual Render backend URL from Step 3.5)

### 4.4 Deploy Frontend

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. **SAVE YOUR FRONTEND URL**: `https://todo-app-phase2.vercel.app`

---

## 🔄 STEP 5: Update Backend CORS

Now that you have your Vercel URL, update backend:

1. Go back to **Render Dashboard**
2. Open your web service
3. Click **"Environment"** in left sidebar
4. Find `CORS_ORIGINS` variable
5. Click **Edit** (pencil icon)
6. Replace value with YOUR Vercel URL:
   ```
   https://todo-app-phase2.vercel.app
   ```
7. Click **"Save Changes"**
8. Service will auto-redeploy (1-2 minutes)

---

## ✅ STEP 6: Verify Everything Works

### Test Backend
```
✓ Health: https://todo-api-phase2.onrender.com/health
✓ API Docs: https://todo-api-phase2.onrender.com/docs
```

### Test Frontend
```
✓ Homepage: https://todo-app-phase2.vercel.app/
✓ Register: https://todo-app-phase2.vercel.app/register
✓ Login: https://todo-app-phase2.vercel.app/login
```

### Full Integration Test
1. Open your Vercel URL
2. Click **"Get Started"**
3. Register with email/password
4. Should redirect to dashboard
5. Create a task
6. Toggle completion
7. Edit task
8. Delete task
9. Logout and login again
10. Tasks should persist

### Check Browser Console
1. Press **F12** to open DevTools
2. Go to **Console** tab
3. Should see NO red errors
4. Should see NO CORS errors

---

## 🎉 SUCCESS!

Your app is now LIVE at:

```
Frontend: https://todo-app-phase2.vercel.app
Backend:  https://todo-api-phase2.onrender.com
API Docs: https://todo-api-phase2.onrender.com/docs
```

---

## 📊 Deployment Checklist

- [ ] Pushed code to GitHub
- [ ] Created Neon PostgreSQL database
- [ ] Deployed backend to Render
- [ ] Set all environment variables
- [ ] Ran database migrations
- [ ] Backend health check passes
- [ ] Deployed frontend to Vercel
- [ ] Set frontend environment variable
- [ ] Updated backend CORS_ORIGINS
- [ ] Full integration test passes
- [ ] No console errors

---

## 🚨 Troubleshooting

### Backend won't start
- Check Render logs for errors
- Verify all environment variables are set
- Ensure DATABASE_URL is correct with `?sslmode=require`

### CORS errors in browser
- Verify CORS_ORIGINS in Render matches Vercel URL exactly
- Must use https:// (not http://)
- No trailing slash
- Wait 1-2 min after updating for redeploy

### Frontend can't reach backend
- Check NEXT_PUBLIC_API_BASE_URL in Vercel
- Verify backend is up: test /health endpoint
- Check browser console for specific error

### Database connection fails
- Verify Neon database is active
- Check connection string has `?sslmode=require`
- Run migrations in Render shell: `alembic upgrade head`

---

## 💡 Quick Links

**Platforms:**
- GitHub: https://github.com
- Render: https://dashboard.render.com
- Vercel: https://vercel.com/dashboard
- Neon: https://console.neon.tech

**Your Project:**
- GitHub Repo: https://github.com/YOUR_USERNAME/YOUR_REPO
- Render Service: https://dashboard.render.com/web/YOUR_SERVICE
- Vercel Project: https://vercel.com/YOUR_USERNAME/YOUR_PROJECT

---

## 📝 Save Your URLs

After deployment, save these:

```
GitHub Repository: ____________________________________
Frontend (Vercel):  ____________________________________
Backend (Render):   ____________________________________
Database (Neon):    ____________________________________
```

---

**Ready to deploy! Start with Step 2 (Create GitHub repo) and follow each step in order.**

**Estimated total time: 25-30 minutes**
**Cost: $0 (all free tiers)**

Good luck! 🚀
