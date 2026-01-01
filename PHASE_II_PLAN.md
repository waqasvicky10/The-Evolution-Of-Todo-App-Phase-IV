# PHASE II TECHNICAL IMPLEMENTATION PLAN

**Project:** Evolution of Todo
**Phase:** II - Full-Stack Web Application
**Version:** 1.0
**Status:** DRAFT
**Parent Document:** PHASE_II_SPECIFICATION.md
**Constitutional Compliance:** Verified against CONSTITUTION.md v2.0
**Date:** 2026-01-01

---

## EXECUTIVE SUMMARY

This document defines the technical implementation approach for Phase II of the Evolution of Todo project. It describes HOW the approved Phase II specification will be implemented as a full-stack web application with Next.js frontend, FastAPI backend, Neon PostgreSQL database, and Better Auth JWT authentication, without introducing new features or deviating from constitutional requirements.

---

## CONSTITUTIONAL COMPLIANCE

This plan is created under:
- **Article I, Section 1.3:** Plan Requirements
- **Article II, Section 2.2:** Strict Specification Adherence
- **Article III, Section 3.1:** Phase Scope Boundaries
- **Article IV, Section 4.1:** Phase II Technology Stack
- **Article VIII, Section 8.2:** Phase II - Full-Stack Web Application
- **Article IX:** Security Requirements
- **Constitutional Workflow:** Constitution → Spec → **Plan** → Tasks → Code

This plan implements ONLY what is specified in PHASE_II_SPECIFICATION.md.

---

## PLANNING PRINCIPLES

### What This Plan Does
✅ Describes technical implementation approach for full-stack architecture
✅ Defines database schema and ORM models
✅ Specifies API endpoints and request/response contracts
✅ Documents authentication and authorization flows
✅ Defines frontend architecture and component structure
✅ Specifies error handling strategies
✅ Breaks work into implementable components
✅ Ensures architectural and security compliance

### What This Plan Does NOT Do
❌ Add new features beyond specification (no AI, no NLP, no agents)
❌ Make architectural decisions not in spec
❌ Reference Phase III features
❌ Introduce unapproved dependencies
❌ Change specified behavior
❌ Implement advanced features out of scope

---

## 1. HIGH-LEVEL SYSTEM ARCHITECTURE

### 1.1 Architecture Overview

Phase II is a **three-tier full-stack web application** with:
- **Frontend (Presentation Tier):** Next.js 14+ with App Router, TypeScript
- **Backend (Application Tier):** FastAPI with SQLModel ORM, Python 3.11+
- **Database (Data Tier):** Neon Serverless PostgreSQL

**Communication:**
- Frontend ↔ Backend: RESTful HTTP API (JSON)
- Backend ↔ Database: SQLModel ORM (PostgreSQL wire protocol)

**Deployment Model (Development):**
- Frontend: `http://localhost:3000` (Next.js dev server)
- Backend: `http://localhost:8000` (Uvicorn ASGI server)
- Database: Neon cloud-hosted PostgreSQL

---

### 1.2 Application Flow

```
User Browser (Client)
       ↓
Next.js Frontend (Port 3000)
       ↓ HTTP/JSON + JWT
FastAPI Backend (Port 8000)
       ↓ SQL via SQLModel
Neon PostgreSQL Database
```

**Request Flow Example (Create Task):**
1. User clicks "Add Task" in browser
2. Frontend sends `POST /api/tasks` with JWT token
3. Backend validates JWT, extracts user_id
4. Backend validates task description
5. Backend creates task record with user_id in database
6. Database returns created task
7. Backend returns task JSON to frontend
8. Frontend updates UI with new task

---

### 1.3 Security Architecture

**Authentication Layer:**
- Better Auth library for JWT generation/validation
- Bcrypt for password hashing (cost factor 12)
- Access tokens: 15-minute expiration
- Refresh tokens: 7-day expiration

**Authorization Layer:**
- Middleware extracts user_id from JWT
- All task queries filter by user_id
- User isolation enforced at SQL query level

**Data Protection:**
- Passwords: bcrypt hashed, never stored plaintext
- Tokens: httpOnly cookies (preferred) or localStorage
- Secrets: environment variables only
- Database: parameterized queries via ORM (SQL injection prevention)

---

## 2. DATABASE DESIGN

### 2.1 Schema Design

**Database:** PostgreSQL 16 (Neon Serverless)
**ORM:** SQLModel (Pydantic + SQLAlchemy)

#### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

**Fields:**
- `id`: Auto-incrementing integer primary key
- `email`: Unique email address, indexed for fast login lookups
- `hashed_password`: Bcrypt hash (60 characters), never plaintext
- `created_at`: Timestamp of account creation (UTC)
- `updated_at`: Timestamp of last modification (UTC)

**Indexes:**
- Primary key index on `id` (automatic)
- Unique index on `email` (for login queries)

---

#### Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    description VARCHAR(500) NOT NULL,
    is_complete BOOLEAN DEFAULT FALSE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

**Fields:**
- `id`: Auto-incrementing integer primary key
- `description`: Task description, max 500 characters, required
- `is_complete`: Boolean completion status, defaults to false
- `user_id`: Foreign key to users.id, required, indexed
- `created_at`: Timestamp of task creation (UTC)
- `updated_at`: Timestamp of last modification (UTC)

**Indexes:**
- Primary key index on `id` (automatic)
- Foreign key index on `user_id` (for user-filtered queries)

**Constraints:**
- Foreign key: `tasks.user_id` → `users.id` with `ON DELETE CASCADE`
- Check: `description` length 1-500 characters (enforced by ORM)

---

### 2.2 SQLModel Definitions

#### User Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")
```

---

#### Task Model

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=500, min_length=1)
    is_complete: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

---

### 2.3 Database Migrations

**Migration Tool:** Alembic

**Initial Migration:** `001_create_users_and_tasks_tables`

**Migration Strategy:**
1. Create `users` table with indexes
2. Create `tasks` table with foreign key and indexes
3. Seed data: None (users register via UI)

**Migration Commands:**
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create users and tasks tables"

# Apply migration
alembic upgrade head
```

---

## 3. BACKEND ARCHITECTURE (FastAPI)

### 3.1 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app, CORS, startup/shutdown
│   ├── config.py                    # Pydantic Settings (env vars)
│   ├── database.py                  # DB connection, engine, session
│   │
│   ├── models/                      # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py                  # User model
│   │   └── task.py                  # Task model
│   │
│   ├── schemas/                     # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth.py                  # RegisterRequest, LoginRequest, TokenResponse
│   │   └── task.py                  # TaskCreate, TaskUpdate, TaskResponse
│   │
│   ├── api/                         # API routes and dependencies
│   │   ├── __init__.py
│   │   ├── deps.py                  # Dependency injection (get_db, get_current_user)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py              # Auth endpoints: register, login, logout, refresh
│   │       └── tasks.py             # Task endpoints: CRUD operations
│   │
│   ├── core/                        # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py              # Password hashing, JWT generation/validation
│   │   └── exceptions.py            # Custom exceptions (NotFoundError, UnauthorizedError)
│   │
│   └── services/                    # Business logic layer
│       ├── __init__.py
│       ├── user_service.py          # User registration, login logic
│       └── task_service.py          # Task CRUD logic with user isolation
│
├── alembic/                         # Database migrations
│   ├── versions/
│   │   └── 001_create_users_and_tasks.py
│   └── env.py
│
├── tests/                           # Pytest test suite
│   ├── __init__.py
│   ├── conftest.py                  # Test fixtures (test DB, test client)
│   ├── test_auth.py                 # Auth endpoint tests
│   ├── test_tasks.py                # Task endpoint tests
│   └── test_user_isolation.py      # User data isolation tests
│
├── .env.example                     # Environment variable template
├── .env                             # Environment variables (gitignored)
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata, Ruff config
└── README.md                        # Backend setup instructions
```

---

### 3.2 Module Responsibilities

| Module | Responsibility | Key Functions |
|--------|---------------|--------------|
| `main.py` | FastAPI app initialization, CORS, startup/shutdown events | `app = FastAPI()`, CORS middleware |
| `config.py` | Environment configuration via Pydantic BaseSettings | `Settings` class |
| `database.py` | Database connection, engine, session management | `get_session()`, `init_db()` |
| `models/user.py` | User SQLModel definition | `User` model |
| `models/task.py` | Task SQLModel definition | `Task` model |
| `schemas/auth.py` | Auth request/response schemas | `RegisterRequest`, `LoginRequest`, `TokenResponse` |
| `schemas/task.py` | Task request/response schemas | `TaskCreate`, `TaskUpdate`, `TaskResponse` |
| `api/deps.py` | Dependency injection for DB session and current user | `get_db()`, `get_current_user()` |
| `api/routes/auth.py` | Auth endpoints (register, login, logout, refresh) | `POST /api/auth/register`, `POST /api/auth/login` |
| `api/routes/tasks.py` | Task CRUD endpoints | `GET /api/tasks`, `POST /api/tasks`, etc. |
| `core/security.py` | Password hashing, JWT generation/validation | `hash_password()`, `create_access_token()`, `verify_token()` |
| `core/exceptions.py` | Custom exception definitions | `NotFoundError`, `UnauthorizedError`, `ForbiddenError` |
| `services/user_service.py` | User business logic (register, login) | `create_user()`, `authenticate_user()` |
| `services/task_service.py` | Task business logic (CRUD with user isolation) | `create_task()`, `get_user_tasks()`, `update_task()` |

---

### 3.3 API Endpoints

#### Authentication Endpoints

| Method | Endpoint | Description | Auth Required | Request Body | Response |
|--------|----------|-------------|--------------|--------------|----------|
| POST | `/api/auth/register` | Register new user | No | `RegisterRequest` | `UserResponse` (201) |
| POST | `/api/auth/login` | Login user | No | `LoginRequest` | `TokenResponse` (200) |
| POST | `/api/auth/logout` | Logout user | Yes | None | `{"message": "..."}` (200) |
| POST | `/api/auth/refresh` | Refresh access token | No | `{"refresh_token": "..."}` | `TokenResponse` (200) |

---

#### Task Endpoints

| Method | Endpoint | Description | Auth Required | Request Body | Response |
|--------|----------|-------------|--------------|--------------|----------|
| GET | `/api/tasks` | Get all tasks for authenticated user | Yes | None | `{"tasks": [...], "total": N}` (200) |
| POST | `/api/tasks` | Create new task | Yes | `TaskCreate` | `TaskResponse` (201) |
| GET | `/api/tasks/{id}` | Get specific task | Yes | None | `TaskResponse` (200) |
| PUT | `/api/tasks/{id}` | Update task description | Yes | `TaskUpdate` | `TaskResponse` (200) |
| PATCH | `/api/tasks/{id}/toggle` | Toggle task completion | Yes | None | `TaskResponse` (200) |
| DELETE | `/api/tasks/{id}` | Delete task | Yes | None | `{"message": "..."}` (200) |

---

### 3.4 Request/Response Schemas

#### Auth Schemas

```python
# RegisterRequest
{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "password_confirmation": "SecurePass123!"
}

# LoginRequest
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}

# TokenResponse
{
    "access_token": "eyJhbGciOi...",
    "refresh_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "expires_in": 900
}
```

---

#### Task Schemas

```python
# TaskCreate
{
    "description": "Buy groceries"
}

# TaskUpdate
{
    "description": "Buy groceries and cook dinner"
}

# TaskResponse
{
    "id": 1,
    "description": "Buy groceries",
    "is_complete": false,
    "user_id": 1,
    "created_at": "2026-01-01T12:00:00Z",
    "updated_at": "2026-01-01T12:00:00Z"
}

# TaskListResponse
{
    "tasks": [TaskResponse, TaskResponse, ...],
    "total": 5
}
```

---

### 3.5 Authentication Flow

#### Registration Flow

```
1. Client → POST /api/auth/register {email, password, password_confirmation}
2. Backend validates:
   - Email format (regex)
   - Email unique (DB query)
   - Password strength (8+ chars, uppercase, lowercase, digit, special)
   - Password match (password == password_confirmation)
3. If valid:
   - Hash password with bcrypt
   - Create user record in DB
   - Return 201 Created with user data (no password)
4. If invalid:
   - Return 400 Bad Request with validation errors
```

---

#### Login Flow

```
1. Client → POST /api/auth/login {email, password}
2. Backend:
   - Query user by email
   - If not found: Return 401 "Invalid email or password"
   - Verify password hash with bcrypt
   - If invalid: Return 401 "Invalid email or password"
3. If valid:
   - Generate JWT access token (15 min expiration, payload: {user_id, exp})
   - Generate JWT refresh token (7 day expiration, payload: {user_id, exp})
   - Return 200 OK with TokenResponse
4. Client stores tokens (httpOnly cookies or localStorage)
```

---

#### Token Refresh Flow

```
1. Client → POST /api/auth/refresh {refresh_token}
2. Backend:
   - Verify refresh token signature
   - Check expiration
   - If invalid/expired: Return 401 Unauthorized
3. If valid:
   - Extract user_id from token payload
   - Generate new access token (15 min expiration)
   - Return 200 OK with new access token
```

---

#### Logout Flow

```
1. Client → POST /api/auth/logout (with Authorization: Bearer <access_token>)
2. Backend:
   - Validate access token (optional, can skip if client-side only)
   - Return 200 OK with success message
3. Client discards tokens (clears cookies/localStorage)
```

---

### 3.6 Authorization Middleware

**Dependency: `get_current_user()`**

```python
# Pseudocode
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    1. Extract token from Authorization header
    2. If no token: Raise HTTPException(401, "Not authenticated")
    3. Verify token signature with SECRET_KEY
    4. If invalid: Raise HTTPException(401, "Invalid token")
    5. If expired: Raise HTTPException(401, "Token expired")
    6. Extract user_id from token payload
    7. Query user from database by user_id
    8. If not found: Raise HTTPException(401, "User not found")
    9. Return user object
```

**Usage in Endpoints:**

```python
@router.get("/api/tasks")
def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # current_user is automatically injected, or 401 raised if invalid token
    tasks = task_service.get_user_tasks(db, user_id=current_user.id)
    return {"tasks": tasks, "total": len(tasks)}
```

---

### 3.7 User Data Isolation Strategy

**Rule:** ALL task queries MUST filter by `user_id = current_user.id`

**Implementation in Task Service:**

```python
# get_user_tasks()
def get_user_tasks(db: Session, user_id: int) -> List[Task]:
    return db.query(Task).filter(Task.user_id == user_id).all()

# get_task_by_id()
def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise NotFoundError("Task not found")
    return task

# update_task()
def update_task(db: Session, task_id: int, user_id: int, description: str) -> Task:
    task = get_task_by_id(db, task_id, user_id)  # Enforces ownership check
    task.description = description
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

# delete_task()
def delete_task(db: Session, task_id: int, user_id: int) -> None:
    task = get_task_by_id(db, task_id, user_id)  # Enforces ownership check
    db.delete(task)
    db.commit()
```

**Key Points:**
- Never trust client-sent `user_id`
- Always use `current_user.id` from JWT
- If task not found OR belongs to different user: Raise 404 (don't leak existence)
- Alternative: Raise 403 Forbidden if want to distinguish (less secure)

---

### 3.8 Error Handling Strategy

#### HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 OK | Success (GET, PUT, PATCH, DELETE) | Task retrieved/updated/deleted successfully |
| 201 Created | Resource created | User registered, task created |
| 400 Bad Request | Validation error | Invalid email, weak password, description too long |
| 401 Unauthorized | Not authenticated | Missing token, invalid token, expired token |
| 403 Forbidden | Not authorized | Task belongs to another user (optional, can use 404) |
| 404 Not Found | Resource not found | Task ID not found, user not found |
| 409 Conflict | Duplicate resource | Email already registered |
| 500 Internal Server Error | Server error | Database connection error, unexpected exception |

---

#### Exception Handling

```python
# Custom exceptions (core/exceptions.py)
class NotFoundError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class ValidationError(Exception):
    pass

# Exception handlers (main.py)
@app.exception_handler(NotFoundError)
def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(UnauthorizedError)
def unauthorized_handler(request, exc):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

@app.exception_handler(ForbiddenError)
def forbidden_handler(request, exc):
    return JSONResponse(status_code=403, content={"detail": str(exc)})

@app.exception_handler(ValidationError)
def validation_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

---

### 3.9 CORS Configuration

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Security Notes:**
- Only allow frontend origin in development
- In production, use actual frontend domain
- `allow_credentials=True` required for cookies

---

## 4. FRONTEND ARCHITECTURE (Next.js)

### 4.1 Project Structure

```
frontend/
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── layout.tsx               # Root layout (global styles, providers)
│   │   ├── page.tsx                 # Landing page (/)
│   │   ├── register/
│   │   │   └── page.tsx             # Register page (/register)
│   │   ├── login/
│   │   │   └── page.tsx             # Login page (/login)
│   │   └── dashboard/
│   │       └── page.tsx             # Dashboard (/dashboard) - protected
│   │
│   ├── components/                  # Reusable UI components
│   │   ├── Navbar.tsx               # Navigation bar
│   │   ├── TaskCard.tsx             # Individual task display
│   │   ├── TaskList.tsx             # List of tasks
│   │   ├── AddTaskModal.tsx         # Modal for adding task
│   │   ├── EditTaskModal.tsx        # Modal for editing task
│   │   ├── DeleteConfirmModal.tsx   # Confirmation modal for delete
│   │   └── ProtectedRoute.tsx       # HOC for route protection
│   │
│   ├── contexts/                    # React Context providers
│   │   └── AuthContext.tsx          # Auth state (user, login, logout)
│   │
│   ├── hooks/                       # Custom React hooks
│   │   ├── useAuth.ts               # Auth operations hook
│   │   └── useTasks.ts              # Task CRUD operations hook
│   │
│   ├── lib/                         # Utility libraries
│   │   ├── api.ts                   # API client (axios wrapper)
│   │   └── auth.ts                  # JWT storage/retrieval utilities
│   │
│   ├── types/                       # TypeScript type definitions
│   │   ├── user.ts                  # User, AuthState types
│   │   └── task.ts                  # Task, TaskList types
│   │
│   └── utils/                       # Helper functions
│       └── validation.ts            # Form validation helpers
│
├── public/                          # Static assets
│   └── favicon.ico
│
├── tests/                           # Jest + React Testing Library
│   └── components/
│       ├── TaskCard.test.tsx
│       └── AddTaskModal.test.tsx
│
├── .env.example                     # Environment variable template
├── .env.local                       # Environment variables (gitignored)
├── next.config.js                   # Next.js configuration
├── tsconfig.json                    # TypeScript configuration
├── tailwind.config.js               # Tailwind CSS configuration (if used)
├── package.json                     # NPM dependencies and scripts
└── README.md                        # Frontend setup instructions
```

---

### 4.2 Page Components

#### Landing Page (`/`)

**Purpose:** Welcome page with CTA to login/register
**Access:** Public (redirects to /dashboard if authenticated)

**Structure:**
```tsx
- Hero section with app description
- "Get Started" button → /register
- "Already have an account? Login" link → /login
- Footer
```

---

#### Register Page (`/register`)

**Purpose:** User registration form
**Access:** Public (redirects to /dashboard if authenticated)

**Form Fields:**
- Email (text input, email validation)
- Password (password input, strength validation)
- Password Confirmation (password input, match validation)
- Submit button ("Create Account")
- Link to login page

**Validation (Client-Side):**
- Email: Required, valid email format
- Password: Required, 8+ chars, uppercase, lowercase, digit, special char
- Password Confirmation: Required, matches password

**Submit Flow:**
1. Validate form inputs
2. If invalid: Show inline errors
3. If valid: Call `POST /api/auth/register`
4. If success (201): Redirect to /login with success toast
5. If error (400/409): Show error message

---

#### Login Page (`/login`)

**Purpose:** User login form
**Access:** Public (redirects to /dashboard if authenticated)

**Form Fields:**
- Email (text input)
- Password (password input)
- Submit button ("Login")
- Link to register page

**Submit Flow:**
1. Validate form inputs (non-empty)
2. Call `POST /api/auth/login`
3. If success (200):
   - Store tokens (httpOnly cookies or localStorage)
   - Update auth context
   - Redirect to /dashboard
4. If error (401): Show error "Invalid email or password"

---

#### Dashboard Page (`/dashboard`)

**Purpose:** User's task management interface
**Access:** Protected (redirects to /login if not authenticated)

**Layout:**
- Navbar (user email, logout button)
- Task list section
  - "Add Task" button
  - TaskList component (displays all tasks)
  - Empty state if no tasks: "No tasks yet. Create your first task!"
- Footer

**Data Fetching:**
- On page load: Call `GET /api/tasks`
- Display tasks in TaskList component
- Handle loading state
- Handle error state

---

### 4.3 Component Specifications

#### Navbar Component

**Props:** None (uses AuthContext)

**Display:**
- App logo/name
- If authenticated:
  - User email
  - Logout button
- If not authenticated:
  - Login link
  - Register link

---

#### TaskCard Component

**Props:**
```tsx
interface TaskCardProps {
  task: {
    id: number;
    description: string;
    is_complete: boolean;
  };
  onToggle: (id: number) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}
```

**Display:**
- Checkbox (checked if is_complete)
- Description (strikethrough if complete)
- Edit button (pencil icon)
- Delete button (trash icon)

**Interactions:**
- Click checkbox: Call onToggle(id)
- Click edit: Call onEdit(id)
- Click delete: Call onDelete(id)

---

#### AddTaskModal Component

**Props:**
```tsx
interface AddTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (description: string) => void;
}
```

**Display:**
- Modal overlay
- Form with textarea (max 500 chars)
- Character counter: "X / 500"
- Submit button ("Add Task")
- Cancel button

**Validation:**
- Description: Required, 1-500 chars
- Show error if empty or too long

**Submit Flow:**
1. Validate description
2. If valid: Call onSubmit(description)
3. If error: Show error message
4. On success: Close modal

---

#### EditTaskModal Component

**Props:**
```tsx
interface EditTaskModalProps {
  isOpen: boolean;
  task: { id: number; description: string } | null;
  onClose: () => void;
  onSubmit: (id: number, description: string) => void;
}
```

**Display:**
- Modal overlay
- Form with textarea pre-filled with task.description
- Character counter: "X / 500"
- Submit button ("Update Task")
- Cancel button

**Validation:**
- Description: Required, 1-500 chars
- Show error if empty or too long

**Submit Flow:**
1. Validate description
2. If valid: Call onSubmit(task.id, description)
3. If error: Show error message
4. On success: Close modal

---

#### DeleteConfirmModal Component

**Props:**
```tsx
interface DeleteConfirmModalProps {
  isOpen: boolean;
  taskDescription: string;
  onClose: () => void;
  onConfirm: () => void;
}
```

**Display:**
- Modal overlay
- Message: "Are you sure you want to delete this task?"
- Task description display
- Confirm button ("Delete", red/danger style)
- Cancel button

**Interactions:**
- Click confirm: Call onConfirm()
- Click cancel: Call onClose()

---

### 4.4 State Management

#### Auth State (AuthContext)

**State:**
```tsx
interface AuthState {
  user: { id: number; email: string } | null;
  loading: boolean;
  error: string | null;
}
```

**Actions:**
```tsx
- login(email, password): Promise<void>
- logout(): void
- register(email, password, passwordConfirmation): Promise<void>
- refreshToken(): Promise<void>
```

**Context Provider:**
- Wraps entire app in root layout
- Provides auth state and actions to all components
- Handles token refresh automatically

---

#### Task State (useTasks hook)

**State:**
```tsx
interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}
```

**Actions:**
```tsx
- fetchTasks(): Promise<void>
- createTask(description: string): Promise<void>
- updateTask(id: number, description: string): Promise<void>
- deleteTask(id: number): Promise<void>
- toggleTask(id: number): Promise<void>
```

**Usage:**
- Import in Dashboard page
- Call fetchTasks() on mount
- Pass actions to components

---

### 4.5 API Client (`lib/api.ts`)

**Implementation:** Axios wrapper with interceptors

**Base Configuration:**
```tsx
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});
```

**Request Interceptor:**
```tsx
api.interceptors.request.use((config) => {
  const token = getAccessToken(); // From localStorage or cookies
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

**Response Interceptor:**
```tsx
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try refresh
      try {
        await refreshToken();
        return api.request(error.config); // Retry original request
      } catch {
        // Refresh failed, redirect to login
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

---

### 4.6 Routing and Protection

#### Public Routes
- `/` - Landing page
- `/register` - Registration page
- `/login` - Login page

**Behavior:**
- If user is authenticated: Redirect to `/dashboard`

---

#### Protected Routes
- `/dashboard` - Dashboard page

**Behavior:**
- If user is NOT authenticated: Redirect to `/login`
- If user is authenticated: Render page

**Implementation:**
- Use middleware or ProtectedRoute HOC
- Check auth state from AuthContext
- Redirect if not authenticated

---

### 4.7 Form Validation

#### Email Validation

```tsx
function validateEmail(email: string): string | null {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!email) return "Email is required";
  if (!emailRegex.test(email)) return "Please enter a valid email address";
  return null; // Valid
}
```

---

#### Password Validation

```tsx
function validatePassword(password: string): string | null {
  if (!password) return "Password is required";
  if (password.length < 8) return "Password must be at least 8 characters";
  if (!/[A-Z]/.test(password)) return "Password must contain an uppercase letter";
  if (!/[a-z]/.test(password)) return "Password must contain a lowercase letter";
  if (!/[0-9]/.test(password)) return "Password must contain a number";
  if (!/[!@#$%^&*]/.test(password)) return "Password must contain a special character";
  return null; // Valid
}
```

---

#### Task Description Validation

```tsx
function validateDescription(description: string): string | null {
  const trimmed = description.trim();
  if (!trimmed) return "Task description cannot be empty";
  if (trimmed.length > 500) return "Task description too long (max 500 characters)";
  return null; // Valid
}
```

---

## 5. SECURITY IMPLEMENTATION

### 5.1 Password Hashing

**Library:** `passlib` (Python) with bcrypt

**Implementation:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Configuration:**
- Cost factor: 12 (default for bcrypt in passlib)
- Salt: Automatically generated per hash

---

### 5.2 JWT Implementation

**Library:** `python-jose` (Python)

**Token Generation:**
```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")  # Min 32 chars
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

---

**Token Verification:**
```python
from jose import JWTError, jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise UnauthorizedError("Invalid or expired token")
```

---

### 5.3 Input Validation

**Backend Validation (Pydantic):**
```python
from pydantic import BaseModel, EmailStr, constr, validator

class RegisterRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    password_confirmation: str

    @validator("password")
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain a lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a number")
        if not any(c in "!@#$%^&*" for c in v):
            raise ValueError("Password must contain a special character")
        return v

    @validator("password_confirmation")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v
```

**Frontend Validation:**
- Same rules as backend, implemented in TypeScript
- Validate before sending request (user experience)
- Backend validation is authoritative (security)

---

### 5.4 SQL Injection Prevention

**Strategy:** Use ORM (SQLModel) with parameterized queries

**Example (Secure):**
```python
# SQLModel automatically parameterizes queries
task = db.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
```

**Never Do This (Vulnerable):**
```python
# NEVER use string formatting for SQL queries
query = f"SELECT * FROM tasks WHERE user_id = {user_id}"  # SQL INJECTION RISK
```

---

### 5.5 XSS Prevention

**Strategy:**
- React automatically escapes all rendered strings
- Never use `dangerouslySetInnerHTML` unless absolutely necessary
- Sanitize user input before rendering (if using HTML)

---

### 5.6 CSRF Protection

**Strategy:**
- Use httpOnly cookies for tokens (prevents JavaScript access)
- SameSite=Strict cookie attribute
- Alternative: Store tokens in localStorage (simpler for Phase II)

---

## 6. TESTING STRATEGY

### 6.1 Backend Testing (pytest)

**Test Coverage Target:** ≥80%

#### Test Files

1. **test_auth.py** - Authentication endpoints
   - Test user registration (valid, invalid email, duplicate email, weak password)
   - Test user login (valid credentials, invalid credentials)
   - Test token refresh (valid token, expired token)
   - Test logout

2. **test_tasks.py** - Task CRUD endpoints
   - Test create task (valid, invalid input, unauthorized)
   - Test get all tasks (returns only user's tasks)
   - Test get task by ID (authorized, unauthorized, not found)
   - Test update task (valid, unauthorized, not found)
   - Test delete task (valid, unauthorized, not found)
   - Test toggle task (valid, unauthorized, not found)

3. **test_user_isolation.py** - User data isolation
   - Test User A cannot view User B's tasks
   - Test User A cannot update User B's tasks
   - Test User A cannot delete User B's tasks
   - Test User A cannot toggle User B's tasks

---

#### Test Fixtures (conftest.py)

```python
import pytest
from sqlmodel import create_engine, Session
from fastapi.testclient import TestClient

@pytest.fixture
def db_session():
    # Create test database
    engine = create_engine("sqlite:///:memory:")
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(db_session):
    # Create test client with test DB
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_user(db_session):
    # Create test user
    user = User(email="test@example.com", hashed_password=hash_password("Test123!"))
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def auth_headers(test_user):
    # Generate auth headers for test user
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}
```

---

### 6.2 Frontend Testing (Jest + React Testing Library)

**Test Coverage Target:** ≥70%

#### Test Files

1. **RegisterPage.test.tsx** - Registration page
   - Test form validation (email, password, confirmation)
   - Test successful registration flow
   - Test error handling (duplicate email, server error)

2. **LoginPage.test.tsx** - Login page
   - Test form validation
   - Test successful login flow
   - Test error handling (invalid credentials, server error)

3. **Dashboard.test.tsx** - Dashboard page
   - Test protected route redirect
   - Test task list rendering
   - Test empty state rendering

4. **TaskCard.test.tsx** - TaskCard component
   - Test task rendering (complete, incomplete)
   - Test checkbox toggle
   - Test edit button click
   - Test delete button click

5. **AddTaskModal.test.tsx** - AddTaskModal component
   - Test form validation
   - Test successful submission
   - Test character counter
   - Test cancel button

---

## 7. ENVIRONMENT CONFIGURATION

### 7.1 Backend Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@host/dbname

# Security
SECRET_KEY=your-secret-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Environment
ENVIRONMENT=development
```

**Required:**
- `DATABASE_URL`: Neon PostgreSQL connection string
- `SECRET_KEY`: Random string ≥32 chars (used for JWT signing)

---

### 7.2 Frontend Environment Variables (.env.local)

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**Required:**
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL

---

## 8. DEPENDENCIES

### 8.1 Backend Dependencies (requirements.txt)

```txt
# Web Framework
fastapi==0.104.0
uvicorn[standard]==0.24.0

# Database
sqlmodel==0.0.14
psycopg2-binary==2.9.9
alembic==1.12.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Validation
pydantic[email]==2.5.0
email-validator==2.1.0

# Environment
python-dotenv==1.0.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1
pytest-cov==4.1.0

# Code Quality
ruff==0.1.6
black==23.11.0
```

---

### 8.2 Frontend Dependencies (package.json)

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "axios": "^1.6.0",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0",
    "prettier": "^3.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0"
  }
}
```

---

## 9. DEVELOPMENT WORKFLOW

### 9.1 Setup Steps

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with actual values (DATABASE_URL, SECRET_KEY)

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local
# Edit .env.local with API URL

# Start development server
npm run dev
```

---

### 9.2 Development Servers

- **Backend:** `http://localhost:8000`
  - API Docs (Swagger): `http://localhost:8000/docs`
  - Alternative Docs (ReDoc): `http://localhost:8000/redoc`

- **Frontend:** `http://localhost:3000`

---

### 9.3 Testing Commands

#### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

---

#### Frontend Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

---

### 9.4 Code Quality Commands

#### Backend Linting and Formatting

```bash
# Lint with Ruff
ruff check .

# Format with Black
black .

# Combined: Format then lint
black . && ruff check .
```

---

#### Frontend Linting and Formatting

```bash
# Lint with ESLint
npm run lint

# Format with Prettier
npm run format

# Type check
npm run type-check
```

---

## 10. DEPLOYMENT CONSIDERATIONS

### 10.1 Production Environment Variables

**Backend:**
- `DATABASE_URL`: Neon production connection string (with SSL)
- `SECRET_KEY`: Strong random key (different from dev)
- `CORS_ORIGINS`: Production frontend domain (e.g., `https://app.example.com`)
- `ENVIRONMENT=production`

**Frontend:**
- `NEXT_PUBLIC_API_BASE_URL`: Production backend URL (e.g., `https://api.example.com`)

---

### 10.2 Database Migrations

**Before Deployment:**
1. Test migrations on staging database
2. Backup production database
3. Run `alembic upgrade head` on production

---

### 10.3 Security Checklist

- [ ] SECRET_KEY is strong and unique
- [ ] DATABASE_URL uses SSL connection
- [ ] CORS_ORIGINS restricts to production frontend domain only
- [ ] All environment variables are set
- [ ] No secrets in source code
- [ ] HTTPS enabled for frontend and backend
- [ ] Password hashing with bcrypt (cost factor 12)
- [ ] JWT tokens have proper expiration times

---

## 11. SUCCESS CRITERIA

This implementation plan will be considered complete when:

1. **Architecture Defined:**
   - ✅ Database schema designed
   - ✅ API endpoints specified
   - ✅ Frontend structure defined
   - ✅ Authentication flow documented

2. **Technical Decisions Made:**
   - ✅ Tech stack confirmed (Next.js, FastAPI, SQLModel, Neon)
   - ✅ Security strategies defined (JWT, bcrypt, user isolation)
   - ✅ Error handling approach documented
   - ✅ Testing strategy defined

3. **Ready for Task Breakdown:**
   - ✅ All modules identified
   - ✅ All components specified
   - ✅ All dependencies listed
   - ✅ All endpoints documented

4. **Constitutional Compliance:**
   - ✅ No Phase III features (AI, NLP, agents)
   - ✅ Implements only PHASE_II_SPECIFICATION.md requirements
   - ✅ Uses approved technologies from Constitution v2.0
   - ✅ Maintains clean architecture principles

---

## 12. NEXT STEPS

After this plan is approved:

1. Create **PHASE_II_TASKS.md** - Break implementation into discrete tasks
2. Tasks will be organized by:
   - Backend setup tasks
   - Database schema tasks
   - Auth endpoint tasks
   - Task endpoint tasks
   - Frontend setup tasks
   - Page implementation tasks
   - Component implementation tasks
   - Testing tasks
   - Documentation tasks

Each task will have:
- Clear description
- Acceptance criteria
- Dependencies (which tasks must be completed first)
- Estimated complexity (small, medium, large)

---

## APPROVAL

**Plan Status:** DRAFT
**Constitutional Compliance:** VERIFIED (Constitution v2.0, PHASE_II_SPECIFICATION.md)
**Ready for Task Breakdown:** PENDING APPROVAL

**Next Steps:**
1. Review and approve this implementation plan
2. Create PHASE_II_TASKS.md (discrete task breakdown)
3. Begin implementation following constitutional workflow

---

**END OF PHASE II IMPLEMENTATION PLAN**

*This plan is subordinate to CONSTITUTION.md v2.0 and PHASE_II_SPECIFICATION.md and may only be amended through the constitutional amendment process.*
