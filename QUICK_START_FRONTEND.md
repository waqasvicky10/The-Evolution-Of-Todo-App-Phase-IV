# Quick Start: Frontend Server

## Problem
Frontend page not showing in browser at http://localhost:3000/register

## Solution

### Option 1: Use Batch File (Easiest)

Double-click: `frontend/START_FRONTEND.bat`

This will:
- Check dependencies
- Install if needed
- Start the server
- Show you the URL

---

### Option 2: Manual Start

**Step 1: Open Terminal**
```powershell
cd E:\heckathon-2\frontend
```

**Step 2: Check Dependencies**
```powershell
# If node_modules doesn't exist or is incomplete
npm install
```

**Step 3: Start Server**
```powershell
npm run dev
```

**Expected Output:**
```
▲ Next.js 14.2.35
- Local:        http://localhost:3000
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## Verify It's Working

### Test 1: Root Page
Open browser: http://localhost:3000/
- Should show landing page with "Todo App" title

### Test 2: Register Page
Open browser: http://localhost:3000/register
- Should show registration form

### Test 3: Login Page
Open browser: http://localhost:3000/login
- Should show login form

---

## If Page Still Not Showing

### Check 1: Is Server Running?
Look at terminal - should see:
```
✓ Compiled /register in XXXms
```

### Check 2: Browser Console (F12)
1. Open http://localhost:3000/register
2. Press F12
3. Check Console tab for errors
4. Check Network tab for failed requests

### Check 3: Port Conflict
```powershell
# Check if port 3000 is in use
netstat -ano | findstr :3000

# If something is using it, kill it:
taskkill /PID <PID> /F
```

### Check 4: Try Different Browser
- Chrome
- Firefox
- Edge
- Or use Incognito/Private mode

---

## Common Errors

### Error: "Port 3000 already in use"
**Fix**: Kill the process using port 3000, or use different port:
```powershell
npm run dev -- -p 3001
```
Then visit: http://localhost:3001/register

### Error: "Module not found"
**Fix**: 
```powershell
cd E:\heckathon-2\frontend
npm install
```

### Error: "Cannot find module"
**Fix**: 
```powershell
cd E:\heckathon-2\frontend
rm -r node_modules
npm install
```

### Blank Page / Nothing Shows
**Possible Causes**:
1. Server not running - Check terminal
2. Compilation error - Check terminal for errors
3. Browser cache - Clear cache or use incognito
4. JavaScript error - Check browser console (F12)

---

## Expected Terminal Output

When working correctly, you should see:

```
▲ Next.js 14.2.35
- Local:        http://localhost:3000

✓ Ready in 2.5s
○ Compiling /register ...
✓ Compiled /register in 500ms
```

---

## Next Steps After Frontend Starts

1. ✅ Frontend running on http://localhost:3000
2. ✅ Test register page: http://localhost:3000/register
3. ✅ Create account
4. ✅ Test login: http://localhost:3000/login
5. ✅ Test dashboard: http://localhost:3000/dashboard

---

## Still Not Working?

Share:
1. **Terminal output** (copy/paste from `npm run dev`)
2. **Browser console errors** (F12 → Console tab)
3. **What you see** when visiting the URL
   - Blank white page?
   - Error message?
   - Loading spinner forever?

---

**Quick Fix**: Run `frontend/START_FRONTEND.bat` and check terminal output!
