# Production Deployment Checklist

**Date**: 2026-01-01
**Application**: Todo App Phase II
**Status**: ✅ Ready to Deploy

---

## Pre-Deployment Verification ✅

- [x] Backend code complete and tested
- [x] Frontend code complete and tested
- [x] All dependencies listed in requirements.txt/package.json
- [x] Environment configuration files present
- [x] Database migrations created
- [x] API documentation generated
- [x] Local testing successful

---

## Deployment Steps

### 1️⃣ Get Neon Database Connection String

- [ ] Go to https://console.neon.tech
- [ ] Sign in or create account
- [ ] Create new project (or use existing)
- [ ] Copy **pooled connection string**
- [ ] Save for step 3

**Format:**
```
postgresql://user:pass@host.neon.tech/dbname?sslmode=require
```

---

### 2️⃣ Push Code to GitHub

- [ ] Create GitHub repository at https://github.com/new
- [ ] Initialize git in your project:
  ```bash
  cd E:\heckathon-2
  git init
  git add .
  git commit -m "Phase II Complete - Ready for deployment"
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```

---

### 3️⃣ Deploy Backend to Render

- [ ] Go to https://render.com
- [ ] Sign up with GitHub
- [ ] Click "New +" → "Web Service"
- [ ] Connect your repository
- [ ] Configure:
  - Name: `todo-api-phase2`
  - Environment: `Python 3`
  - Root Directory: `backend`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

- [ ] Add Environment Variables:
  ```
  DATABASE_URL=[Your Neon connection string]
  SECRET_KEY=[Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"]
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=15
  REFRESH_TOKEN_EXPIRE_DAYS=7
  CORS_ORIGINS=https://your-app.vercel.app
  ENVIRONMENT=production
  ```

- [ ] Click "Create Web Service"
- [ ] Wait for deployment (3-5 min)
- [ ] Save backend URL: `https://todo-api-phase2.onrender.com`
- [ ] Go to Shell tab and run: `alembic upgrade head`
- [ ] Verify: Visit `https://todo-api-phase2.onrender.com/health`

---

### 4️⃣ Deploy Frontend to Vercel

- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub
- [ ] Click "Add New..." → "Project"
- [ ] Import your repository
- [ ] Configure:
  - Framework Preset: `Next.js`
  - Root Directory: `frontend`
  - Build Command: `npm run build`

- [ ] Add Environment Variable:
  ```
  NEXT_PUBLIC_API_BASE_URL=https://todo-api-phase2.onrender.com
  ```

- [ ] Click "Deploy"
- [ ] Wait for deployment (2-3 min)
- [ ] Save frontend URL: `https://your-project.vercel.app`

---

### 5️⃣ Update Backend CORS

- [ ] Go back to Render dashboard
- [ ] Open your web service
- [ ] Click "Environment"
- [ ] Update `CORS_ORIGINS` with your actual Vercel URL:
  ```
  https://your-project.vercel.app
  ```
- [ ] Click "Save Changes"
- [ ] Wait for redeployment (1-2 min)

---

### 6️⃣ Test Production Deployment

#### Backend Tests
- [ ] Health check: `https://todo-api-phase2.onrender.com/health`
  - Should return: `{"status":"healthy"}`
- [ ] Root endpoint: `https://todo-api-phase2.onrender.com/`
  - Should return API info
- [ ] API docs: `https://todo-api-phase2.onrender.com/docs`
  - Should show Swagger UI

#### Frontend Tests
- [ ] Landing page: `https://your-project.vercel.app/`
  - Should load successfully
- [ ] Register page: `https://your-project.vercel.app/register`
  - Form should be visible
- [ ] Login page: `https://your-project.vercel.app/login`
  - Form should be visible

#### Full Integration Test
- [ ] Register a new account
- [ ] Receive success message
- [ ] Redirected to dashboard
- [ ] Create a new task
- [ ] Task appears in list
- [ ] Toggle task completion
- [ ] Edit task description
- [ ] Delete task
- [ ] Logout
- [ ] Login again
- [ ] Tasks persist

#### Browser Console Check
- [ ] Open developer tools (F12)
- [ ] Check console for errors
- [ ] Should see no CORS errors
- [ ] Should see no 401/403/500 errors

---

## Post-Deployment Configuration

### Optional: Custom Domain

#### For Frontend (Vercel)
- [ ] Go to Project Settings → Domains
- [ ] Add your domain
- [ ] Update DNS records (A/CNAME)
- [ ] Wait for DNS propagation

#### For Backend (Render)
- [ ] Go to Settings → Custom Domains
- [ ] Add your domain
- [ ] Update DNS records
- [ ] Update frontend NEXT_PUBLIC_API_BASE_URL

---

## Monitoring Setup

### Uptime Monitoring
- [ ] Sign up at https://uptimerobot.com
- [ ] Add monitor for backend health endpoint
- [ ] Add monitor for frontend homepage
- [ ] Configure email alerts

### Error Tracking (Optional)
- [ ] Sign up at https://sentry.io
- [ ] Install Sentry SDK in backend/frontend
- [ ] Configure error reporting

---

## Production URLs

Fill in your actual URLs:

```
Frontend Application: https://___________________.vercel.app
Backend API:         https://___________________.onrender.com
API Documentation:   https://___________________.onrender.com/docs
Database:            [Neon PostgreSQL Dashboard]
```

---

## Security Checklist

- [ ] SECRET_KEY is unique and secure (32+ characters)
- [ ] DATABASE_URL includes `?sslmode=require`
- [ ] CORS_ORIGINS only includes production frontend URL
- [ ] ENVIRONMENT set to "production"
- [ ] .env files NOT committed to Git (.gitignore configured)
- [ ] All sensitive data in environment variables

---

## Performance Checklist

- [ ] Backend responds within 2 seconds (first request)
- [ ] Frontend loads within 3 seconds
- [ ] Database queries optimized
- [ ] Images optimized (if any)
- [ ] No console errors or warnings

---

## Documentation

- [ ] README.md updated with production URLs
- [ ] DEPLOYMENT.md reviewed
- [ ] API documentation accessible at /docs
- [ ] User guides available (if needed)

---

## Rollback Plan

If deployment fails:

1. **Backend Issues:**
   - Check Render logs
   - Verify environment variables
   - Test database connection
   - Roll back to previous deployment in Render

2. **Frontend Issues:**
   - Check Vercel deployment logs
   - Verify environment variables
   - Roll back to previous deployment in Vercel

3. **Database Issues:**
   - Check Neon dashboard for errors
   - Verify connection string
   - Rollback migration: `alembic downgrade -1`

---

## Success Criteria

✅ Deployment is successful when:
- Backend health check returns healthy
- Frontend loads without errors
- Users can register and login
- Users can create, read, update, delete tasks
- User data isolation works
- No CORS errors
- All pages accessible

---

## Cost Summary

**Free Tier:**
- Render Backend: $0/month (sleeps after 15 min)
- Vercel Frontend: $0/month (100GB bandwidth)
- Neon Database: $0/month (0.5GB storage)

**Total: $0/month**

**Paid Tier (Optional):**
- Render Starter: $7/month (no sleep)
- Vercel Pro: $20/month (priority support)
- Neon Scale: $0-$19/month (more storage)

---

## Support Resources

- **Render Status**: https://status.render.com
- **Vercel Status**: https://www.vercel-status.com
- **Neon Status**: https://neonstatus.com
- **Your Guides**: SETUP_GUIDE.md, DEPLOYMENT.md
- **Your Docs**: README.md, PHASE_II_COMPLETE.md

---

## Completion

**Deployment Completed On:** __________________
**Deployed By:** __________________
**Production URL:** __________________
**Status:** ☐ Success  ☐ Issues (see notes)

**Notes:**
____________________________________________
____________________________________________
____________________________________________

---

**✅ Ready to deploy! Follow DEPLOY_NOW.md for step-by-step instructions.**
