# Phase II Deployment Guide

Guide for deploying the Todo App to production environments.

---

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Recommended Platforms](#recommended-platforms)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Setup](#database-setup)
6. [Environment Configuration](#environment-configuration)
7. [Post-Deployment](#post-deployment)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Deployment Overview

### Architecture

```
┌─────────────────┐
│   Users/Clients │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
    ┌────▼─────┐      ┌────▼──────┐
    │ Frontend │      │  Backend  │
    │ (Vercel) │      │  (Render) │
    └──────────┘      └─────┬─────┘
                            │
                      ┌─────▼──────┐
                      │ PostgreSQL │
                      │   (Neon)   │
                      └────────────┘
```

### Components to Deploy

1. **Backend API**: FastAPI application
2. **Frontend**: Next.js application
3. **Database**: PostgreSQL (Neon - already serverless)

---

## Recommended Platforms

### Backend: Render or Railway

**Render** (Recommended)
- ✅ Free tier available
- ✅ Easy Python deployment
- ✅ Automatic HTTPS
- ✅ Health checks
- 🔗 https://render.com

**Railway** (Alternative)
- ✅ Free tier with $5 credit
- ✅ Simple deployment
- ✅ Great developer experience
- 🔗 https://railway.app

### Frontend: Vercel or Netlify

**Vercel** (Recommended)
- ✅ Built by Next.js creators
- ✅ Zero-config deployment
- ✅ Automatic HTTPS and CDN
- ✅ Preview deployments
- 🔗 https://vercel.com

**Netlify** (Alternative)
- ✅ Free tier
- ✅ Easy Next.js support
- ✅ Forms and functions
- 🔗 https://netlify.com

### Database: Neon PostgreSQL

**Neon** (Already configured)
- ✅ Serverless PostgreSQL
- ✅ Free tier (0.5GB storage)
- ✅ Automatic backups
- ✅ No maintenance required
- 🔗 https://neon.tech

---

## Backend Deployment

### Option 1: Deploy to Render

#### Step 1: Prepare Repository

Ensure your code is in a Git repository (GitHub, GitLab, or Bitbucket).

#### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub account
3. Authorize Render to access your repository

#### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure service:

**Basic Settings:**
```yaml
Name: todo-api-phase2
Environment: Python 3
Region: [Choose closest to your users]
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

#### Step 4: Set Environment Variables

Add these environment variables in Render dashboard:

```env
DATABASE_URL=[Your Neon PostgreSQL connection string]
SECRET_KEY=[Generate new secure key]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=https://your-frontend-domain.vercel.app
ENVIRONMENT=production
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Step 5: Deploy

1. Click "Create Web Service"
2. Wait for deployment (3-5 minutes)
3. Note your backend URL: `https://todo-api-phase2.onrender.com`

#### Step 6: Run Migrations

After first deployment:

1. Go to "Shell" tab in Render dashboard
2. Run: `alembic upgrade head`

Or use Render's deploy hook to run migrations automatically.

---

### Option 2: Deploy to Railway

#### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
railway login
```

#### Step 2: Initialize Project

```bash
cd backend
railway init
```

#### Step 3: Configure Railway

Create `railway.json` in backend directory:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### Step 4: Add Environment Variables

```bash
railway variables set DATABASE_URL=[your-connection-string]
railway variables set SECRET_KEY=[your-secret-key]
railway variables set CORS_ORIGINS=https://your-frontend-domain.vercel.app
railway variables set ENVIRONMENT=production
```

#### Step 5: Deploy

```bash
railway up
```

#### Step 6: Run Migrations

```bash
railway run alembic upgrade head
```

---

## Frontend Deployment

### Option 1: Deploy to Vercel

#### Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

#### Step 2: Deploy via Vercel Dashboard

1. Go to https://vercel.com
2. Sign up with GitHub account
3. Click "New Project"
4. Import your repository
5. Configure project:

**Framework Preset:** Next.js
**Root Directory:** frontend
**Build Command:** `npm run build`
**Output Directory:** `.next`

#### Step 3: Set Environment Variables

Add in Vercel dashboard:

```env
NEXT_PUBLIC_API_BASE_URL=https://todo-api-phase2.onrender.com
```

#### Step 4: Deploy

1. Click "Deploy"
2. Wait for deployment (2-3 minutes)
3. Note your frontend URL: `https://your-project.vercel.app`

#### Step 5: Update Backend CORS

Update backend environment variable:
```env
CORS_ORIGINS=https://your-project.vercel.app
```

---

### Option 2: Deploy to Netlify

#### Step 1: Create netlify.toml

In `frontend/` directory:

```toml
[build]
  command = "npm run build"
  publish = ".next"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Step 2: Deploy via Netlify Dashboard

1. Go to https://netlify.com
2. Sign up and click "Add new site"
3. Import from Git
4. Configure:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `.next`

#### Step 3: Set Environment Variables

```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.onrender.com
```

#### Step 4: Deploy

1. Click "Deploy site"
2. Wait for deployment
3. Update backend CORS with Netlify URL

---

## Database Setup

### Neon PostgreSQL (Already Configured)

Your Neon database is already set up. For production:

#### Step 1: Verify Configuration

1. Log in to https://console.neon.tech
2. Check your project and database
3. Copy production connection string

#### Step 2: Enable Connection Pooling (Recommended)

1. Go to your Neon project
2. Navigate to "Connection Details"
3. Use the **pooled connection string** for better performance:
   ```
   postgresql://[user]:[password]@[host]/[database]?sslmode=require&pooler=true
   ```

#### Step 3: Set Up Backups

Neon provides automatic backups. Configure retention:
1. Go to project settings
2. Set backup retention period
3. Enable point-in-time recovery if needed

---

## Environment Configuration

### Production Environment Variables

#### Backend (.env or platform dashboard)

```env
# Database - Use pooled connection for production
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require&pooler=true

# Security - MUST be changed for production
SECRET_KEY=[Generate new 32+ character random string]
ALGORITHM=HS256

# Token expiration
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS - Only include production frontend URL
CORS_ORIGINS=https://your-production-frontend.vercel.app

# Environment
ENVIRONMENT=production
```

#### Frontend (.env.local or platform dashboard)

```env
# Backend API URL - Your production backend
NEXT_PUBLIC_API_BASE_URL=https://your-production-backend.onrender.com
```

---

## Post-Deployment

### Step 1: Run Database Migrations

After first deployment:

**Render:**
```bash
# In Render shell
alembic upgrade head
```

**Railway:**
```bash
railway run alembic upgrade head
```

### Step 2: Test Endpoints

**Health Check:**
```bash
curl https://your-backend-url.onrender.com/health
```

**API Documentation:**
- Visit: `https://your-backend-url.onrender.com/docs`
- Verify all endpoints are documented

### Step 3: Test User Flow

1. Visit your frontend URL
2. Register a new account
3. Login
4. Create, update, and delete tasks
5. Test toggle completion
6. Logout and login again

### Step 4: Verify CORS

1. Open browser developer console
2. Check for CORS errors
3. If errors, update backend `CORS_ORIGINS`

---

## Monitoring and Maintenance

### Backend Monitoring

**Render:**
- Logs: Dashboard → Logs tab
- Metrics: Dashboard → Metrics tab
- Set up email alerts for downtime

**Railway:**
- Logs: Dashboard → Logs
- Metrics: Dashboard → Metrics
- Configure webhooks for notifications

### Frontend Monitoring

**Vercel:**
- Analytics: Dashboard → Analytics
- Logs: Dashboard → Functions logs
- Real-time error tracking

### Database Monitoring

**Neon:**
- Monitoring: Dashboard → Monitoring
- Query performance
- Connection pooling stats
- Storage usage

### Health Checks

Set up automated health checks:

**UptimeRobot** (Free):
1. Go to https://uptimerobot.com
2. Add monitors for:
   - Backend: `https://your-backend-url.onrender.com/health`
   - Frontend: `https://your-frontend-url.vercel.app`
3. Set up email/SMS alerts

---

## Security Checklist

Before going live:

### Backend
- [ ] Changed SECRET_KEY to production value
- [ ] Updated CORS_ORIGINS to only production frontend
- [ ] Environment set to "production"
- [ ] Using HTTPS (automatic with Render/Railway)
- [ ] Database connection uses SSL (Neon default)
- [ ] No sensitive data in logs

### Frontend
- [ ] Using production backend URL
- [ ] HTTPS enabled (automatic with Vercel/Netlify)
- [ ] No API keys in client-side code
- [ ] Environment variables properly set

### Database
- [ ] Using pooled connections
- [ ] Backups configured
- [ ] Access restricted to backend only
- [ ] SSL/TLS enabled

---

## Scaling Considerations

### Backend Scaling

**Vertical Scaling:**
- Upgrade Render/Railway plan for more CPU/RAM
- Suitable for < 1000 concurrent users

**Horizontal Scaling:**
- Enable auto-scaling on Render
- Use load balancer for multiple instances

### Database Scaling

**Neon Autoscaling:**
- Automatically scales compute resources
- Scales to zero when idle (saves cost)
- Upgrade plan for more storage/compute

### Frontend Scaling

**Automatic with Vercel/Netlify:**
- Global CDN distribution
- Automatic edge caching
- Handles millions of requests

---

## Troubleshooting Deployment

### Issue: Build Fails

**Check:**
- All dependencies in requirements.txt/package.json
- Python/Node version compatibility
- Environment variables set correctly

### Issue: Migrations Fail

**Check:**
- DATABASE_URL is correct
- Database is accessible from deployment platform
- SSL mode is set correctly

### Issue: 502/503 Errors

**Check:**
- Backend is running (check logs)
- Start command is correct
- Port binding is correct ($PORT variable)

### Issue: CORS Errors

**Check:**
- CORS_ORIGINS includes frontend URL
- Frontend URL is correct (https, no trailing slash)
- Redeploy backend after CORS changes

---

## Cost Estimation

### Free Tier Setup

**Total: $0/month**
- Backend (Render Free): $0
- Frontend (Vercel Hobby): $0
- Database (Neon Free): $0

**Limitations:**
- Backend sleeps after inactivity (cold starts ~30s)
- Neon: 0.5GB storage, 10M rows
- Vercel: 100GB bandwidth/month

### Recommended Paid Setup

**Total: ~$20/month**
- Backend (Render Starter): $7/month
- Frontend (Vercel Pro): $20/month
- Database (Neon Pro): $0 (free tier sufficient initially)

**Benefits:**
- No cold starts
- Better support
- More bandwidth
- Custom domains included

---

## Deployment Checklist

- [ ] Database created and accessible
- [ ] Backend deployed with correct environment variables
- [ ] Database migrations run successfully
- [ ] Backend health check responds
- [ ] Frontend deployed with correct API URL
- [ ] CORS configured correctly
- [ ] User registration works
- [ ] User login works
- [ ] Task CRUD operations work
- [ ] User isolation verified
- [ ] Monitoring set up
- [ ] Health checks configured
- [ ] SSL/HTTPS enabled everywhere

---

**Deployment Complete!** 🚀

Your Phase II Todo App is now live and accessible to users worldwide.
