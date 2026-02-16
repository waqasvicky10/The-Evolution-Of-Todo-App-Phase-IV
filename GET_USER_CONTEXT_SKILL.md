# GetUserContext Skill - Documentation

## Overview

The **GetUserContext Skill** extracts authenticated user information (user_id, email, name) from JWT tokens for chatbot personalization and other features. This skill follows the pattern specified in the requirements:

1. Request header se **Authorization: Bearer \<token\>** lo
2. JWT decode karo (Better Auth secret use karo)
3. Return: `{"user_id": "...", "email": "...", "name": "..."}`

## Quick Start

### Usage in FastAPI Routes

```python
from app.api.deps import get_user_context
from fastapi import Depends

@router.get("/personalized")
def personalized_endpoint(context: dict = Depends(get_user_context)):
    """
    Endpoint with automatic user context extraction.
    No database query needed!
    """
    user_id = context['user_id']    # Always present
    email = context['email']        # May be None
    name = context['name']          # May be None
    
    return {"message": f"Hello {email}!"}
```

### Direct Token Extraction

```python
from app.core.user_context import get_user_context_from_token

# Extract context from raw token string
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
context = get_user_context_from_token(token)

print(context)
# Output: {'user_id': 1, 'email': 'user@example.com', 'name': 'John Doe'}
```

## Implementation Files

### Core Module: `user_context.py`

Location: [`backend/app/core/user_context.py`](file:///f:/heckathon-3/backend/app/core/user_context.py)

**Functions:**

1. **`get_user_context_from_token(token: str) -> dict`**
   - Core skill function
   - Extracts user context from JWT token
   - Returns: `{"user_id": int, "email": str|None, "name": str|None}`

2. **`get_user_context_from_credentials(credentials: HTTPAuthorizationCredentials) -> dict`**
   - FastAPI wrapper for `get_user_context_from_token`
   - Works directly with `HTTPBearer` security scheme

3. **`format_user_greeting(context: dict, language: str) -> str`**
   - Helper function for personalized greetings
   - Supports English ("en") and Urdu ("ur")

### Enhanced Security: `security.py`

Location: [`backend/app/core/security.py`](file:///f:/heckathon-3/backend/app/core/security.py)

**Updated Functions:**

- `create_access_token(user_id, email=None, name=None)`
- `create_refresh_token(user_id, email=None, name=None)`

Both now include optional `email` and `name` parameters that are encoded in the JWT payload.

### FastAPI Dependency: `deps.py`

Location: [`backend/app/api/deps.py`](file:///f:/heckathon-3/backend/app/api/deps.py)

**New Dependency:**

```python
def get_user_context(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Returns user context without database query.
    Use this when you only need user_id/email/name.
    """
```

## Integration Examples

### Example 1: Chat Endpoint with User Context

```python
@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    user_context: dict = Depends(get_user_context),
    db: Session = Depends(get_db)
):
    """Chat endpoint with user context logging."""
    # Log user context for debugging
    print(f"[Chat] User: {user_context['email']}")
    
    # Use context for personalization
    greeting = format_user_greeting(user_context, language="en")
    response = f"{greeting} How can I help you today?"
    
    return ChatResponse(response=response)
```

### Example 2: Profile Endpoint (No Database Query)

```python
@router.get("/me/quick")
def quick_profile(context: dict = Depends(get_user_context)):
    """
    Fast profile endpoint - extracts info from token only.
    No database query needed!
    """
    return {
        "user_id": context['user_id'],
        "email": context['email'],
        "name": context['name']
    }
```

### Example 3: Personalized Todo List

```python
@router.get("/todos/personalized")
def get_personalized_todos(
    context: dict = Depends(get_user_context),
    db: Session = Depends(get_db)
):
    """Get todos with personalized greeting."""
    greeting = format_user_greeting(context, language="en")
    
    tasks = get_user_tasks(db, context['user_id'])
    
    return {
        "greeting": greeting,
        "tasks": tasks,
        "user_email": context['email']
    }
```

## Authentication Flow

### Login Process

When a user logs in, the email is now automatically included in tokens:

```python
# In auth.py login endpoint
user = authenticate_user(db, email=request.email, password=request.password)

# Tokens now include email for context extraction
access_token = create_access_token(user.id, email=user.email)
refresh_token = create_refresh_token(user.id, email=user.email)
```

### Token Refresh

The refresh endpoint preserves user context:

```python
# Extract email from refresh token
payload = verify_token(request.refresh_token)
email = payload.get("email")
name = payload.get("name")

# New access token preserves context
new_access_token = create_access_token(user_id, email=email, name=name)
```

## Testing

Run the test suite:

```bash
cd f:\heckathon-3\backend
python test_get_user_context.py
```

**Test Coverage:**
- ✅ JWT token creation with email
- ✅ JWT token creation with email and name
- ✅ User context extraction from token
- ✅ Handling missing name field
- ✅ Greeting formatting (English & Urdu)
- ✅ Complete skill pattern demonstration

## API Reference

### `get_user_context_from_token(token: str) -> dict`

Extracts user context from JWT token string.

**Parameters:**
- `token` (str): JWT token from Authorization header

**Returns:**
- `dict`: User context with keys:
  - `user_id` (int): User's unique identifier
  - `email` (str | None): User's email address
  - `name` (str | None): User's name

**Raises:**
- `ValueError`: If token is invalid, expired, or missing user_id

**Example:**
```python
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
context = get_user_context_from_token(token)
# {'user_id': 1, 'email': 'user@example.com', 'name': 'John Doe'}
```

### `get_user_context(credentials) -> dict`

FastAPI dependency for extracting user context.

**Parameters:**
- `credentials` (HTTPAuthorizationCredentials): From `Depends(security)`

**Returns:**
- Same as `get_user_context_from_token`

**Raises:**
- `HTTPException 401`: If token is invalid or expired

**Example:**
```python
@app.get("/endpoint")
def endpoint(context: dict = Depends(get_user_context)):
    return {"email": context['email']}
```

### `format_user_greeting(context: dict, language: str) -> str`

Formats a personalized greeting.

**Parameters:**
- `context` (dict): User context from `get_user_context_from_token`
- `language` (str): "en" for English, "ur" for Urdu

**Returns:**
- `str`: Personalized greeting

**Example:**
```python
context = {"user_id": 1, "email": "waqas@example.com", "name": "Waqas"}
greeting = format_user_greeting(context, language="ur")
# "السلام علیکم Waqas!"
```

## Performance Benefits

### Before (using `get_current_user`)
- Extracts token → Decodes JWT → **Queries database** → Returns User object
- ~10-50ms (includes DB query)

### After (using `get_user_context`)
- Extracts token → Decodes JWT → Returns context dict
- ~1-5ms (no DB query!)

**Use `get_user_context` when:**
- You only need user_id, email, or name
- Performance is critical
- Database is under heavy load

**Use `get_current_user` when:**
- You need the full User object
- You need to check user status/flags
- You need related data (e.g., user.tasks)

## Best Practices

1. **Always call this skill first** in conversation handlers for debugging and personalization

2. **Log user context** at the start of important operations:
   ```python
   print(f"[Operation] User: {context['user_id']} ({context['email']})")
   ```

3. **Handle None values** gracefully:
   ```python
   display_name = context.get('name') or context.get('email') or f"User {context['user_id']}"
   ```

4. **Use for personalization**:
   ```python
   if context['email']:
       response = f"Hello {context['email'].split('@')[0]}!"
   ```

## Troubleshooting

### Issue: Context returns None for email/name

**Solution:** User logged in before this feature was implemented. Ask them to log out and log in again to get a new token with email included.

### Issue: HTTPException 401 "Invalid token"

**Solution:** Token is expired or malformed. User needs to refresh their token or log in again.

### Issue: "user_id not in context"

**Solution:** This should never happen if using the official `get_user_context` dependency. If it does, the token is not a valid authentication token.

## Future Enhancements

Potential additions to the skill:

- [ ] Add user roles/permissions to token payload
- [ ] Add last_login timestamp
- [ ] Support for multiple languages in greetings
- [ ] Cache user context for repeated requests
- [ ] Add user preferences to context
