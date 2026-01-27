# Start Frontend - Quick Guide

## Prerequisites

✅ Backend server running on http://localhost:8000
✅ Frontend dependencies installed (`npm install` completed)

---

## Step 1: Start Frontend

Open a **new terminal** and run:

```powershell
cd E:\heckathon-2\frontend
npm run dev
```

**Expected Output:**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
```

---

## Step 2: Open Browser

Visit: **http://localhost:3000**

You should see the landing page.

---

## Step 3: Test Login Flow

### Option A: Register New User

1. Click "Register" or go to: http://localhost:3000/register
2. Fill in:
   - Email: `test@example.com`
   - Password: `Test123!@#`
   - Confirm Password: `Test123!@#`
3. Click "Create Account"
4. Should redirect to dashboard

### Option B: Login (if user exists)

1. Go to: http://localhost:3000/login
2. Enter credentials
3. Click "Sign In"
4. Should redirect to dashboard

---

## Step 4: Test Dashboard

After login, you should see:
- Dashboard at http://localhost:3000/dashboard
- "Create Task" button
- Task list (empty initially)
- Navigation bar

---

## Troubleshooting

### Frontend won't start
```powershell
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill process if needed (replace PID)
taskkill /PID <PID> /F

# Try again
npm run dev
```

### "Cannot connect to API"
- Make sure backend is running: http://localhost:8000
- Check `frontend/.env.local` has: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`

### "Module not found"
```powershell
cd E:\heckathon-2\frontend
npm install
```

### Login/Registration fails
- Check backend terminal for errors
- Check browser console (F12) for errors
- Verify database connection in backend

---

## Performance Issues

If login/requests are slow:

1. **Backend Performance**: Database queries are slow (1-2 seconds)
   - This is normal for Neon PostgreSQL cold starts
   - Connection pooling will help after first request

2. **Frontend Timeout**: If requests timeout:
   - Increase timeout in `frontend/src/lib/api.ts`
   - Check backend is responding

---

## Next Steps After Frontend Works

1. ✅ Test all pages (Login, Register, Dashboard)
2. ✅ Test task CRUD operations
3. ✅ Address performance issues
4. ✅ Verify Phase III completion
5. ✅ Then proceed to Phase IV

---

## Quick Test Checklist

- [ ] Frontend starts on port 3000
- [ ] Landing page loads
- [ ] Register page works
- [ ] Login page works
- [ ] Dashboard loads after login
- [ ] Can create tasks
- [ ] Can view tasks
- [ ] Can update tasks
- [ ] Can delete tasks
- [ ] Can toggle task completion

---

**Ready to start? Run: `cd E:\heckathon-2\frontend && npm run dev`**
