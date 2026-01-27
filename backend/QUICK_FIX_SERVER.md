# Quick Fix: Server Hanging on Requests

## Problem
Server starts but hangs/times out when processing requests. This is likely due to slow database connections.

## Solution Applied

I've updated the code to:
1. **Add connection timeouts** - Database connections won't hang indefinitely
2. **Make startup non-blocking** - Server starts immediately, database init happens in background
3. **Add connection pool settings** - Better connection management

## What to Do

### Step 1: Restart the Server

**Stop the current server** (Press `CTRL+C` in the terminal)

**Restart it:**
```powershell
cd E:\heckathon-2\backend
uvicorn app.main:app --reload
```

### Step 2: Test Again

The server should now:
- Start immediately (no hanging)
- Respond to requests quickly
- Handle database connections with timeouts

### Step 3: Check Server Logs

You should see:
- `[Startup] Initializing database...` (in background)
- Server responds to requests immediately
- Database init completes separately

## If Still Hanging

The database connection might be too slow. Try:

### Option 1: Skip Database Init on Startup

Comment out the startup event in `main.py`:
```python
# @app.on_event("startup")
# async def startup_event():
#     ...
```

Then run migrations manually:
```powershell
alembic upgrade head
```

### Option 2: Check Database Connection

Test if you can connect to Neon:
```powershell
cd E:\heckathon-2\backend
python -c "from app.database import engine; conn = engine.connect(); print('Connected!'); conn.close()"
```

If this hangs, the issue is with your Neon connection string or network.

## Expected Behavior After Fix

- ✅ Server starts in < 2 seconds
- ✅ http://127.0.0.1:8000/ responds immediately
- ✅ http://127.0.0.1:8000/health responds immediately
- ✅ http://127.0.0.1:8000/docs loads in browser
- ✅ Database operations work (with timeout protection)
