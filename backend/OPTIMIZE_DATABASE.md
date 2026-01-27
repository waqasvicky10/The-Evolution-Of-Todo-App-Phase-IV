# Database Performance Optimization

## Issues Identified

1. **Slow Server Startup**: Database initialization blocking startup
2. **Slow Registration/Login**: Database queries taking 30+ seconds
3. **Connection Pool Too Large**: Causing slow initial connections

## Optimizations Applied ✅

### 1. Faster Server Startup
- **Removed blocking database init** on startup
- Server starts immediately
- Tables should be created via migrations: `alembic upgrade head`

### 2. Optimized Connection Pool
- **Reduced pool size**: 5 → 2 (faster startup)
- **Reduced overflow**: 10 → 5
- **Faster timeout**: 30s → 10s
- **Connection timeout**: 10s → 5s

### 3. Disabled SQL Logging
- **echo=False**: No SQL query logging (was slowing down)
- Faster request processing

### 4. Connection Recycling
- **pool_recycle=3600**: Recycle connections after 1 hour
- Prevents stale connections

---

## Critical: Run Migrations First

**Before starting server, run migrations:**

```powershell
cd E:\heckathon-2\backend
alembic upgrade head
```

This creates all tables **before** the server starts, so requests are fast.

---

## If Still Slow: Use Neon Pooler

Neon provides a **pooler endpoint** that's faster. Update your connection string:

### Current (Direct Connection):
```
postgresql://neondb_owner:npg_SI5OmZEqpHl8@ep-dawn-block-ahbbc7e5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Check if Pooler is Already Used:
Your connection string already has `-pooler` in it, which is good! But you might need to add pooler-specific parameters.

### Optimized Connection String:
```
postgresql://neondb_owner:npg_SI5OmZEqpHl8@ep-dawn-block-ahbbc7e5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&connect_timeout=5
```

---

## Testing Performance

### Test Database Connection Speed:
```powershell
cd E:\heckathon-2\backend
python -c "import time; from app.database import engine; start=time.time(); conn=engine.connect(); print(f'Connection: {time.time()-start:.2f}s'); conn.close()"
```

**Expected**: < 2 seconds
**If > 5 seconds**: Database connection is the issue

### Test Registration Speed:
```powershell
# After migrations, test registration
$body = @{
    email = "test2@example.com"
    password = "Test123!@#"
    password_confirmation = "Test123!@#"
} | ConvertTo-Json

Measure-Command {
    Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/register" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $body `
        -UseBasicParsing
}
```

**Expected**: < 3 seconds
**If > 10 seconds**: Need further optimization

---

## Additional Optimizations (If Still Slow)

### Option 1: Increase Frontend Timeout Further
```typescript
// frontend/src/lib/api.ts
timeout: 60000, // 60 seconds
```

### Option 2: Add Database Indexes
```sql
-- Run in Neon SQL Editor
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
```

### Option 3: Use Async Database Operations
- Convert sync database calls to async
- Use async/await for better concurrency

---

## Step-by-Step Fix

1. **Run Migrations** (Critical):
   ```powershell
   cd E:\heckathon-2\backend
   alembic upgrade head
   ```

2. **Restart Backend**:
   ```powershell
   uvicorn app.main:app --reload
   ```
   Should start in < 2 seconds now

3. **Test Registration**:
   - Should complete in < 3 seconds
   - If still slow, check database connection

4. **If Still Timing Out**:
   - Check Neon dashboard for connection issues
   - Verify connection string is correct
   - Try direct connection (non-pooler) to test

---

## Expected Performance After Fix

- **Server Startup**: < 2 seconds ✅
- **Registration**: < 3 seconds ✅
- **Login**: < 2 seconds ✅
- **Task Operations**: < 1 second ✅

---

**Status**: Optimizations applied. **Run migrations before testing!**
