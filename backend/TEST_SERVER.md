# Server Troubleshooting Guide

## Server Status Check

The server appears to be running on port 8000. Here's how to verify and fix:

---

## Step 1: Verify Server is Running

Check if the server process is active:

```powershell
# Check if uvicorn is running
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*"}

# Check port 8000
netstat -ano | findstr :8000
```

---

## Step 2: Test Server Endpoints

### Option A: Using Browser
Try these URLs:
- **Root endpoint**: http://127.0.0.1:8000/
- **Health check**: http://127.0.0.1:8000/health
- **API docs**: http://127.0.0.1:8000/docs

### Option B: Using PowerShell
```powershell
# Test root endpoint
Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -UseBasicParsing

# Test health endpoint
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing
```

### Option C: Using curl (if available)
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
```

---

## Step 3: Check Server Logs

Look at the terminal where you ran `uvicorn app.main:app --reload`. You should see:
- `INFO: Uvicorn running on http://127.0.0.1:8000`
- `INFO: Application startup complete.`

If you see errors, share them.

---

## Step 4: Restart Server

If the server isn't responding:

1. **Stop the server** (Press `CTRL+C` in the terminal)
2. **Restart it**:
   ```powershell
   cd E:\heckathon-2\backend
   uvicorn app.main:app --reload
   ```

---

## Step 5: Check for Port Conflicts

If port 8000 is already in use:

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

Then restart the server.

---

## Step 6: Try Different URL

Sometimes `127.0.0.1` doesn't work. Try:
- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs

---

## Step 7: Check Firewall

Windows Firewall might be blocking the connection:

1. Open Windows Defender Firewall
2. Check if Python or uvicorn is blocked
3. Allow it if needed

---

## Expected Response

When you visit http://127.0.0.1:8000/, you should see:

```json
{
  "message": "Todo API Phase II",
  "version": "2.0.0",
  "status": "running"
}
```

When you visit http://127.0.0.1:8000/health, you should see:

```json
{
  "status": "healthy"
}
```

---

## Common Issues

### Issue: "This site can't be reached"
**Solution**: Server might not be running. Restart it.

### Issue: "Connection refused"
**Solution**: Check if the server is actually running on port 8000.

### Issue: Browser shows nothing
**Solution**: 
- Try a different browser
- Clear browser cache
- Check browser console for errors (F12)

### Issue: Server starts but crashes
**Solution**: Check the terminal output for error messages. Common causes:
- Database connection issues
- Missing environment variables
- Import errors

---

## Quick Test Script

Create a test file `test_server.py`:

```python
import requests

try:
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✅ Server is working!")
except requests.exceptions.ConnectionError:
    print("❌ Server is not running or not accessible")
except Exception as e:
    print(f"❌ Error: {e}")
```

Run it:
```powershell
cd E:\heckathon-2\backend
python test_server.py
```

---

## Still Not Working?

1. Share the exact error message from the browser
2. Share the server terminal output
3. Check if you can access http://127.0.0.1:8000/docs (Swagger UI)
