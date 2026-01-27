# Fix: Frontend Not Loading in Browser

## Problem
http://localhost:3000/register not showing page in browser

## Step-by-Step Troubleshooting

### Step 1: Check if Frontend is Running

Open a terminal and check:

```powershell
# Check if port 3000 is in use
netstat -ano | findstr :3000
```

**If nothing shows**: Frontend is NOT running. Go to Step 2.

**If something shows**: Frontend might be running but has errors. Go to Step 3.

---

### Step 2: Start Frontend Server

```powershell
cd E:\heckathon-2\frontend
npm run dev
```

**Expected Output:**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
```

**If you see errors**, share them and we'll fix.

---

### Step 3: Check for Compilation Errors

Look at the terminal where `npm run dev` is running. Check for:

- ❌ **TypeScript errors**
- ❌ **Module not found errors**
- ❌ **Build failures**

**Common Errors:**

#### Error: "Module not found"
```powershell
cd E:\heckathon-2\frontend
npm install
```

#### Error: "Port 3000 already in use"
```powershell
# Find what's using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Try again
npm run dev
```

---

### Step 4: Check Browser Console

1. Open browser: http://localhost:3000/register
2. Press **F12** to open Developer Tools
3. Check **Console** tab for errors
4. Check **Network** tab for failed requests

**Common Browser Errors:**
- "Failed to load resource" → Backend not running
- "404 Not Found" → Route doesn't exist
- "CORS error" → Backend CORS misconfigured

---

### Step 5: Try Different URLs

Test these URLs in order:

1. **Root**: http://localhost:3000/
   - Should show landing page

2. **Register**: http://localhost:3000/register
   - Should show registration form

3. **Login**: http://localhost:3000/login
   - Should show login form

**If root works but register doesn't**: There's a routing issue.

---

### Step 6: Clear Browser Cache

Sometimes browser cache causes issues:

1. **Chrome/Edge**: Press `CTRL + SHIFT + DELETE`
2. Select "Cached images and files"
3. Click "Clear data"
4. Try again

Or use **Incognito/Private mode**:
- `CTRL + SHIFT + N` (Chrome)
- `CTRL + SHIFT + P` (Firefox)

---

### Step 7: Check Frontend Logs

In the terminal where `npm run dev` is running, look for:

```
✓ Compiled /register in XXXms
```

**If you see errors**, they'll show what's wrong.

---

## Quick Fix Checklist

- [ ] Frontend server is running (`npm run dev`)
- [ ] No errors in terminal
- [ ] Port 3000 is accessible
- [ ] Browser console shows no errors
- [ ] Tried clearing cache
- [ ] Tried incognito mode
- [ ] Backend is running on port 8000

---

## Common Solutions

### Solution 1: Restart Frontend
```powershell
# Stop (CTRL+C)
cd E:\heckathon-2\frontend
npm run dev
```

### Solution 2: Reinstall Dependencies
```powershell
cd E:\heckathon-2\frontend
rm -r node_modules  # or: Remove-Item -Recurse node_modules
npm install
npm run dev
```

### Solution 3: Check File Structure
Make sure these files exist:
- ✅ `frontend/src/app/register/page.tsx`
- ✅ `frontend/src/app/layout.tsx`
- ✅ `frontend/package.json`

---

## If Still Not Working

Share:
1. **Terminal output** from `npm run dev`
2. **Browser console errors** (F12 → Console)
3. **What you see** when visiting http://localhost:3000/register
   - Blank page?
   - Error message?
   - Loading forever?

---

## Expected Behavior

When working correctly:
1. Visit http://localhost:3000/register
2. Should see registration form immediately
3. Form has: Email, Password, Confirm Password fields
4. "Create Account" button at bottom

---

**Next Step**: Check if frontend is running and share any errors you see.
