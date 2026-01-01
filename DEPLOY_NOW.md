# Deploy Todo App to Production - Quick Guide

**Status**: Ready to deploy
**Estimated Time**: 20-30 minutes
**Cost**: $0 (using free tiers)

---

## 🎯 Deployment Plan

We'll deploy to:
- **Backend**: Render (free tier)
- **Frontend**: Vercel (free tier)
- **Database**: Neon PostgreSQL (already serverless, free tier)

---

## Step 1: Prepare Database (5 minutes)

### Get Your Neon Connection String

1. Go to https://console.neon.tech
2. Sign in or create account
3. Create a new project (if you haven't already)
4. Go to "Connection Details"
5. Copy the **pooled connection string** (looks like):
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```
6. **Save this** - you'll need it for backend deployment

---

## Step 2: Prepare Git Repository (5 minutes)

Your code needs to be in a Git repository (GitHub, GitLab, or Bitbucket).

### If you don't have a Git repo yet:

```bash
cd E:\heckathon-2

# Initialize git (if not already done)
git init

# Create .gitignore if not exists
echo "node_modules/
.env
.env.local
__pycache__/
*.pyc
.pytest_cache/
.coverage
venv/
.next/
dist/
build/" > .gitignore

# Add all files
git add .

# Commit
git commit -m "Phase II - Complete Todo App Implementation"

# Create GitHub repository at https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy Backend to Render (10 minutes)

### 3.1 Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### 3.2 Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure:

**Basic Settings:**
```
Name: todo-api-phase2
Environment: Python 3
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: backend
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3.3 Set Environment Variables

Click "Environment" and add these variables:

```env
DATABASE_URL=[YOUR_NEON_CONNECTION_STRING]
SECRET_KEY=[Generate new - see below]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=https://your-app-name.vercel.app
ENVIRONMENT=production
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy the output and paste as SECRET_KEY.

**Note**: You'll update `CORS_ORIGINS` with your actual Vercel URL later.

### 3.4 Deploy

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Your backend URL will be: `https://todo-api-phase2.onrender.com`
4. **Save this URL** - you'll need it for frontend

### 3.5 Run Database Migrations

After deployment completes:

1. Go to your service dashboard
2. Click **"Shell"** tab (left sidebar)
3. Wait for shell to connect
4. Run:
   ```bash
   alembic upgrade head
   ```
5. You should see: `Running upgrade -> 001, create users and tasks tables`

---

## Step 4: Deploy Frontend to Vercel (5 minutes)

### 4.1 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub (recommended)
3. Authorize Vercel

### 4.2 Import Project

1. Click **"Add New..."** → **"Project"**
2. Import your Git repository
3. Configure:

**Framework Preset:** Next.js
**Root Directory:** `frontend`
**Build Command:** `npm run build` (default)
**Output Directory:** `.next` (default)
**Install Command:** `npm install` (default)

### 4.3 Set Environment Variable

Click "Environment Variables" and add:

```env
Name: NEXT_PUBLIC_API_BASE_URL
Value: https://todo-api-phase2.onrender.com
```

(Use your actual Render backend URL from Step 3.4)

### 4.4 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Your frontend URL will be: `https://your-project-name.vercel.app`
4. **Save this URL**

---

## Step 5: Update Backend CORS (2 minutes)

Now that you have your Vercel URL, update backend CORS:

1. Go back to Render dashboard
2. Go to your web service
3. Click **"Environment"**
4. Update `CORS_ORIGINS`:
   ```
   https://your-project-name.vercel.app
   ```
5. Click **"Save Changes"**
6. Service will automatically redeploy (1-2 minutes)

---

## Step 6: Verify Deployment (5 minutes)

### Test Backend

Visit your backend URL:
```
https://todo-api-phase2.onrender.com/health
```

Should return: `{"status":"healthy"}`

Check API docs:
```
https://todo-api-phase2.onrender.com/docs
```

### Test Frontend

Visit your frontend URL:
```
https://your-project-name.vercel.app
```

You should see the landing page!

### Test Complete Flow

1. Click "Get Started" → Register
2. Create account with email/password
3. Login
4. Create a task
5. Toggle completion
6. Update task
7. Delete task

---

## 🎉 Deployment Complete!

Your app is now live at:
- **Frontend**: https://your-project-name.vercel.app
- **Backend**: https://todo-api-phase2.onrender.com
- **API Docs**: https://todo-api-phase2.onrender.com/docs

---

## 📊 Post-Deployment Checklist

- [ ] Backend health check returns "healthy"
- [ ] API documentation accessible
- [ ] Frontend landing page loads
- [ ] Can register new account
- [ ] Can login
- [ ] Can create tasks
- [ ] Can view tasks
- [ ] Can update tasks
- [ ] Can delete tasks
- [ ] Can toggle task completion
- [ ] User data isolation works (can't see other users' tasks)
- [ ] No CORS errors in browser console

---

## 🔧 Monitoring & Maintenance

### Render (Backend)
- **Dashboard**: https://dashboard.render.com
- **View Logs**: Dashboard → Your Service → Logs
- **Metrics**: Dashboard → Your Service → Metrics
- **Free Tier Note**: Service sleeps after 15 min of inactivity (cold start ~30s)

### Vercel (Frontend)
- **Dashboard**: https://vercel.com/dashboard
- **View Deployments**: Dashboard → Your Project → Deployments
- **Analytics**: Dashboard → Your Project → Analytics
- **Free Tier**: Unlimited deployments, 100GB bandwidth/month

### Neon (Database)
- **Dashboard**: https://console.neon.tech
- **Monitoring**: Dashboard → Your Project → Monitoring
- **Free Tier**: 0.5GB storage, autoscaling compute, 10M rows

---

## 🚨 Troubleshooting

### Backend not starting
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure DATABASE_URL is correct
- Check Python version (should be 3.12+)

### CORS errors
- Verify CORS_ORIGINS in Render includes exact Vercel URL
- No trailing slash in URL
- Must use https:// (not http://)
- Redeploy backend after changing CORS

### Frontend can't reach backend
- Check NEXT_PUBLIC_API_BASE_URL in Vercel
- Verify backend URL is correct and live
- Test backend health check manually

### Database connection issues
- Verify DATABASE_URL is correct
- Ensure connection string includes ?sslmode=require
- Check Neon database is active
- Run migrations: `alembic upgrade head` in Render shell

### 502/503 errors
- Backend might be starting up (first request after sleep)
- Wait 30 seconds and try again
- Check Render logs for errors

---

## 💡 Quick Tips

### Custom Domain (Optional)
**Vercel:**
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as shown

**Render:**
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records

### Environment Variables
**To update:**
1. Change in platform dashboard (Render/Vercel)
2. Service auto-redeploys with new values

### Scaling
**Free Tier Limitations:**
- Backend sleeps after 15 min inactivity
- First request has ~30s cold start
- Upgrade to paid tier ($7/month) for always-on

**To Upgrade:**
- Render: Dashboard → Instance Type → Starter ($7/mo)
- Vercel: Dashboard → Upgrade → Pro ($20/mo)

---

## 📈 Next Steps

### Add Features
- Email verification
- Password reset
- Task categories/tags
- Due dates
- Task priorities

### Monitoring
- Set up Uptime monitoring (UptimeRobot)
- Configure error tracking (Sentry)
- Set up analytics (PostHog, Plausible)

### Security
- Enable rate limiting
- Add input sanitization
- Set up security headers
- Configure CSP (Content Security Policy)

---

## 🎊 Congratulations!

Your Phase II Todo App is now **LIVE IN PRODUCTION**!

Share your app:
```
🚀 My Todo App (Phase II)
Frontend: https://your-project-name.vercel.app
API Docs: https://todo-api-phase2.onrender.com/docs

Built with Next.js, FastAPI, PostgreSQL, and deployed on Vercel + Render!
```

---

**Total Cost**: $0/month (free tiers)
**Deployment Time**: ~30 minutes
**Status**: Production Ready ✅

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Neon Docs**: https://neon.tech/docs
- **Your Setup Guide**: SETUP_GUIDE.md
- **Your Deployment Guide**: DEPLOYMENT.md
