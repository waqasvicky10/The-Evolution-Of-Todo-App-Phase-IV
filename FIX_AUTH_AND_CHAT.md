# 🔧 Fix Authentication & Chat Errors

## 🎯 Two Different Issues

### Issue 1: Authentication Errors (Current)
- `401 Unauthorized` - Login failed
- `409 Conflict` - Email already exists

### Issue 2: Chat API Errors (Previous)
- Phase III agent not responding properly

---

## ✅ Quick Fixes

### Fix 1: Registration Error (409 Conflict)

**Problem**: Email already exists in database

**Solution A: Use Different Email**
- Try registering with a different email address
- Example: `test2@example.com` instead of `test@example.com`

**Solution B: Login Instead**
- If you already registered, just login
- Use the email and password you used before

**Solution C: Clear Database (Development Only)**
```sql
-- Connect to your Neon PostgreSQL database
-- Run this to clear users (WARNING: Deletes all users!)
DELETE FROM users;
```

### Fix 2: Login Error (401 Unauthorized)

**Problem**: Wrong email/password or user doesn't exist

**Solutions**:
1. **Check credentials** - Make sure email and password are correct
2. **Register first** - If new user, register before logging in
3. **Reset password** - If forgot password, register again with same email (if allowed)

---

## 🚀 Step-by-Step Solution

### Option 1: Register with New Email (Easiest)

1. Go to: http://localhost:3000/register
2. Use a **different email** (e.g., `test2@example.com`)
3. Use a strong password (8+ characters)
4. Click "Create Account"

### Option 2: Login with Existing Account

1. Go to: http://localhost:3000/login
2. Enter the **email you registered with before**
3. Enter the **password you used**
4. Click "Sign In"

### Option 3: Check Database

If you want to see what users exist:

```powershell
# Connect to your Neon database
# Check users table
SELECT id, email, created_at FROM users;
```

---

## 🔍 Debugging Steps

### Step 1: Check Backend Logs

When you try to register/login, check backend terminal for:
- Registration: Should show user creation or conflict
- Login: Should show authentication attempt

### Step 2: Verify Database Connection

Make sure backend can connect to Neon PostgreSQL:
```powershell
cd E:\heckathon-2\backend
python -c "from app.database import engine; conn = engine.connect(); print('Connected!'); conn.close()"
```

### Step 3: Test Registration Endpoint

```powershell
# Test registration
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/auth/register" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"email": "newuser@example.com", "password": "Test1234!", "password_confirmation": "Test1234!"}'
```

---

## 📋 Common Scenarios

### Scenario 1: First Time User
**Action**: Register with any email

### Scenario 2: Already Registered
**Action**: Login with existing credentials

### Scenario 3: Forgot Password
**Action**: 
- Try to register again (might fail if email exists)
- Or use a different email

### Scenario 4: Want to Start Fresh
**Action**: Clear database (development only)

---

## ✅ Quick Test

1. **Try registration** with new email: `testuser@example.com`
2. **If 409 error**, email exists - try login instead
3. **If 401 error**, wrong password - try registering again

---

## 🎯 For Chat API (Separate Issue)

The chat API errors are different. To test chat:

1. **First, login successfully** (fix auth errors above)
2. **Then go to**: http://localhost:3000/chat
3. **Send message**: "Add a task to buy groceries"
4. **Check backend logs** for chat errors

---

## 📝 Summary

**Current Issue**: Authentication (401/409 errors)
- **409**: Email already exists → Use different email or login
- **401**: Wrong credentials → Check email/password

**Previous Issue**: Chat API (Phase III agent)
- Separate issue, test after fixing auth

**Action**: 
1. Try registering with different email OR
2. Login with existing credentials
3. Then test chat API

---

## 🔧 If Still Having Issues

Share:
1. **What you're trying to do** (register or login)
2. **Email you're using**
3. **Backend logs** when you try to register/login
4. **Any error messages** from frontend
