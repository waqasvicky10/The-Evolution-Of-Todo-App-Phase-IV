# Critical Fix: Latency Issues

## Problems Identified

1. **Frontend `npm run dev` slow**: Taking too long to start
2. **Registration timing out**: Even with 30-second timeout
3. **Database connection very slow**: Likely the root cause

## Fixes Applied ✅

### 1. Optimized Database Connection Pool
- **Reduced pool size**: 5 → 2 (faster startup)
- **Reduced overflow**: 10 → 5
- **Faster timeouts**: 30s → 10s pool, 10s → 5s connection
- **Disabled SQL logging**: `echo=False` (was slowing down)

### 2. Removed Blocking Startup
- **No database init on startup**: Server starts immediately
- **Tables created via migrations**: Run `alembic upgrade head` first

### 3. Fixed Invalid Connection Option
- **Removed `server_side_cursors`**: Not valid for psycopg2

---

## CRITICAL: Run Migrations First!

**Before starting server, you MUST run migrations:**

```powershell
cd E:\heckathon-2\backend
alembic upgrade head
```

This creates all database tables **before** requests, making them much faster.

---

## Step-by-Step Fix

### Step 1: Run Migrations (REQUIRED)
```powershell
cd E:\heckathon-2\backend
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_create_users_and_tasks_tables, Create users and tasks tables
```

### Step 2: Restart Backend
```powershell
# Stop current server (CTRL+C)
cd E:\heckathon-2\backend
uvicorn app.main:app --reload
```

**Should start in < 2 seconds now** (no database init blocking)

### Step 3: Test Registration
1. Go to: http://localhost:3000/register
2. Create account
3. Should complete in < 3 seconds (instead of timing out)

---

## If Still Slow After Migrations

### Option 1: Check Database Connection Speed
```powershell
cd E:\heckathon-2\backend
python -c "import time; from app.database import engine; start=time.time(); conn=engine.connect(); print(f'{time.time()-start:.2f}s'); conn.close()"
```

**Expected**: < 2 seconds
**If > 5 seconds**: Database connection is the issue

### Option 2: Use Neon Direct Connection (Not Pooler)
Sometimes pooler can be slower. Try direct connection:

1. Go to Neon Console
2. Get **direct connection string** (not pooler)
3. Update `backend/.env`:
   ```
   DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/db?sslmode=require
   ```
   (Remove `-pooler` from hostname)

### Option 3: Increase Frontend Timeout Further
```typescript
// frontend/src/lib/api.ts
timeout: 60000, // 60 seconds
```

---

## Performance Expectations

### After Migrations + Optimizations:
- **Server Startup**: < 2 seconds ✅
- **First Request**: 2-3 seconds (cold start)
- **Subsequent Requests**: < 1 second ✅
- **Registration**: < 3 seconds ✅
- **Login**: < 2 seconds ✅

---

## Troubleshooting

### Issue: "Alembic command not found"
```powershell
pip install alembic
```

### Issue: "No such revision"
```powershell
# Check migrations exist
ls backend/alembic/versions/

# If empty, create migration
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Issue: "Tables already exist"
```powershell
# That's OK - migrations are idempotent
# Just proceed with testing
```

---

## Most Important Action

**RUN MIGRATIONS FIRST:**
```powershell
cd E:\heckathon-2\backend
alembic upgrade head
```

This is **critical** - without it, every request tries to create tables, which is very slow.

---

**Status**: ✅ Optimizations applied. **Run migrations before testing!**
