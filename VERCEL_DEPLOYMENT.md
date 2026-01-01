# 🎨 Vercel Frontend Deployment - Step by Step

**GitHub Repo**: https://github.com/waqasvicky10/The-Evolution-Of-Todo-App
**Status**: Ready to deploy

---

## 📋 Pre-Deployment Checklist

Before starting, make sure you have:
- [x] GitHub repository pushed (✅ Done!)
- [x] Backend deployed to Render (✅ You should have your backend URL)
- [ ] Vercel account (free)

---

## Step 1: Prepare Backend URL

You need your Render backend URL from the previous deployment.

**It should look like:**
```
https://todo-api-phase2.onrender.com
```

**If you don't have it:**
1. Go to https://dashboard.render.com
2. Click on your service
3. Copy the URL at the top of the page

**SAVE THIS URL** - you'll need it in Step 3.4

---

## Step 2: Deploy to Vercel

### 2.1 Create Vercel Account

1. **Open**: https://vercel.com
2. **Click**: "Start Deploying" or "Sign Up"
3. **Choose**: "Continue with GitHub"
4. **Authorize** Vercel to access your repositories
5. You'll be taken to the Vercel Dashboard

### 2.2 Import Your Project

1. **Click**: "Add New..." button (top right)
2. **Select**: "Project"
3. You'll see a list of your GitHub repositories
4. **Find**: "The-Evolution-Of-Todo-App"
5. **Click**: "Import"

**If you don't see your repository:**
- Click "Adjust GitHub App Permissions"
- Select "All repositories" or choose specific repo
- Save and return to import page

### 2.3 Configure Project Settings

You'll see a configuration page. Fill in these settings:

#### Project Configuration:

**Project Name:**
```
todo-app-phase2
```
(Or choose your own name - this becomes part of your URL)

**Framework Preset:**
```
Next.js
```
(Should auto-detect)

**Root Directory:**
- **Click**: "Edit" button next to Root Directory
- **Select**: `frontend` from the dropdown
- **Click**: "Continue"

**Build and Output Settings:**
- Build Command: `npm run build` (default - leave it)
- Output Directory: `.next` (default - leave it)
- Install Command: `npm install` (default - leave it)

### 2.4 Add Environment Variable

**IMPORTANT**: You must add this before deploying!

**Scroll down** to "Environment Variables" section

**Click**: "Add" or expand the section

Add this variable:

**Name (Key):**
```
NEXT_PUBLIC_API_BASE_URL
```

**Value:**
```
https://todo-api-phase2.onrender.com
```
**REPLACE WITH YOUR ACTUAL RENDER URL** from your backend deployment!

**Environment:** All (Production, Preview, Development) - leave checked

### 2.5 Deploy Frontend

1. **Review** all settings one more time
2. **Click**: "Deploy" button (blue button at bottom)
3. Vercel will start building!

### 2.6 Watch the Deployment

You'll see real-time build logs:

```
Running "npm install"...
Running "npm run build"...
Collecting page data...
Generating static pages...
Creating optimized production build...
Build completed successfully!
Deploying...
Deployment completed!
```

**This takes about 2-3 minutes.**

### 2.7 Get Your Frontend URL

Once deployment is complete:

1. You'll see a **"Congratulations!"** page
2. Your app URL will be shown prominently:
   ```
   https://todo-app-phase2.vercel.app
   ```
   (Or something similar based on your project name)

3. **Click**: "Visit" to see your app live!
4. **COPY THIS URL** - you need it to update backend CORS!

---

## Step 3: Test Your Frontend

### Test 1: Homepage

**Open your Vercel URL in browser**

You should see:
- ✅ Landing page with "Todo App" title
- ✅ "Phase II - Full-Stack Web Application" subtitle
- ✅ Three feature cards (Secure, Persistent, Multi-User)
- ✅ "Get Started" and "Sign In" buttons

### Test 2: Pages Load

Try accessing each page:

**Register Page:**
```
https://your-app.vercel.app/register
```
Should show registration form

**Login Page:**
```
https://your-app.vercel.app/login
```
Should show login form

---

## Step 4: Update Backend CORS

**CRITICAL**: Now you need to tell your backend to accept requests from your frontend!

### 4.1 Go to Render Dashboard

1. **Open**: https://dashboard.render.com
2. **Click**: on your "todo-api-phase2" service
3. **Click**: "Environment" in the left sidebar

### 4.2 Update CORS_ORIGINS

1. **Find**: The `CORS_ORIGINS` variable in the list
2. **Click**: The pencil icon (Edit) next to it
3. **Replace** the value with YOUR Vercel URL:
   ```
   https://todo-app-phase2.vercel.app
   ```
   (Use your actual Vercel URL!)

4. **Click**: "Save Changes"

### 4.3 Wait for Redeploy

- Render will automatically redeploy your backend (1-2 minutes)
- Wait until the service shows "Live" again
- **IMPORTANT**: Don't test until this completes!

---

## Step 5: Test Full Integration

Now test that frontend and backend work together!

### 5.1 Open Your App

**Visit**: Your Vercel URL (e.g., https://todo-app-phase2.vercel.app)

### 5.2 Register a New Account

1. **Click**: "Get Started" button
2. **Fill in**:
   - Email: your-email@example.com
   - Password: TestPass123!
   - Confirm Password: TestPass123!
3. **Click**: "Create Account"
4. Should redirect to **Dashboard** automatically!

### 5.3 Test Task Management

**Create a Task:**
1. Type in the task input: "Test my production app"
2. Click "Add Task"
3. Task should appear in the "Active Tasks" section

**Toggle Completion:**
1. Click the checkbox next to your task
2. Task should move to "Completed Tasks" section
3. Task should show with strikethrough

**Edit Task:**
1. Click "Edit" button
2. Change description
3. Click "Save"
4. Description should update

**Delete Task:**
1. Click "Delete" button
2. Confirm deletion
3. Task should disappear

**Logout and Login:**
1. Click "Logout" button
2. Login again with same credentials
3. Your tasks should still be there (persistence!)

### 5.4 Check Browser Console

**IMPORTANT**: Check for errors!

1. Press **F12** to open Developer Tools
2. Click **"Console"** tab
3. Look for errors:
   - ❌ Red errors = something wrong
   - ✅ No red errors = working perfectly!

**Common issues:**
- CORS errors → Backend CORS_ORIGINS not updated yet
- 401 errors → Authentication issue
- Network errors → Backend URL wrong in environment variable

---

## ✅ Frontend Deployment Complete!

Your frontend is now live at:
```
https://todo-app-phase2.vercel.app
```
(or your actual URL)

---

## 📊 What You Have Now

- ✅ Frontend deployed on Vercel
- ✅ Backend deployed on Render
- ✅ Database on Neon
- ✅ CORS configured
- ✅ HTTPS everywhere
- ✅ Full authentication working
- ✅ Task management working
- ✅ Auto-deployments enabled

---

## 🚨 Troubleshooting

### CORS Errors in Browser Console

**Error message:** "blocked by CORS policy"

**Solution:**
1. Verify CORS_ORIGINS in Render matches your Vercel URL **exactly**
2. Must be `https://` (not `http://`)
3. No trailing slash
4. Wait 1-2 minutes after updating for backend to redeploy
5. Clear browser cache and try again (Ctrl+Shift+R)

### Frontend Shows but Can't Register/Login

**Check:**
1. NEXT_PUBLIC_API_BASE_URL in Vercel environment variables
2. Backend URL is correct and includes `https://`
3. Backend is responding (test /health endpoint)
4. Browser console for specific errors

### Build Failed on Vercel

**Check:**
1. Vercel deployment logs for specific error
2. Ensure Root Directory is set to `frontend`
3. Check package.json is valid
4. Redeploy from Vercel dashboard

### "Network Error" when trying to register

**Check:**
1. Backend is running (visit /health endpoint)
2. CORS is configured correctly
3. Frontend has correct API URL
4. Browser isn't blocking requests

---

## 🔄 Making Updates

### Update Frontend Code

```bash
# Make changes to frontend code
cd E:\heckathon-2\frontend
# Edit files...

# Commit and push
cd E:\heckathon-2
git add .
git commit -m "Update frontend"
git push origin main
```

Vercel will automatically:
- Detect the push
- Build your frontend
- Deploy new version
- Takes 2-3 minutes

### Update Environment Variables

**In Vercel:**
1. Go to Project Settings → Environment Variables
2. Update the variable
3. Redeploy (Vercel → Deployments → ... menu → Redeploy)

---

## 🎨 Vercel Features You Get

### Free Tier Includes:
- ✅ Unlimited deployments
- ✅ Automatic HTTPS/SSL
- ✅ Global CDN
- ✅ 100GB bandwidth per month
- ✅ Preview deployments for pull requests
- ✅ Analytics dashboard
- ✅ Custom domain support

### Dashboard Features:
- **Deployments**: See all your deployments and preview URLs
- **Analytics**: View page views and traffic
- **Domains**: Add custom domains
- **Settings**: Manage environment variables

---

## 📊 Deployment Summary

**Repository:**
```
https://github.com/waqasvicky10/The-Evolution-Of-Todo-App
```

**Frontend (Vercel):**
```
https://todo-app-phase2.vercel.app
```

**Backend (Render):**
```
https://todo-api-phase2.onrender.com
```

**API Documentation:**
```
https://todo-api-phase2.onrender.com/docs
```

---

## 💡 Next Steps

### Share Your App:
```
🚀 Check out my Todo App!

App: https://todo-app-phase2.vercel.app
API: https://todo-api-phase2.onrender.com/docs
GitHub: https://github.com/waqasvicky10/The-Evolution-Of-Todo-App

Built with Next.js, FastAPI, and PostgreSQL!
```

### Monitor Your App:
- Vercel: https://vercel.com/dashboard
- Render: https://dashboard.render.com
- Neon: https://console.neon.tech

### Add Custom Domain:
- Follow steps in DEPLOYMENT.md
- Update CORS after adding domain

---

## ✅ Frontend Deployment Complete!

**Your Phase II Todo App is LIVE on the internet!** 🌍

**Frontend**: https://todo-app-phase2.vercel.app
**Backend**: https://todo-api-phase2.onrender.com

**Total Cost**: $0/month ✨

---

**Next**: Test your app thoroughly and share it with the world! 🎉
