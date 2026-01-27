# Fix: Server Hanging on Startup

## Problem
The server starts but hangs and doesn't respond to requests. This is likely because the database connection is blocking during startup.

## Solution

### Step 1: Stop the Current Server
Press `CTRL+C` in the terminal where the server is running.

### Step 2: Check Database Connection
The server might be hanging while trying to connect to Neon PostgreSQL. Let's test the connection:

```powershell
cd E:\heckathon-2\backend
python -c "from app.database import engine; print('Testing connection...'); conn = engine.connect(); print('✅ Connected!'); conn.close()"
```

### Step 3: Make Database Initialization Non-Blocking
I've updated `main.py` to handle database initialization errors gracefully. The server should now start even if there's a database issue.

### Step 4: Restart Server
```powershell
cd E:\heckathon-2\backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 5: Check Server Logs
Look for:
- `[Startup] Initializing database...`
- `[Startup] Database initialized successfully`
- Or any error messages

## Alternative: Skip Database Init on Startup

If the database connection is the problem, you can temporarily skip it:

1. Comment out the `init_db()` call in `main.py`
2. Run migrations manually: `alembic upgrade head`
3. Restart server

## Quick Fix Commands

```powershell
# 1. Stop server (CTRL+C)

# 2. Test database connection
cd E:\heckathon-2\backend
python -c "from app.config import settings; from sqlmodel import create_engine; engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True); conn = engine.connect(); print('✅ DB OK'); conn.close()"

# 3. Restart server
uvicorn app.main:app --reload
```

## Expected Behavior

After the fix, you should see:
- Server starts quickly
- Database connection happens in background
- Server responds to http://127.0.0.1:8000/ immediately
- No hanging/timeout
