# Browser Testing Guide

## Servers Started

### Backend (FastAPI)
- **URL:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Frontend (Next.js)
- **URL:** http://localhost:3000
- **Landing Page:** http://localhost:3000
- **Register:** http://localhost:3000/register
- **Login:** http://localhost:3000/login
- **Dashboard:** http://localhost:3000/dashboard (requires login)

## Testing Checklist

### 1. Landing Page
- [ ] Open http://localhost:3000
- [ ] Verify page loads without errors
- [ ] Check browser console for errors (F12)
- [ ] Verify navigation links work

### 2. Registration
- [ ] Click "Register" or go to /register
- [ ] Fill in registration form:
  - Email: test@example.com
  - Password: Test123!@#
  - Confirm Password: Test123!@#
- [ ] Submit form
- [ ] Verify success message
- [ ] Check for console errors

### 3. Login
- [ ] Go to /login
- [ ] Enter credentials:
  - Email: test@example.com
  - Password: Test123!@#
- [ ] Submit form
- [ ] Verify redirect to dashboard
- [ ] Check for console errors

### 4. Dashboard
- [ ] Verify you're logged in
- [ ] Check empty state (if no tasks)
- [ ] Create a new task
- [ ] Verify task appears in list
- [ ] Toggle task completion
- [ ] Edit task description
- [ ] Delete task
- [ ] Check browser console for errors

### 5. API Testing
- [ ] Open http://localhost:8000/docs
- [ ] Test POST /api/auth/register
- [ ] Test POST /api/auth/login
- [ ] Test GET /api/tasks (with token)
- [ ] Test POST /api/tasks (with token)
- [ ] Verify all endpoints work

## Common Issues to Check

### Browser Console Errors
1. Open Developer Tools (F12)
2. Check Console tab for:
   - Red error messages
   - Network errors (404, 500, etc.)
   - CORS errors
   - Authentication errors

### Network Tab
1. Check Network tab in DevTools
2. Verify API calls are successful:
   - Status 200 for successful requests
   - Status 401 for unauthorized
   - Status 404 for not found
   - Status 500 for server errors

### Common Errors
- **CORS errors:** Backend CORS not configured correctly
- **401 Unauthorized:** Token not being sent or expired
- **404 Not Found:** API endpoint not found
- **500 Server Error:** Backend error, check backend logs

## Fixing Issues

If you find errors:
1. Note the error message
2. Check browser console
3. Check backend terminal for errors
4. Check frontend terminal for errors
5. Fix the issue
6. Refresh browser and test again

## Next Steps

After successful testing:
1. All features work correctly
2. No console errors
3. All API endpoints respond correctly
4. Ready for deployment
