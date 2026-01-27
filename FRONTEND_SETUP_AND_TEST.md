# Frontend Setup and Testing Guide

## Step 1: Install Dependencies

```powershell
cd E:\heckathon-2\frontend
npm install
```

This will install:
- Next.js
- React
- Axios
- Better Auth packages
- Tailwind CSS
- All other dependencies

---

## Step 2: Verify Environment Variables

Check `frontend/.env.local` exists and has:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

If missing, create it:
```powershell
cd E:\heckathon-2\frontend
copy .env.local.example .env.local
# Then edit .env.local and set NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## Step 3: Start Frontend Server

```powershell
cd E:\heckathon-2\frontend
npm run dev
```

Frontend will start on: **http://localhost:3000**

---

## Step 4: Test Login Page

1. **Open browser**: http://localhost:3000/login

2. **Test Registration First** (if no account):
   - Go to: http://localhost:3000/register
   - Create account with:
     - Email: test@example.com
     - Password: Test123!@#
     - Confirm Password: Test123!@#

3. **Test Login**:
   - Go to: http://localhost:3000/login
   - Enter credentials
   - Should redirect to dashboard

---

## Step 5: Test Dashboard

After login, you should see:
- Dashboard page at http://localhost:3000/dashboard
- Task list (empty initially)
- Create task button
- Task management features

---

## Troubleshooting

### Issue: "Module not found"
**Solution**: Run `npm install` in frontend directory

### Issue: "Cannot connect to API"
**Solution**: 
- Make sure backend is running on http://localhost:8000
- Check `NEXT_PUBLIC_API_BASE_URL` in `.env.local`

### Issue: "Login fails"
**Solution**:
- Check backend is running
- Check backend logs for errors
- Verify database connection

### Issue: "Page not loading"
**Solution**:
- Check browser console (F12) for errors
- Check terminal for frontend errors
- Verify port 3000 is not in use

---

## Expected Flow

1. ✅ Frontend starts on port 3000
2. ✅ Login page loads
3. ✅ Registration works
4. ✅ Login works
5. ✅ Dashboard loads
6. ✅ Tasks can be created/viewed/updated/deleted

---

## Performance Testing

After everything works, we'll:
1. Test response times
2. Optimize database queries
3. Add connection pooling
4. Improve error handling
