# QUICK FIX - Frontend Blank Page Issue

## IMMEDIATE SOLUTION

### Step 1: Check if Frontend is Running

Open **NEW PowerShell window** and run:

```powershell
cd E:\heckathon-2\frontend
npm run dev
```

**Expected Output:**
```
▲ Next.js 14.2.35
- Local:        http://localhost:3000
- ready started server on 0.0.0.0:3000
```

### Step 2: If Frontend Not Running - Install Dependencies

```powershell
cd E:\heckathon-2\frontend
npm install
npm run dev
```

### Step 3: Check Browser Console

1. Open: http://localhost:3000/register
2. Press **F12** (Developer Tools)
3. Check **Console** tab for errors
4. Share any errors you see

### Step 4: Verify Backend Connection

Backend should be running on: http://127.0.0.1:8000

Test it:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing
```

---

## Common Issues & Fixes

### Issue 1: "Cannot find module"
**Fix**: Run `npm install` in frontend folder

### Issue 2: "Port 3000 already in use"
**Fix**: 
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
# Note the PID, then:
taskkill /PID <PID> /F
```

### Issue 3: "Module not found: Can't resolve '@/...'"
**Fix**: Check `tsconfig.json` paths are correct

### Issue 4: Blank page with no errors
**Fix**: Check if `.env.local` exists and has correct values

---

## Create .env.local if Missing

Create file: `E:\heckathon-2\frontend\.env.local`

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

---

## Phase III Status

✅ **Gradio App** - Phase III voice input working
✅ **Agent Integration** - Complete in gradio_app.py
✅ **MCP Tools** - Connected and functional

**For Phase III, use Gradio app:**
```powershell
cd E:\heckathon-2
.\START_GRADIO_APP.bat
```

Then open: http://localhost:7860

---

## Next Steps After Frontend Works

1. Test registration at: http://localhost:3000/register
2. Test login at: http://localhost:3000/login
3. Test dashboard at: http://localhost:3000/dashboard (after login)
4. Test Phase III Gradio app: http://localhost:7860
