# 🚀 Render Backend Deployment - Step by Step

**GitHub Repo**: https://github.com/waqasvicky10/The-Evolution-Of-Todo-App
**Status**: Ready to deploy

---

## 📋 Pre-Deployment Checklist

Before starting, make sure you have:
- [x] GitHub repository pushed (✅ Done!)
- [ ] Neon PostgreSQL connection string
- [ ] Render account (free)

---

## Step 1: Get Neon Database Connection String

### Do This First (5 minutes):

1. **Open**: https://console.neon.tech
2. **Sign up** or **Sign in** (use GitHub for quick auth)
3. **Click**: "Create a project"
   - Name: `todo-app-phase2`
   - Region: Choose closest to you
4. **Click**: "Create project"
5. **On the dashboard**, you'll see "Connection Details"
6. **Select**: "Pooled connection" (dropdown)
7. **Copy** the connection string - it looks like:
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
8. **SAVE THIS** - paste it in a notepad for now

---

## Step 2: Generate SECRET_KEY

Run this command in your terminal:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Copy the output** - it will look like:
```
x1y2z3a4b5c6d7e8f9g0h1i2j3k4l5m6n7o8p9q0r1s2
```

**SAVE THIS** too!

---

## Step 3: Deploy to Render

### 3.1 Create Render Account

1. **Open**: https://render.com
2. **Click**: "Get Started for Free"
3. **Choose**: "Continue with GitHub"
4. **Authorize** Render to access your repositories
5. You'll be taken to the Render Dashboard

### 3.2 Create Web Service

1. **Click**: "New +" button (top right)
2. **Select**: "Web Service"
3. You'll see your repositories listed
4. **Find**: "The-Evolution-Of-Todo-App"
5. **Click**: "Connect"

### 3.3 Configure Your Service

Fill in these settings on the configuration page:

#### Basic Settings:

**Name:**
```
todo-api-phase2
```

**Environment:**
```
Python 3
```

**Region:**
```
Oregon (US West)
```
(Or choose closest to your location)

**Branch:**
```
main
```

**Root Directory:**
```
backend
```

#### Build Settings:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3.4 Add Environment Variables

Scroll down to "Environment Variables" section.

**Click**: "Add Environment Variable"

Add these **7 variables** (one at a time):

---

**Variable 1:**
- Key: `DATABASE_URL`
- Value: [Paste your Neon connection string from Step 1]

---

**Variable 2:**
- Key: `SECRET_KEY`
- Value: [Paste the secret key from Step 2]

---

**Variable 3:**
- Key: `ALGORITHM`
- Value: `HS256`

---

**Variable 4:**
- Key: `ACCESS_TOKEN_EXPIRE_MINUTES`
- Value: `15`

---

**Variable 5:**
- Key: `REFRESH_TOKEN_EXPIRE_DAYS`
- Value: `7`

---

**Variable 6:**
- Key: `CORS_ORIGINS`
- Value: `https://placeholder.vercel.app`
(We'll update this later after deploying frontend)

---

**Variable 7:**
- Key: `ENVIRONMENT`
- Value: `production`

---

### 3.5 Review and Deploy

1. **Scroll down** and review all settings
2. **Click**: "Create Web Service" (blue button at bottom)
3. Render will start building and deploying!

### 3.6 Watch the Deployment

You'll see the build logs in real-time:

```
==> Building...
==> Downloading Python...
==> Installing dependencies...
==> pip install -r requirements.txt
==> Starting service...
==> Your service is live!
```

**This takes about 3-5 minutes.**

### 3.7 Get Your Backend URL

Once deployment is complete:
1. At the top of the page, you'll see your service URL
2. It will be something like:
   ```
   https://todo-api-phase2.onrender.com
   ```
3. **COPY THIS URL** - you need it for the frontend!

---

## Step 4: Run Database Migrations

After the service shows "Live":

1. **On your service page**, look at the left sidebar
2. **Click**: "Shell" tab
3. Wait for the shell to connect (~10 seconds)
4. **Type this command**:
   ```bash
   alembic upgrade head
   ```
5. **Press Enter**

You should see:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, create users and tasks tables
```

✅ **Migrations complete!**

---

## Step 5: Test Your Backend

### Test 1: Health Check

**Open in browser:**
```
https://your-service-name.onrender.com/health
```

**Expected response:**
```json
{"status":"healthy"}
```

### Test 2: Root Endpoint

**Open in browser:**
```
https://your-service-name.onrender.com/
```

**Expected response:**
```json
{
  "message": "Todo API Phase II",
  "version": "2.0.0",
  "status": "running"
}
```

### Test 3: API Documentation

**Open in browser:**
```
https://your-service-name.onrender.com/docs
```

**You should see:** Interactive Swagger UI with all your endpoints!

---

## ✅ Backend Deployment Complete!

Your backend is now live at:
```
https://todo-api-phase2.onrender.com
```
(or your actual URL)

---

## 📊 What You Have Now

- ✅ Backend API deployed and running
- ✅ Database connected (Neon PostgreSQL)
- ✅ Migrations applied (users and tasks tables created)
- ✅ API documentation accessible
- ✅ HTTPS enabled
- ✅ Health check passing

---

## 🚨 Troubleshooting

### Service won't start - Check Logs

1. Go to your service page on Render
2. Click "Logs" tab
3. Look for error messages
4. Common issues:
   - Missing environment variables
   - Wrong DATABASE_URL format
   - Python version mismatch

### Database connection error

Check that:
- DATABASE_URL includes `?sslmode=require`
- Neon database is active (check Neon dashboard)
- Connection string is correct (no typos)

### Migrations failed

Try running again:
1. Go to Shell tab
2. Run: `alembic upgrade head`
3. Check the output for specific errors

### 502/503 Errors

This is normal for free tier:
- Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- Subsequent requests are fast

---

## 📝 Save Your Information

**Backend URL:**
```
https://_____________________________.onrender.com
```

**Database URL:** (stored in Render environment variables)

**SECRET_KEY:** (stored in Render environment variables)

---

## 🎯 Next Steps

Now that backend is deployed, you need to:

1. ✅ Backend deployed to Render - **DONE!**
2. ⏭️ Deploy frontend to Vercel - **NEXT**
3. ⏭️ Update CORS_ORIGINS with Vercel URL
4. ⏭️ Test full integration

**Continue with frontend deployment!**

---

## 💡 Render Free Tier Notes

**What you get:**
- 750 hours/month of runtime
- Automatic HTTPS
- Auto-deploy on git push
- Free SSL certificate

**Limitations:**
- Service sleeps after 15 min of inactivity
- ~30 second cold start on first request
- 512 MB RAM

**To upgrade to always-on ($7/mo):**
1. Go to your service settings
2. Change Instance Type to "Starter"
3. Service will restart and never sleep

---

## 🔄 Redeploying After Code Changes

When you push changes to GitHub:

1. Render automatically detects the push
2. Rebuilds your service
3. Deploys the new version
4. Takes 2-3 minutes

You don't need to do anything!

---

**Backend Deployment Complete!** ✅

**Your API is LIVE at**: https://todo-api-phase2.onrender.com

**Next**: Deploy frontend to Vercel!
