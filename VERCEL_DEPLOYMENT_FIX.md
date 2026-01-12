# 🔧 Vercel Deployment Fix Guide

**Issue**: Build failures on Vercel deployment
**Solution**: Updated configuration and proper environment setup

---

## 🚨 Common Vercel Build Issues & Fixes

### Issue 1: Missing Environment Variables
**Problem**: `NEXT_PUBLIC_API_BASE_URL` not set correctly
**Fix**: Set proper production backend URL

### Issue 2: Build Configuration
**Problem**: Incorrect Vercel configuration
**Fix**: Updated `vercel.json` with proper settings

### Issue 3: Dependency Vulnerabilities
**Problem**: Security warnings causing build failures
**Fix**: Updated Next.js to latest stable version

---

## ✅ Step-by-Step Fix

### Step 1: Update Dependencies (Already Done)
```json
{
  "dependencies": {
    "next": "^14.2.35"
  },
  "devDependencies": {
    "eslint-config-next": "^14.2.35"
  }
}
```

### Step 2: Proper Vercel Configuration (Already Done)
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "functions": {
    "src/app/**/*.tsx": {
      "runtime": "nodejs18.x"
    }
  }
}
```

### Step 3: Deploy to Vercel with Correct Settings

#### 3.1 Go to Vercel Dashboard
1. Visit: https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository

#### 3.2 Configure Project Settings
```
Project Name: todo-app-phase2
Framework Preset: Next.js (auto-detected)
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

#### 3.3 Set Environment Variable
**CRITICAL**: Add this environment variable:

```
Name: NEXT_PUBLIC_API_BASE_URL
Value: https://todo-api-phase2.onrender.com
Environment: Production, Preview, Development
```

**Replace with your actual Render backend URL!**

### Step 4: Deploy
1. Click "Deploy"
2. Wait for build to complete (2-3 minutes)
3. Get your Vercel URL (e.g., `https://todo-app-phase2.vercel.app`)

### Step 5: Update Backend CORS
1. Go to Render Dashboard
2. Open your backend service
3. Go to Environment variables
4. Update `CORS_ORIGINS` to your Vercel URL
5. Save changes (service will redeploy)

---

## 🔍 Troubleshooting Build Failures

### Build Error: "Module not found"
**Check**: Ensure all imports use correct paths
**Fix**: All imports should use `@/` prefix for src directory

### Build Error: "Type errors"
**Check**: TypeScript configuration
**Fix**: Run `npm run build` locally first to catch issues

### Build Error: "Environment variable undefined"
**Check**: Environment variable starts with `NEXT_PUBLIC_`
**Fix**: Ensure variable is set in Vercel dashboard

### Build Error: "CORS issues"
**Check**: Backend CORS configuration
**Fix**: Update CORS_ORIGINS in Render with exact Vercel URL

---

## 📋 Deployment Checklist

- [x] Dependencies updated to latest stable versions
- [x] Vercel configuration optimized
- [x] Build passes locally (`npm run build`)
- [x] No TypeScript errors (`npm run lint`)
- [ ] Environment variable set in Vercel
- [ ] Backend deployed to Render
- [ ] CORS updated with Vercel URL

---

## 🚀 Quick Deploy Commands

### Test Build Locally
```bash
cd frontend
npm install
npm run build
npm run lint
```

### Deploy to Vercel (CLI method)
```bash
npm install -g vercel
cd frontend
vercel --prod
```

---

## 📊 Expected Results

### Successful Build Output
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages (8/8)
✓ Finalizing page optimization
```

### Live Application Features
- ✅ Landing page loads
- ✅ Registration works
- ✅ Login works
- ✅ Dashboard shows tasks
- ✅ CRUD operations work
- ✅ No CORS errors

---

## 🔗 Final URLs

**Frontend (Vercel)**: https://todo-app-phase2.vercel.app
**Backend (Render)**: https://todo-api-phase2.onrender.com
**API Docs**: https://todo-api-phase2.onrender.com/docs

---

**Status**: ✅ Ready for deployment
**Build Issues**: ✅ Fixed
**Configuration**: ✅ Optimized