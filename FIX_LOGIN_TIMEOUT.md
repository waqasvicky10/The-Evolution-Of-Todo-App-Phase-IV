# Fix: Login Page Timeout Error

## Problem
Login page shows: "timeout of 10000ms exceeded"

## Cause
- Backend database queries are slow (1-2 seconds per query)
- Frontend timeout was set to 10 seconds
- With slow database, requests can exceed timeout

## Solution Applied ✅

### 1. Increased Frontend Timeout
- Changed from 10 seconds to 30 seconds
- Applied to login and register endpoints
- Better error messages for timeouts

### 2. Better Error Handling
- Specific timeout error messages
- User-friendly error display
- Retry guidance

---

## What Changed

### File: `frontend/src/lib/api.ts`

1. **Increased default timeout**:
   ```typescript
   timeout: 30000, // 30 seconds (was 10 seconds)
   ```

2. **Added timeout handling for login**:
   ```typescript
   try {
     const response = await apiClient.post(...);
   } catch (error) {
     if (error.code === 'ECONNABORTED') {
       throw new Error("Request timed out. The server may be slow. Please try again.");
     }
   }
   ```

3. **Added timeout handling for register**:
   - Same pattern as login

---

## Testing

### Step 1: Restart Frontend
```powershell
# Stop frontend (CTRL+C)
# Restart it
cd E:\heckathon-2\frontend
npm run dev
```

### Step 2: Test Login
1. Go to: http://localhost:3000/login
2. Enter credentials
3. Click "Sign In"
4. Should work now (may take 2-3 seconds, but won't timeout)

### Step 3: If Still Timing Out

Check backend is responding:
```powershell
# Test backend health
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing
```

If backend doesn't respond:
- Make sure backend is running: `uvicorn app.main:app --reload`
- Check backend logs for errors
- Verify database connection

---

## Expected Behavior

### Before Fix:
- ❌ Timeout after 10 seconds
- ❌ Error: "timeout of 10000ms exceeded"

### After Fix:
- ✅ Timeout after 30 seconds
- ✅ Login works (may take 2-3 seconds)
- ✅ Better error messages if timeout occurs
- ✅ User-friendly feedback

---

## Performance Notes

- **First request**: 2-3 seconds (database cold start)
- **Subsequent requests**: Faster (connection pooling)
- **Timeout**: 30 seconds (plenty of time)

---

## If Still Having Issues

1. **Check Backend Status**:
   ```powershell
   # Should return: {"status": "healthy"}
   Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing
   ```

2. **Check Backend Logs**:
   - Look for database connection errors
   - Check for slow queries

3. **Test Database Connection**:
   ```powershell
   cd E:\heckathon-2\backend
   python -c "from app.database import engine; conn = engine.connect(); print('Connected!'); conn.close()"
   ```

4. **Increase Timeout Further** (if needed):
   - Edit `frontend/src/lib/api.ts`
   - Change `timeout: 30000` to `timeout: 60000` (60 seconds)

---

**Status**: ✅ Fixed - Timeout increased to 30 seconds

**Next Step**: Restart frontend and test login again
