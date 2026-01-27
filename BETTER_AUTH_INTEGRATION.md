# Better Auth Integration Guide

This guide explains how Better Auth is integrated into the Todo App for Phase II compliance.

---

## Overview

Better Auth is now integrated as the authentication solution for the frontend (Next.js), replacing the custom JWT implementation. Better Auth handles:

- User registration
- User login
- Session management (cookies)
- Password hashing
- Token generation

The FastAPI backend validates Better Auth sessions and can work alongside Better Auth's authentication system.

---

## Architecture

```
┌─────────────────┐
│   Next.js App   │
│  (Better Auth)  │
└────────┬────────┘
         │
         │ Session Cookie
         │
┌────────▼────────┐
│  FastAPI Backend│
│ (Validates      │
│  Better Auth    │
│  Sessions)      │
└─────────────────┘
```

---

## Installation

### 1. Install Better Auth Packages

```bash
cd frontend
npm install better-auth @better-auth/react
```

### 2. Environment Variables

Create or update `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-at-least-32-characters-long
NEXT_PUBLIC_BASE_URL=http://localhost:3000

# Database URL (should match backend for user sync)
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

---

## File Structure

### Frontend Files

```
frontend/
├── src/
│   ├── lib/
│   │   ├── auth.ts              # Better Auth server configuration
│   │   ├── auth-client.ts       # Better Auth React client
│   │   └── db.ts                # Database adapter (placeholder)
│   ├── app/
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts  # Better Auth API route handler
│   └── contexts/
│       └── BetterAuthContext.tsx # React context for Better Auth
```

---

## Usage

### 1. Wrap App with Better Auth Provider

Update `frontend/src/app/layout.tsx`:

```tsx
import { BetterAuthProvider } from "@/contexts/BetterAuthContext";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <BetterAuthProvider>
          {children}
        </BetterAuthProvider>
      </body>
    </html>
  );
}
```

### 2. Use Better Auth in Components

```tsx
import { useBetterAuth } from "@/contexts/BetterAuthContext";

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useBetterAuth();

  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }

  return (
    <div>
      <p>Welcome, {user?.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### 3. Login Page

```tsx
import { useBetterAuth } from "@/contexts/BetterAuthContext";

export default function LoginPage() {
  const { login } = useBetterAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      // Redirect handled by context
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
    </form>
  );
}
```

---

## FastAPI Integration

### Option 1: Validate Better Auth Sessions (Recommended)

FastAPI can validate Better Auth session cookies:

```python
from fastapi import Depends, HTTPException, Request
from better_auth import verify_session

def get_current_user(request: Request):
    """Validate Better Auth session from cookie."""
    session_token = request.cookies.get("better-auth.session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Verify session with Better Auth
    session = verify_session(session_token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    return session.user
```

### Option 2: Sync Users with FastAPI Database

Better Auth stores users in its own database. To sync with FastAPI:

1. **Create a webhook** in Better Auth to notify FastAPI when users register
2. **Use FastAPI's user service** to create users when Better Auth creates them
3. **Share the same database** between Better Auth and FastAPI

---

## Migration from Custom JWT

### Before (Custom JWT)

```tsx
// Old AuthContext
const { login, user, isAuthenticated } = useAuth();
await login({ email, password });
```

### After (Better Auth)

```tsx
// New BetterAuthContext
const { login, user, isAuthenticated } = useBetterAuth();
await login(email, password);
```

### Changes Required

1. **Replace `useAuth` with `useBetterAuth`** in all components
2. **Update login/register calls** to use Better Auth methods
3. **Remove custom JWT token management** (Better Auth handles this)
4. **Update API client** to use session cookies instead of Bearer tokens

---

## API Client Updates

### Before (JWT Bearer Token)

```tsx
// Old API client
apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
```

### After (Session Cookies)

```tsx
// Better Auth handles cookies automatically
// No manual token management needed
// Cookies are sent with requests automatically
```

---

## Database Setup

Better Auth requires a database. Options:

### Option 1: Shared PostgreSQL Database (Recommended)

Use the same Neon PostgreSQL database for both Better Auth and FastAPI:

```env
# Both frontend and backend use same DATABASE_URL
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

Better Auth will create its own tables:
- `user`
- `session`
- `account`
- `verification`

FastAPI uses:
- `users` (can sync with Better Auth's `user` table)
- `tasks`

### Option 2: Separate Databases

- Better Auth: SQLite or separate PostgreSQL
- FastAPI: Neon PostgreSQL

Requires user synchronization between databases.

---

## Testing

### 1. Test Registration

```bash
# Start frontend
cd frontend
npm run dev

# Visit http://localhost:3000/register
# Create a new account
```

### 2. Test Login

```bash
# Visit http://localhost:3000/login
# Login with created account
```

### 3. Test Session

```bash
# Check browser cookies
# Should see: better-auth.session_token

# Check database
# Should see user in Better Auth's user table
```

---

## Troubleshooting

### Issue: "Better Auth not found"

**Solution:**
```bash
cd frontend
npm install better-auth @better-auth/react
```

### Issue: "Database connection failed"

**Solution:**
- Check `DATABASE_URL` in `.env.local`
- Verify Neon PostgreSQL connection string
- Ensure database is accessible

### Issue: "Session not persisting"

**Solution:**
- Check `BETTER_AUTH_SECRET` is set
- Verify `baseURL` matches your frontend URL
- Check CORS settings in FastAPI

### Issue: "FastAPI can't validate sessions"

**Solution:**
- Install Better Auth Python SDK (if available)
- Or implement custom session validation
- Or use shared database to query sessions

---

## Production Deployment

### Environment Variables

Set in your hosting platform (Vercel, Render, etc.):

```env
BETTER_AUTH_SECRET=your-production-secret-key
NEXT_PUBLIC_BASE_URL=https://your-app.vercel.app
DATABASE_URL=postgresql://... (Neon connection string)
```

### Security

1. **Use strong `BETTER_AUTH_SECRET`** (32+ characters, random)
2. **Enable HTTPS** (required for secure cookies)
3. **Set secure cookie flags** in production
4. **Enable email verification** for production

---

## Next Steps

1. ✅ Better Auth installed and configured
2. ✅ API routes created
3. ✅ React context provider created
4. ⚠️ Update login/register pages to use Better Auth
5. ⚠️ Update dashboard to use Better Auth
6. ⚠️ Integrate with FastAPI backend
7. ⚠️ Test end-to-end authentication flow

---

## Resources

- **Better Auth Documentation**: https://better-auth.com/docs
- **Better Auth GitHub**: https://github.com/better-auth/better-auth
- **Next.js Integration**: https://better-auth.com/docs/integrations/next

---

**Status**: ✅ Better Auth integrated, ready for testing and FastAPI integration
