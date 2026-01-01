# PHASE II IMPLEMENTATION TASKS

**Project:** Evolution of Todo
**Phase:** II - Full-Stack Web Application
**Version:** 1.0
**Status:** DRAFT
**Parent Documents:**
- CONSTITUTION.md v2.0
- PHASE_II_SPECIFICATION.md
- PHASE_II_PLAN.md
**Date:** 2026-01-01

---

## EXECUTIVE SUMMARY

This document breaks down the Phase II technical plan into atomic, sequential implementation tasks. Each task is independently implementable, testable, and verifiable against the specification. Phase II consists of 52 tasks organized into 8 major work streams: Project Setup, Database, Backend Auth, Backend Tasks, Frontend Setup, Frontend Pages, Frontend Components, and Testing & Documentation.

---

## CONSTITUTIONAL COMPLIANCE

This task breakdown is created under:
- **Article I, Section 1.4:** Task Requirements
- **Article II, Section 2.2:** Strict Specification Adherence
- **Article III, Section 3.1:** Phase Scope Boundaries (Full-Stack Web App, NO AI/Agents)
- **Article VIII, Section 8.2:** Phase II Provisions
- **Constitutional Workflow:** Constitution → Spec → Plan → **Tasks** → Code

All tasks implement ONLY what is specified in PHASE_II_SPECIFICATION.md and PHASE_II_PLAN.md.

---

## TASK STRUCTURE

Each task includes:
- **Task ID:** Unique identifier (P2-001, P2-002, etc.)
- **Title:** Clear, action-oriented description
- **Description:** What needs to be implemented
- **Preconditions:** What must exist before starting
- **Specification References:** Relevant spec sections
- **Plan References:** Relevant plan sections
- **Artifacts:** Files to create or modify
- **Acceptance Criteria:** How to verify completion
- **Estimated Complexity:** Small (1-2 hours), Medium (3-5 hours), Large (6-8 hours)
- **Dependencies:** Which tasks must complete first

---

## TASK OVERVIEW BY WORK STREAM

### 1. Project Setup (5 tasks)
- P2-001: Create project structure
- P2-002: Backend environment setup
- P2-003: Frontend environment setup
- P2-004: Database connection setup
- P2-005: Initialize Alembic migrations

### 2. Database Schema (3 tasks)
- P2-006: Create User SQLModel
- P2-007: Create Task SQLModel
- P2-008: Create initial database migration

### 3. Backend Core (5 tasks)
- P2-009: Implement password hashing utilities
- P2-010: Implement JWT generation and validation
- P2-011: Implement database session dependency
- P2-012: Implement get_current_user dependency
- P2-013: Create custom exceptions

### 4. Backend Auth Endpoints (5 tasks)
- P2-014: Create auth request/response schemas
- P2-015: Implement user service (register, login)
- P2-016: Implement POST /api/auth/register endpoint
- P2-017: Implement POST /api/auth/login endpoint
- P2-018: Implement POST /api/auth/logout and /api/auth/refresh endpoints

### 5. Backend Task Endpoints (6 tasks)
- P2-019: Create task request/response schemas
- P2-020: Implement task service with user isolation
- P2-021: Implement GET /api/tasks endpoint
- P2-022: Implement POST /api/tasks endpoint
- P2-023: Implement GET/PUT/DELETE /api/tasks/{id} endpoints
- P2-024: Implement PATCH /api/tasks/{id}/toggle endpoint

### 6. Frontend Core (7 tasks)
- P2-025: Create TypeScript type definitions
- P2-026: Implement API client with interceptors
- P2-027: Implement JWT storage utilities
- P2-028: Implement form validation utilities
- P2-029: Create AuthContext and provider
- P2-030: Create useAuth hook
- P2-031: Create useTasks hook

### 7. Frontend Pages & Components (11 tasks)
- P2-032: Create root layout
- P2-033: Create landing page (/)
- P2-034: Create register page (/register)
- P2-035: Create login page (/login)
- P2-036: Create dashboard page (/dashboard)
- P2-037: Create Navbar component
- P2-038: Create TaskCard component
- P2-039: Create TaskList component
- P2-040: Create AddTaskModal component
- P2-041: Create EditTaskModal component
- P2-042: Create DeleteConfirmModal component

### 8. Testing & Documentation (10 tasks)
- P2-043: Write backend auth tests
- P2-044: Write backend task CRUD tests
- P2-045: Write backend user isolation tests
- P2-046: Write frontend register page tests
- P2-047: Write frontend login page tests
- P2-048: Write frontend dashboard tests
- P2-049: Write frontend component tests
- P2-050: Run linting and formatting
- P2-051: Manual testing and bug fixes
- P2-052: Create README and documentation

---

## TASK DEPENDENCY GRAPH

```
[PROJECT SETUP]
P2-001 (Project Structure)
    ├─→ P2-002 (Backend Env Setup)
    │      ├─→ P2-004 (DB Connection)
    │      │      └─→ P2-005 (Init Alembic)
    │      │             └─→ P2-006 (User Model)
    │      │                    └─→ P2-007 (Task Model)
    │      │                           └─→ P2-008 (DB Migration)
    │      └─→ P2-009 (Password Hashing)
    │             └─→ P2-010 (JWT Utils)
    │                    └─→ P2-011 (DB Session Dep)
    │                           └─→ P2-012 (Current User Dep)
    │                                  └─→ P2-013 (Exceptions)
    │
    └─→ P2-003 (Frontend Env Setup)
           └─→ P2-025 (Type Definitions)
                  └─→ P2-026 (API Client)
                         └─→ P2-027 (JWT Storage)
                                └─→ P2-028 (Validation Utils)

[BACKEND AUTH FLOW]
P2-013 (Exceptions) → P2-014 (Auth Schemas)
                         └─→ P2-015 (User Service)
                                ├─→ P2-016 (Register Endpoint)
                                ├─→ P2-017 (Login Endpoint)
                                └─→ P2-018 (Logout/Refresh Endpoints)

[BACKEND TASKS FLOW]
P2-012 (Current User Dep) → P2-019 (Task Schemas)
                                └─→ P2-020 (Task Service)
                                       ├─→ P2-021 (GET /api/tasks)
                                       ├─→ P2-022 (POST /api/tasks)
                                       ├─→ P2-023 (GET/PUT/DELETE /api/tasks/{id})
                                       └─→ P2-024 (PATCH /api/tasks/{id}/toggle)

[FRONTEND AUTH FLOW]
P2-028 (Validation Utils) → P2-029 (AuthContext)
                               └─→ P2-030 (useAuth Hook)
                                      ├─→ P2-032 (Root Layout)
                                      ├─→ P2-033 (Landing Page)
                                      ├─→ P2-034 (Register Page)
                                      └─→ P2-035 (Login Page)

[FRONTEND TASKS FLOW]
P2-030 (useAuth Hook) → P2-031 (useTasks Hook)
                           └─→ P2-036 (Dashboard Page)
                                  ├─→ P2-037 (Navbar)
                                  ├─→ P2-038 (TaskCard)
                                  ├─→ P2-039 (TaskList)
                                  ├─→ P2-040 (AddTaskModal)
                                  ├─→ P2-041 (EditTaskModal)
                                  └─→ P2-042 (DeleteConfirmModal)

[TESTING FLOW]
P2-018 (Auth Endpoints) ──┐
P2-024 (Task Endpoints) ──┼─→ P2-043 (Backend Auth Tests)
                          │   ├─→ P2-044 (Backend Task Tests)
                          │   └─→ P2-045 (Backend Isolation Tests)
                          │
P2-042 (All Components) ──┼─→ P2-046 (Register Page Tests)
                          │   ├─→ P2-047 (Login Page Tests)
                          │   ├─→ P2-048 (Dashboard Tests)
                          │   └─→ P2-049 (Component Tests)
                          │
All Code Complete ────────┴─→ P2-050 (Linting/Formatting)
                               └─→ P2-051 (Manual Testing)
                                      └─→ P2-052 (Documentation)
                                             └─→ [PHASE II COMPLETE]
```

---

## DETAILED TASK SPECIFICATIONS

---

## 1. PROJECT SETUP TASKS

---

### P2-001: Create Project Structure

**Title:** Set up Phase II project structure for backend and frontend

**Description:**
Create the complete directory structure for Phase II implementation including backend (FastAPI) and frontend (Next.js) directories with proper organization.

**Preconditions:**
- CONSTITUTION.md v2.0 exists
- PHASE_II_SPECIFICATION.md exists
- PHASE_II_PLAN.md exists
- Working directory is E:\heckathon-2

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Technology Stack" section

**Plan References:**
- PHASE_II_PLAN.md: Section 3.1 "Backend Project Structure"
- PHASE_II_PLAN.md: Section 4.1 "Frontend Project Structure"

**Artifacts to Create:**
```
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
├── alembic/
├── tests/
│   └── __init__.py
└── .gitignore

frontend/
├── src/
│   ├── app/
│   ├── components/
│   ├── contexts/
│   ├── hooks/
│   ├── lib/
│   ├── types/
│   └── utils/
├── public/
├── tests/
└── .gitignore
```

**Acceptance Criteria:**
- [ ] `backend/app/` directory structure created with all subdirectories
- [ ] All `__init__.py` files created in backend
- [ ] `frontend/src/` directory structure created with all subdirectories
- [ ] `.gitignore` files created for both backend and frontend
- [ ] Directory structure matches PHASE_II_PLAN.md specifications

**Estimated Complexity:** Small

**Dependencies:** None

---

### P2-002: Backend Environment Setup

**Title:** Configure backend Python environment and dependencies

**Description:**
Set up Python virtual environment, install required dependencies, and configure environment variables for the FastAPI backend.

**Preconditions:**
- P2-001 complete
- Python 3.11+ installed

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Technology Stack" section

**Plan References:**
- PHASE_II_PLAN.md: Section 8.1 "Backend Dependencies"
- PHASE_II_PLAN.md: Section 7.1 "Backend Environment Variables"

**Artifacts to Create:**
```
backend/requirements.txt
backend/.env.example
backend/.env (gitignored)
backend/pyproject.toml
```

**Implementation Requirements:**

**requirements.txt:**
```txt
fastapi==0.104.0
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
alembic==1.12.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic[email]==2.5.0
email-validator==2.1.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1
pytest-cov==4.1.0
ruff==0.1.6
black==23.11.0
```

**.env.example:**
```bash
DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=your-secret-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

**pyproject.toml:**
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
```

**Acceptance Criteria:**
- [ ] `requirements.txt` created with all dependencies
- [ ] `.env.example` created with all required variables
- [ ] `.env` created (with placeholder values)
- [ ] `pyproject.toml` created with Ruff and Black configuration
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Can import FastAPI: `python -c "import fastapi"`

**Estimated Complexity:** Small

**Dependencies:** P2-001

---

### P2-003: Frontend Environment Setup

**Title:** Initialize Next.js frontend with TypeScript and dependencies

**Description:**
Initialize Next.js project with App Router, TypeScript, and install required dependencies including axios, testing libraries, and linting tools.

**Preconditions:**
- P2-001 complete
- Node.js 18+ and npm installed

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Technology Stack" section

**Plan References:**
- PHASE_II_PLAN.md: Section 8.2 "Frontend Dependencies"
- PHASE_II_PLAN.md: Section 7.2 "Frontend Environment Variables"

**Artifacts to Create:**
```
frontend/package.json
frontend/.env.local.example
frontend/.env.local (gitignored)
frontend/next.config.js
frontend/tsconfig.json
frontend/.eslintrc.json
frontend/.prettierrc
```

**Implementation Requirements:**

**Initialize Next.js:**
```bash
cd frontend
npx create-next-app@latest . --typescript --app --no-tailwind --eslint
```

**Install additional dependencies:**
```bash
npm install axios
npm install -D jest @testing-library/react @testing-library/jest-dom prettier
```

**.env.local.example:**
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**next.config.js:**
```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
```

**Acceptance Criteria:**
- [ ] Next.js project initialized with App Router
- [ ] TypeScript configured
- [ ] `package.json` has all required dependencies
- [ ] `.env.local.example` created
- [ ] `.env.local` created with API base URL
- [ ] ESLint and Prettier configured
- [ ] Can run dev server: `npm run dev`

**Estimated Complexity:** Small

**Dependencies:** P2-001

---

### P2-004: Database Connection Setup

**Title:** Implement database connection and session management

**Description:**
Create database.py module with SQLModel engine, session factory, and connection utilities for Neon PostgreSQL.

**Preconditions:**
- P2-002 complete
- Neon PostgreSQL database created

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Data Model" section

**Plan References:**
- PHASE_II_PLAN.md: Section 2 "Database Design"
- PHASE_II_PLAN.md: Section 3.2 "Module Responsibilities"

**Artifacts to Create:**
```
backend/app/database.py
backend/app/config.py
```

**Implementation Requirements:**

**app/config.py:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
```

**app/database.py:**
```python
from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session
```

**Acceptance Criteria:**
- [ ] `config.py` created with Settings class
- [ ] `database.py` created with engine and session factory
- [ ] Settings loads from .env correctly
- [ ] Can create engine without errors
- [ ] `get_session()` dependency works

**Estimated Complexity:** Small

**Dependencies:** P2-002

---

### P2-005: Initialize Alembic Migrations

**Title:** Set up Alembic for database migrations

**Description:**
Initialize Alembic migration tool and configure it to work with SQLModel and Neon PostgreSQL.

**Preconditions:**
- P2-004 complete
- Alembic installed via requirements.txt

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Data Model" section

**Plan References:**
- PHASE_II_PLAN.md: Section 2.3 "Database Migrations"

**Artifacts to Create:**
```
backend/alembic.ini
backend/alembic/env.py
backend/alembic/versions/ (directory)
```

**Implementation Requirements:**

```bash
cd backend
alembic init alembic
```

**Edit alembic.ini:**
```ini
sqlalchemy.url = # Leave empty, will use config from env.py
```

**Edit alembic/env.py:**
```python
from app.config import settings
from app.database import engine
from sqlmodel import SQLModel

# Import all models
from app.models.user import User
from app.models.task import Task

target_metadata = SQLModel.metadata
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

**Acceptance Criteria:**
- [ ] Alembic initialized in `backend/alembic/`
- [ ] `alembic.ini` configured
- [ ] `alembic/env.py` configured with SQLModel metadata
- [ ] Can run: `alembic revision --autogenerate -m "test"`
- [ ] Can run: `alembic upgrade head`

**Estimated Complexity:** Small

**Dependencies:** P2-004

---

## 2. DATABASE SCHEMA TASKS

---

### P2-006: Create User SQLModel

**Title:** Implement User model with SQLModel

**Description:**
Create the User SQLModel class with all required fields, constraints, and relationship to tasks.

**Preconditions:**
- P2-005 complete

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Data Requirements" section (User Data)

**Plan References:**
- PHASE_II_PLAN.md: Section 2.2 "SQLModel Definitions" (User Model)

**Artifacts to Create:**
```
backend/app/models/user.py
```

**Implementation Requirements:**

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

**Acceptance Criteria:**
- [ ] `app/models/user.py` created
- [ ] User model has all required fields
- [ ] Email field is unique and indexed
- [ ] created_at and updated_at have defaults
- [ ] Relationship to Task defined
- [ ] Can import: `from app.models.user import User`

**Estimated Complexity:** Small

**Dependencies:** P2-005

---

### P2-007: Create Task SQLModel

**Title:** Implement Task model with SQLModel and user relationship

**Description:**
Create the Task SQLModel class with all required fields, foreign key to User, and relationship configuration.

**Preconditions:**
- P2-006 complete

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Data Requirements" section (Task Data)

**Plan References:**
- PHASE_II_PLAN.md: Section 2.2 "SQLModel Definitions" (Task Model)

**Artifacts to Create:**
```
backend/app/models/task.py
```

**Implementation Requirements:**

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=500, min_length=1)
    is_complete: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")
```

**Acceptance Criteria:**
- [ ] `app/models/task.py` created
- [ ] Task model has all required fields
- [ ] user_id foreign key to users.id
- [ ] user_id is indexed
- [ ] description has min/max length constraints
- [ ] is_complete defaults to False
- [ ] Relationship to User defined
- [ ] Can import: `from app.models.task import Task`

**Estimated Complexity:** Small

**Dependencies:** P2-006

---

### P2-008: Create Initial Database Migration

**Title:** Generate and apply initial migration for users and tasks tables

**Description:**
Use Alembic to generate the initial migration that creates users and tasks tables with all indexes and constraints.

**Preconditions:**
- P2-007 complete
- Database connection configured

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Data Model" section

**Plan References:**
- PHASE_II_PLAN.md: Section 2.1 "Schema Design"
- PHASE_II_PLAN.md: Section 2.3 "Database Migrations"

**Artifacts to Create:**
```
backend/alembic/versions/001_create_users_and_tasks.py
```

**Implementation Requirements:**

```bash
cd backend
alembic revision --autogenerate -m "Create users and tasks tables"
alembic upgrade head
```

**Migration should create:**
- users table with id, email (unique, indexed), hashed_password, timestamps
- tasks table with id, description, is_complete, user_id (FK, indexed), timestamps
- Foreign key constraint: tasks.user_id → users.id with ON DELETE CASCADE

**Acceptance Criteria:**
- [ ] Migration file created in alembic/versions/
- [ ] Migration includes users table creation
- [ ] Migration includes tasks table creation
- [ ] Email index created on users table
- [ ] user_id index created on tasks table
- [ ] Foreign key constraint defined
- [ ] Migration runs successfully: `alembic upgrade head`
- [ ] Tables exist in database (verify with SQL client)

**Estimated Complexity:** Medium

**Dependencies:** P2-007

---

## 3. BACKEND CORE TASKS

---

### P2-009: Implement Password Hashing Utilities

**Title:** Create password hashing and verification functions with bcrypt

**Description:**
Implement secure password hashing using passlib with bcrypt, including hash and verify functions.

**Preconditions:**
- P2-002 complete (passlib installed)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-201 (password hashing requirement)

**Plan References:**
- PHASE_II_PLAN.md: Section 5.1 "Password Hashing"

**Artifacts to Create:**
```
backend/app/core/security.py
```

**Implementation Requirements:**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
```

**Acceptance Criteria:**
- [ ] `app/core/security.py` created
- [ ] `hash_password()` function implemented
- [ ] `verify_password()` function implemented
- [ ] Hashing uses bcrypt with cost factor 12 (default)
- [ ] Test: Hash password and verify returns True
- [ ] Test: Wrong password verification returns False
- [ ] Docstrings present for both functions

**Estimated Complexity:** Small

**Dependencies:** P2-002

---

### P2-010: Implement JWT Generation and Validation

**Title:** Create JWT token generation and verification utilities

**Description:**
Implement JWT access token and refresh token generation, validation, and payload extraction using python-jose.

**Preconditions:**
- P2-009 complete

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-202 (JWT tokens)

**Plan References:**
- PHASE_II_PLAN.md: Section 5.2 "JWT Implementation"

**Artifacts to Update:**
```
backend/app/core/security.py
```

**Implementation Requirements:**

Add to `app/core/security.py`:

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import settings

def create_access_token(user_id: int) -> str:
    """
    Generate JWT access token.

    Args:
        user_id: User ID to encode in token

    Returns:
        JWT token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    """
    Generate JWT refresh token.

    Args:
        user_id: User ID to encode in token

    Returns:
        JWT refresh token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token.

    Args:
        token: JWT token string

    Returns:
        Token payload dict

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
```

**Acceptance Criteria:**
- [ ] `create_access_token()` function implemented
- [ ] `create_refresh_token()` function implemented
- [ ] `verify_token()` function implemented
- [ ] Access token expires in 15 minutes
- [ ] Refresh token expires in 7 days
- [ ] Test: Generate token and verify returns payload
- [ ] Test: Expired token raises error
- [ ] Test: Invalid token raises error
- [ ] Docstrings present for all functions

**Estimated Complexity:** Medium

**Dependencies:** P2-009

---

### P2-011: Implement Database Session Dependency

**Title:** Create FastAPI dependency for database session injection

**Description:**
Implement get_db() dependency function for FastAPI endpoints to receive database sessions.

**Preconditions:**
- P2-004 complete (database.py exists)

**Specification References:**
- PHASE_II_SPECIFICATION.md: API endpoints require database access

**Plan References:**
- PHASE_II_PLAN.md: Section 3.2 "Module Responsibilities" (api/deps.py)

**Artifacts to Create:**
```
backend/app/api/deps.py
```

**Implementation Requirements:**

```python
from sqlmodel import Session
from typing import Generator
from app.database import get_session

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.

    Yields:
        Database session
    """
    return get_session()
```

**Acceptance Criteria:**
- [ ] `app/api/deps.py` created
- [ ] `get_db()` dependency implemented
- [ ] Returns database session generator
- [ ] Can be used in FastAPI endpoint with `Depends(get_db)`

**Estimated Complexity:** Small

**Dependencies:** P2-004

---

### P2-012: Implement Get Current User Dependency

**Title:** Create FastAPI dependency for authenticated user extraction from JWT

**Description:**
Implement get_current_user() dependency that extracts and validates JWT from Authorization header, verifies token, and returns authenticated user from database.

**Preconditions:**
- P2-010 complete (JWT verification)
- P2-011 complete (DB session dependency)
- P2-006 complete (User model)

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Authentication and Authorization Behavior"

**Plan References:**
- PHASE_II_PLAN.md: Section 3.6 "Authorization Middleware"

**Artifacts to Update:**
```
backend/app/api/deps.py
```

**Implementation Requirements:**

Add to `app/api/deps.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.models.user import User

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get currently authenticated user.

    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session

    Returns:
        Authenticated user object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

**Acceptance Criteria:**
- [ ] `get_current_user()` dependency implemented in deps.py
- [ ] Extracts token from Authorization header
- [ ] Verifies token using verify_token()
- [ ] Queries user from database by user_id
- [ ] Returns User object if valid
- [ ] Raises 401 if token missing/invalid
- [ ] Raises 401 if token expired
- [ ] Raises 401 if user not found
- [ ] Docstring present

**Estimated Complexity:** Medium

**Dependencies:** P2-010, P2-011, P2-006

---

### P2-013: Create Custom Exceptions

**Title:** Define custom exception classes for application errors

**Description:**
Create custom exception classes for common error scenarios (NotFound, Unauthorized, Forbidden, Validation) with exception handlers.

**Preconditions:**
- P2-002 complete

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Error and Edge Cases" section

**Plan References:**
- PHASE_II_PLAN.md: Section 3.8 "Error Handling Strategy"

**Artifacts to Create:**
```
backend/app/core/exceptions.py
```

**Implementation Requirements:**

```python
class NotFoundError(Exception):
    """Raised when a resource is not found."""
    pass

class UnauthorizedError(Exception):
    """Raised when authentication fails."""
    pass

class ForbiddenError(Exception):
    """Raised when user lacks permission."""
    pass

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass
```

**Exception handlers (to be added to main.py later):**

```python
from fastapi.responses import JSONResponse

@app.exception_handler(NotFoundError)
def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

# Similar handlers for other exceptions
```

**Acceptance Criteria:**
- [ ] `app/core/exceptions.py` created
- [ ] NotFoundError defined
- [ ] UnauthorizedError defined
- [ ] ForbiddenError defined
- [ ] ValidationError defined
- [ ] All exceptions inherit from Exception
- [ ] Can raise and catch exceptions

**Estimated Complexity:** Small

**Dependencies:** P2-002

---

## 4. BACKEND AUTH ENDPOINTS TASKS

---

### P2-014: Create Auth Request/Response Schemas

**Title:** Define Pydantic schemas for authentication endpoints

**Description:**
Create Pydantic request and response schemas for register, login, and token refresh endpoints with validation.

**Preconditions:**
- P2-002 complete (Pydantic installed)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-201, US-202 (registration, login)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.4 "Request/Response Schemas" (Auth Schemas)

**Artifacts to Create:**
```
backend/app/schemas/auth.py
```

**Implementation Requirements:**

```python
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional

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

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: str

    class Config:
        from_attributes = True
```

**Acceptance Criteria:**
- [ ] `app/schemas/auth.py` created
- [ ] RegisterRequest schema with email, password, password_confirmation
- [ ] Password validation (8+ chars, uppercase, lowercase, digit, special)
- [ ] Password confirmation match validation
- [ ] LoginRequest schema with email, password
- [ ] TokenResponse schema with tokens and expiration
- [ ] RefreshTokenRequest schema
- [ ] UserResponse schema (no password field)
- [ ] All schemas have proper types

**Estimated Complexity:** Medium

**Dependencies:** P2-002

---

### P2-015: Implement User Service

**Title:** Create user service with registration and authentication logic

**Description:**
Implement UserService class with methods for user registration, login authentication, and user lookup with business logic and error handling.

**Preconditions:**
- P2-009 complete (password hashing)
- P2-013 complete (exceptions)
- P2-006 complete (User model)
- P2-014 complete (auth schemas)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-201 (registration), US-202 (login)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.2 "Module Responsibilities" (services/user_service.py)

**Artifacts to Create:**
```
backend/app/services/user_service.py
```

**Implementation Requirements:**

```python
from sqlmodel import Session, select
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.exceptions import ValidationError, UnauthorizedError
from fastapi import HTTPException, status

def create_user(db: Session, email: str, password: str) -> User:
    """
    Create a new user.

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        Created user object

    Raises:
        HTTPException: If email already exists
    """
    # Check if email already exists
    existing_user = db.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    # Hash password
    hashed_password = hash_password(password)

    # Create user
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticate user by email and password.

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        Authenticated user object

    Raises:
        HTTPException: If credentials are invalid
    """
    user = db.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return user

def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User object

    Raises:
        HTTPException: If user not found
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

**Acceptance Criteria:**
- [ ] `app/services/user_service.py` created
- [ ] `create_user()` function implemented
- [ ] Email uniqueness check implemented
- [ ] Password hashing implemented
- [ ] `authenticate_user()` function implemented
- [ ] Generic error message for invalid credentials (security)
- [ ] `get_user_by_id()` function implemented
- [ ] All functions have docstrings
- [ ] Proper error handling with HTTPException

**Estimated Complexity:** Medium

**Dependencies:** P2-009, P2-013, P2-006, P2-014

---

### P2-016: Implement POST /api/auth/register Endpoint

**Title:** Create user registration API endpoint

**Description:**
Implement FastAPI endpoint for user registration that validates input, creates user, and returns user data.

**Preconditions:**
- P2-015 complete (user service)
- P2-014 complete (auth schemas)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-201 (User Registration)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.3 "API Endpoints" (POST /api/auth/register)

**Artifacts to Create:**
```
backend/app/api/routes/auth.py
backend/app/main.py (update)
```

**Implementation Requirements:**

**app/api/routes/auth.py:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.auth import RegisterRequest, UserResponse
from app.services.user_service import create_user
from app.api.deps import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    Args:
        request: Registration request with email, password, password_confirmation
        db: Database session

    Returns:
        Created user data (without password)

    Raises:
        409: Email already exists
        400: Validation error
    """
    user = create_user(db, email=request.email, password=request.password)
    return user
```

**app/main.py:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import auth

app = FastAPI(title="Todo API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Todo API Phase II"}
```

**Acceptance Criteria:**
- [ ] `app/api/routes/auth.py` created with router
- [ ] POST /api/auth/register endpoint implemented
- [ ] Endpoint uses RegisterRequest schema
- [ ] Endpoint returns UserResponse (201 Created)
- [ ] Endpoint validates password strength via schema
- [ ] Endpoint checks password confirmation match
- [ ] Returns 409 if email already exists
- [ ] Returns 400 for validation errors
- [ ] `app/main.py` created with FastAPI app
- [ ] Auth router included in main app
- [ ] CORS middleware configured
- [ ] Can start server: `uvicorn app.main:app --reload`
- [ ] Can register user via POST request

**Estimated Complexity:** Medium

**Dependencies:** P2-015, P2-014

---

### P2-017: Implement POST /api/auth/login Endpoint

**Title:** Create user login API endpoint with JWT token generation

**Description:**
Implement FastAPI endpoint for user login that authenticates credentials and returns JWT tokens.

**Preconditions:**
- P2-016 complete (register endpoint exists)
- P2-010 complete (JWT generation)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-202 (User Login)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.3 "API Endpoints" (POST /api/auth/login)
- PHASE_II_PLAN.md: Section 3.5 "Authentication Flow" (Login Flow)

**Artifacts to Update:**
```
backend/app/api/routes/auth.py
```

**Implementation Requirements:**

Add to `app/api/routes/auth.py`:

```python
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user_service import authenticate_user
from app.core.security import create_access_token, create_refresh_token
from app.config import settings

@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user and return JWT tokens.

    Args:
        request: Login request with email and password
        db: Database session

    Returns:
        Access token, refresh token, and expiration

    Raises:
        401: Invalid credentials
    """
    user = authenticate_user(db, email=request.email, password=request.password)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    )
```

**Acceptance Criteria:**
- [ ] POST /api/auth/login endpoint implemented
- [ ] Endpoint uses LoginRequest schema
- [ ] Endpoint authenticates user via user_service
- [ ] Generates access token (15 min expiration)
- [ ] Generates refresh token (7 day expiration)
- [ ] Returns TokenResponse with both tokens
- [ ] Returns 401 for invalid credentials
- [ ] Generic error message (doesn't reveal if email or password wrong)
- [ ] Can login with registered user via POST request
- [ ] Tokens are valid JWT format

**Estimated Complexity:** Medium

**Dependencies:** P2-016, P2-010

---

### P2-018: Implement Logout and Refresh Token Endpoints

**Title:** Create logout and token refresh API endpoints

**Description:**
Implement POST /api/auth/logout and POST /api/auth/refresh endpoints for logging out and refreshing access tokens.

**Preconditions:**
- P2-017 complete (login endpoint)
- P2-012 complete (get_current_user dependency)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-203 (logout), US-204 (token refresh)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.3 "API Endpoints" (logout, refresh)
- PHASE_II_PLAN.md: Section 3.5 "Authentication Flow"

**Artifacts to Update:**
```
backend/app/api/routes/auth.py
```

**Implementation Requirements:**

Add to `app/api/routes/auth.py`:

```python
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.auth import RefreshTokenRequest

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client-side token invalidation).

    Args:
        current_user: Currently authenticated user

    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token.

    Args:
        request: Refresh token request

    Returns:
        New access token

    Raises:
        401: Invalid or expired refresh token
    """
    try:
        payload = verify_token(request.refresh_token)
        user_id = payload.get("user_id")
        token_type = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # Generate new access token
        new_access_token = create_access_token(user_id)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=request.refresh_token,  # Return same refresh token
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
```

**Acceptance Criteria:**
- [ ] POST /api/auth/logout endpoint implemented
- [ ] Logout requires authentication (uses get_current_user)
- [ ] Logout returns success message
- [ ] POST /api/auth/refresh endpoint implemented
- [ ] Refresh validates refresh token
- [ ] Refresh checks token type is "refresh"
- [ ] Refresh generates new access token
- [ ] Refresh returns new access token with same refresh token
- [ ] Returns 401 for invalid/expired refresh token
- [ ] Can logout with valid access token
- [ ] Can refresh access token with valid refresh token

**Estimated Complexity:** Medium

**Dependencies:** P2-017, P2-012

---

## 5. BACKEND TASK ENDPOINTS TASKS

---

### P2-019: Create Task Request/Response Schemas

**Title:** Define Pydantic schemas for task endpoints

**Description:**
Create Pydantic request and response schemas for task CRUD operations with validation.

**Preconditions:**
- P2-002 complete (Pydantic installed)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-205 through US-209 (task operations)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.4 "Request/Response Schemas" (Task Schemas)

**Artifacts to Create:**
```
backend/app/schemas/task.py
```

**Implementation Requirements:**

```python
from pydantic import BaseModel, constr, validator
from typing import List

class TaskCreate(BaseModel):
    description: constr(min_length=1, max_length=500)

    @validator("description")
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError("Task description cannot be empty")
        return v.strip()

class TaskUpdate(BaseModel):
    description: constr(min_length=1, max_length=500)

    @validator("description")
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError("Task description cannot be empty")
        return v.strip()

class TaskResponse(BaseModel):
    id: int
    description: str
    is_complete: bool
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
```

**Acceptance Criteria:**
- [ ] `app/schemas/task.py` created
- [ ] TaskCreate schema with description (1-500 chars)
- [ ] TaskUpdate schema with description (1-500 chars)
- [ ] Description validation strips whitespace
- [ ] Description validation rejects empty strings
- [ ] TaskResponse schema with all task fields
- [ ] TaskListResponse schema with tasks array and total count
- [ ] All schemas have proper types

**Estimated Complexity:** Small

**Dependencies:** P2-002

---

### P2-020: Implement Task Service with User Isolation

**Title:** Create task service with CRUD operations and user isolation enforcement

**Description:**
Implement TaskService class with methods for task CRUD operations, ensuring all queries filter by user_id for data isolation.

**Preconditions:**
- P2-007 complete (Task model)
- P2-013 complete (exceptions)
- P2-019 complete (task schemas)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-205 through US-209 (task operations)
- PHASE_II_SPECIFICATION.md: "Authentication and Authorization Behavior"

**Plan References:**
- PHASE_II_PLAN.md: Section 3.7 "User Data Isolation Strategy"

**Artifacts to Create:**
```
backend/app/services/task_service.py
```

**Implementation Requirements:**

```python
from sqlmodel import Session, select
from app.models.task import Task
from fastapi import HTTPException, status
from datetime import datetime
from typing import List

def get_user_tasks(db: Session, user_id: int) -> List[Task]:
    """
    Get all tasks for a user.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        List of user's tasks
    """
    tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
    return list(tasks)

def create_task(db: Session, user_id: int, description: str) -> Task:
    """
    Create a new task for a user.

    Args:
        db: Database session
        user_id: User ID
        description: Task description

    Returns:
        Created task
    """
    task = Task(description=description, user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task:
    """
    Get a specific task by ID (with user isolation check).

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID

    Returns:
        Task object

    Raises:
        HTTPException: If task not found or belongs to different user
    """
    task = db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

def update_task(db: Session, task_id: int, user_id: int, description: str) -> Task:
    """
    Update a task's description (with user isolation check).

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID
        description: New description

    Returns:
        Updated task

    Raises:
        HTTPException: If task not found or belongs to different user
    """
    task = get_task_by_id(db, task_id, user_id)
    task.description = description
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int) -> None:
    """
    Delete a task (with user isolation check).

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID

    Raises:
        HTTPException: If task not found or belongs to different user
    """
    task = get_task_by_id(db, task_id, user_id)
    db.delete(task)
    db.commit()

def toggle_task(db: Session, task_id: int, user_id: int) -> Task:
    """
    Toggle a task's completion status (with user isolation check).

    Args:
        db: Database session
        task_id: Task ID
        user_id: User ID

    Returns:
        Updated task

    Raises:
        HTTPException: If task not found or belongs to different user
    """
    task = get_task_by_id(db, task_id, user_id)
    task.is_complete = not task.is_complete
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task
```

**Acceptance Criteria:**
- [ ] `app/services/task_service.py` created
- [ ] `get_user_tasks()` filters by user_id
- [ ] `create_task()` associates task with user_id
- [ ] `get_task_by_id()` filters by both task_id AND user_id
- [ ] `update_task()` enforces user ownership
- [ ] `delete_task()` enforces user ownership
- [ ] `toggle_task()` enforces user ownership
- [ ] All functions have docstrings
- [ ] 404 returned if task not found OR belongs to different user
- [ ] updated_at timestamp updated on modifications

**Estimated Complexity:** Medium

**Dependencies:** P2-007, P2-013, P2-019

---

### P2-021: Implement GET /api/tasks Endpoint

**Title:** Create endpoint to retrieve all tasks for authenticated user

**Description:**
Implement FastAPI endpoint to get all tasks belonging to the authenticated user.

**Preconditions:**
- P2-020 complete (task service)
- P2-012 complete (get_current_user dependency)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-204 (View Personal Task List)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.3 "API Endpoints" (GET /api/tasks)

**Artifacts to Create:**
```
backend/app/api/routes/tasks.py
backend/app/main.py (update to include router)
```

**Implementation Requirements:**

**app/api/routes/tasks.py:**
```python
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.task import TaskListResponse, TaskResponse
from app.services.task_service import get_user_tasks
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("", response_model=TaskListResponse)
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the authenticated user.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        List of tasks and total count

    Requires:
        Valid JWT token in Authorization header
    """
    tasks = get_user_tasks(db, user_id=current_user.id)
    return TaskListResponse(
        tasks=[TaskResponse.from_orm(task) for task in tasks],
        total=len(tasks)
    )
```

**Update app/main.py:**
```python
from app.api.routes import tasks

app.include_router(tasks.router)
```

**Acceptance Criteria:**
- [ ] `app/api/routes/tasks.py` created with router
- [ ] GET /api/tasks endpoint implemented
- [ ] Endpoint requires authentication (uses get_current_user)
- [ ] Endpoint returns TaskListResponse
- [ ] Only returns tasks for authenticated user
- [ ] Returns empty array if user has no tasks
- [ ] Returns 401 if no/invalid JWT token
- [ ] Tasks router included in main app
- [ ] Can retrieve tasks via GET request with JWT

**Estimated Complexity:** Small

**Dependencies:** P2-020, P2-012

---

### P2-022: Implement POST /api/tasks Endpoint

**Title:** Create endpoint to add new task for authenticated user

**Description:**
Implement FastAPI endpoint to create a new task associated with the authenticated user.

**Preconditions:**
- P2-021 complete (tasks router exists)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-205 (Create a New Task)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.3 "API Endpoints" (POST /api/tasks)

**Artifacts to Update:**
```
backend/app/api/routes/tasks.py
```

**Implementation Requirements:**

Add to `app/api/routes/tasks.py`:

```python
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import create_task
from fastapi import status

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    request: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.

    Args:
        request: Task creation request with description
        current_user: Authenticated user
        db: Database session

    Returns:
        Created task

    Requires:
        Valid JWT token in Authorization header

    Raises:
        400: Validation error (empty or too long description)
        401: Not authenticated
    """
    task = create_task(db, user_id=current_user.id, description=request.description)
    return TaskResponse.from_orm(task)
```

**Acceptance Criteria:**
- [ ] POST /api/tasks endpoint implemented
- [ ] Endpoint requires authentication
- [ ] Endpoint uses TaskCreate schema
- [ ] Endpoint returns TaskResponse (201 Created)
- [ ] Task is associated with current_user.id
- [ ] Task defaults to is_complete=False
- [ ] Returns 400 for empty description
- [ ] Returns 400 for description >500 chars
- [ ] Returns 401 if no/invalid JWT token
- [ ] Can create task via POST request with JWT

**Estimated Complexity:** Small

**Dependencies:** P2-021

---

### P2-023: Implement GET/PUT/DELETE /api/tasks/{id} Endpoints

**Title:** Create endpoints for retrieving, updating, and deleting specific tasks

**Description:**
Implement FastAPI endpoints for getting, updating, and deleting a task by ID with user isolation enforcement.

**Preconditions:**
- P2-022 complete (POST /api/tasks exists)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-206 (Update Task), US-207 (Delete Task)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.3 "API Endpoints"

**Artifacts to Update:**
```
backend/app/api/routes/tasks.py
```

**Implementation Requirements:**

Add to `app/api/routes/tasks.py`:

```python
from app.schemas.task import TaskUpdate
from app.services.task_service import get_task_by_id, update_task, delete_task

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.

    Args:
        task_id: Task ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Task data

    Raises:
        401: Not authenticated
        404: Task not found or belongs to different user
    """
    task = get_task_by_id(db, task_id=task_id, user_id=current_user.id)
    return TaskResponse.from_orm(task)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    request: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task's description.

    Args:
        task_id: Task ID
        request: Task update request with new description
        current_user: Authenticated user
        db: Database session

    Returns:
        Updated task

    Raises:
        400: Validation error
        401: Not authenticated
        404: Task not found or belongs to different user
    """
    task = update_task(db, task_id=task_id, user_id=current_user.id, description=request.description)
    return TaskResponse.from_orm(task)

@router.delete("/{task_id}")
def delete_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task.

    Args:
        task_id: Task ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Success message

    Raises:
        401: Not authenticated
        404: Task not found or belongs to different user
    """
    delete_task(db, task_id=task_id, user_id=current_user.id)
    return {"message": "Task deleted successfully"}
```

**Acceptance Criteria:**
- [ ] GET /api/tasks/{id} endpoint implemented
- [ ] PUT /api/tasks/{id} endpoint implemented
- [ ] DELETE /api/tasks/{id} endpoint implemented
- [ ] All endpoints require authentication
- [ ] All endpoints enforce user isolation (404 if wrong user)
- [ ] GET returns task data
- [ ] PUT updates description and returns updated task
- [ ] DELETE removes task and returns success message
- [ ] Returns 404 if task not found
- [ ] Returns 404 if task belongs to different user (security)
- [ ] Can get/update/delete own tasks via requests with JWT

**Estimated Complexity:** Medium

**Dependencies:** P2-022

---

### P2-024: Implement PATCH /api/tasks/{id}/toggle Endpoint

**Title:** Create endpoint to toggle task completion status

**Description:**
Implement FastAPI endpoint to toggle a task's is_complete status between true and false with user isolation.

**Preconditions:**
- P2-023 complete (other task endpoints exist)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-208 (Mark Task Complete/Incomplete)

**Plan References:**
- PHASE_II_PLAN.md: Section 3.3 "API Endpoints" (PATCH /api/tasks/{id}/toggle)

**Artifacts to Update:**
```
backend/app/api/routes/tasks.py
```

**Implementation Requirements:**

Add to `app/api/routes/tasks.py`:

```python
from app.services.task_service import toggle_task

@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_endpoint(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle a task's completion status.

    Args:
        task_id: Task ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Updated task with toggled is_complete status

    Raises:
        401: Not authenticated
        404: Task not found or belongs to different user
    """
    task = toggle_task(db, task_id=task_id, user_id=current_user.id)
    return TaskResponse.from_orm(task)
```

**Acceptance Criteria:**
- [ ] PATCH /api/tasks/{id}/toggle endpoint implemented
- [ ] Endpoint requires authentication
- [ ] Endpoint toggles is_complete (false → true, true → false)
- [ ] Endpoint returns updated task
- [ ] Endpoint enforces user isolation
- [ ] Returns 404 if task not found
- [ ] Returns 404 if task belongs to different user
- [ ] Can toggle task via PATCH request with JWT

**Estimated Complexity:** Small

**Dependencies:** P2-023

---

## 6. FRONTEND CORE TASKS

---

### P2-025: Create TypeScript Type Definitions

**Title:** Define TypeScript types for User and Task entities

**Description:**
Create TypeScript type definitions for User, Task, and related data structures.

**Preconditions:**
- P2-003 complete (frontend environment setup)

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Data Requirements" section

**Plan References:**
- PHASE_II_PLAN.md: Section 4.1 "Frontend Project Structure" (types/)

**Artifacts to Create:**
```
frontend/src/types/user.ts
frontend/src/types/task.ts
```

**Implementation Requirements:**

**src/types/user.ts:**
```typescript
export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

export interface RegisterData {
  email: string;
  password: string;
  password_confirmation: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}
```

**src/types/task.ts:**
```typescript
export interface Task {
  id: number;
  description: string;
  is_complete: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}
```

**Acceptance Criteria:**
- [ ] `src/types/user.ts` created
- [ ] User, AuthState, RegisterData, LoginData, TokenResponse types defined
- [ ] `src/types/task.ts` created
- [ ] Task, TaskListResponse, TaskState types defined
- [ ] All types match backend schema structure
- [ ] No TypeScript errors when importing types

**Estimated Complexity:** Small

**Dependencies:** P2-003

---

### P2-026: Implement API Client with Interceptors

**Title:** Create axios API client with request/response interceptors

**Description:**
Implement API client using axios with interceptors for automatic JWT injection and token refresh on 401 errors.

**Preconditions:**
- P2-025 complete (types defined)
- Axios installed

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Authentication and Authorization Behavior"

**Plan References:**
- PHASE_II_PLAN.md: Section 4.5 "API Client"

**Artifacts to Create:**
```
frontend/src/lib/api.ts
```

**Implementation Requirements:**

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Add JWT to Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: Handle 401 and refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        // Call refresh endpoint
        const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

**Acceptance Criteria:**
- [ ] `src/lib/api.ts` created
- [ ] Axios instance created with base URL
- [ ] Request interceptor adds JWT to Authorization header
- [ ] Response interceptor handles 401 errors
- [ ] Automatic token refresh on 401
- [ ] Redirect to login if refresh fails
- [ ] Can import and use api client

**Estimated Complexity:** Medium

**Dependencies:** P2-025

---

### P2-027: Implement JWT Storage Utilities

**Title:** Create utilities for storing and retrieving JWT tokens

**Description:**
Implement helper functions for storing, retrieving, and clearing JWT tokens from localStorage.

**Preconditions:**
- P2-003 complete

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-202 (tokens stored securely)

**Plan References:**
- PHASE_II_PLAN.md: Section 4.1 "Frontend Project Structure" (lib/auth.ts)

**Artifacts to Create:**
```
frontend/src/lib/auth.ts
```

**Implementation Requirements:**

```typescript
export const setTokens = (accessToken: string, refreshToken: string): void => {
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', refreshToken);
};

export const getAccessToken = (): string | null => {
  return localStorage.getItem('access_token');
};

export const getRefreshToken = (): string | null => {
  return localStorage.getItem('refresh_token');
};

export const clearTokens = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export const isAuthenticated = (): boolean => {
  return !!getAccessToken();
};
```

**Acceptance Criteria:**
- [ ] `src/lib/auth.ts` created
- [ ] `setTokens()` stores both tokens in localStorage
- [ ] `getAccessToken()` retrieves access token
- [ ] `getRefreshToken()` retrieves refresh token
- [ ] `clearTokens()` removes both tokens
- [ ] `isAuthenticated()` checks if access token exists
- [ ] All functions have proper return types

**Estimated Complexity:** Small

**Dependencies:** P2-003

---

### P2-028: Implement Form Validation Utilities

**Title:** Create form validation helper functions

**Description:**
Implement validation functions for email, password, and task description matching backend validation rules.

**Preconditions:**
- P2-003 complete

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Validation Rules" section

**Plan References:**
- PHASE_II_PLAN.md: Section 4.7 "Form Validation"

**Artifacts to Create:**
```
frontend/src/utils/validation.ts
```

**Implementation Requirements:**

```typescript
export const validateEmail = (email: string): string | null => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!email) return 'Email is required';
  if (!emailRegex.test(email)) return 'Please enter a valid email address';
  return null;
};

export const validatePassword = (password: string): string | null => {
  if (!password) return 'Password is required';
  if (password.length < 8) return 'Password must be at least 8 characters';
  if (!/[A-Z]/.test(password)) return 'Password must contain an uppercase letter';
  if (!/[a-z]/.test(password)) return 'Password must contain a lowercase letter';
  if (!/[0-9]/.test(password)) return 'Password must contain a number';
  if (!/[!@#$%^&*]/.test(password)) return 'Password must contain a special character';
  return null;
};

export const validatePasswordConfirmation = (
  password: string,
  confirmation: string
): string | null => {
  if (!confirmation) return 'Password confirmation is required';
  if (password !== confirmation) return 'Passwords do not match';
  return null;
};

export const validateDescription = (description: string): string | null => {
  const trimmed = description.trim();
  if (!trimmed) return 'Task description cannot be empty';
  if (trimmed.length > 500) return 'Task description too long (max 500 characters)';
  return null;
};
```

**Acceptance Criteria:**
- [ ] `src/utils/validation.ts` created
- [ ] `validateEmail()` checks format and empty
- [ ] `validatePassword()` checks all requirements (8+ chars, uppercase, lowercase, digit, special)
- [ ] `validatePasswordConfirmation()` checks match
- [ ] `validateDescription()` checks length (1-500 chars)
- [ ] All functions return null if valid, error message if invalid
- [ ] Validation rules match backend exactly

**Estimated Complexity:** Small

**Dependencies:** P2-003

---

### P2-029: Create AuthContext and Provider

**Title:** Implement React Context for authentication state management

**Description:**
Create AuthContext with user state, login, logout, and register functions using React Context API.

**Preconditions:**
- P2-026 complete (API client)
- P2-027 complete (JWT storage)
- P2-025 complete (types)

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Authentication and Authorization Behavior"

**Plan References:**
- PHASE_II_PLAN.md: Section 4.4 "State Management" (Auth State)

**Artifacts to Create:**
```
frontend/src/contexts/AuthContext.tsx
```

**Implementation Requirements:**

```typescript
'use client';

import React, { createContext, useState, useEffect, ReactNode } from 'react';
import api from '@/lib/api';
import { setTokens, clearTokens, getAccessToken } from '@/lib/auth';
import { User, AuthState, RegisterData, LoginData } from '@/types/user';

interface AuthContextType extends AuthState {
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is authenticated on mount
    const token = getAccessToken();
    if (token) {
      // TODO: Fetch current user data from backend (optional)
      // For now, assume user is authenticated if token exists
      setUser({ id: 0, email: '', created_at: '' }); // Placeholder
    }
    setLoading(false);
  }, []);

  const register = async (data: RegisterData) => {
    setLoading(true);
    setError(null);
    try {
      await api.post('/api/auth/register', data);
      // Registration successful, don't auto-login
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const login = async (data: LoginData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/api/auth/login', data);
      const { access_token, refresh_token } = response.data;
      setTokens(access_token, refresh_token);
      // TODO: Fetch current user data (optional)
      setUser({ id: 0, email: data.email, created_at: '' }); // Placeholder
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

**Acceptance Criteria:**
- [ ] `src/contexts/AuthContext.tsx` created
- [ ] AuthContext created with user, loading, error state
- [ ] AuthProvider component wraps children
- [ ] `register()` function calls POST /api/auth/register
- [ ] `login()` function calls POST /api/auth/login and stores tokens
- [ ] `logout()` function clears tokens and user state
- [ ] Context checks for existing token on mount
- [ ] Error handling for auth operations
- [ ] Can wrap app with AuthProvider

**Estimated Complexity:** Medium

**Dependencies:** P2-026, P2-027, P2-025

---

### P2-030: Create useAuth Hook

**Title:** Create custom React hook for accessing auth context

**Description:**
Implement useAuth hook to access AuthContext easily from components.

**Preconditions:**
- P2-029 complete (AuthContext)

**Specification References:**
- PHASE_II_SPECIFICATION.md: Authentication flows

**Plan References:**
- PHASE_II_PLAN.md: Section 4.1 "Frontend Project Structure" (hooks/useAuth.ts)

**Artifacts to Create:**
```
frontend/src/hooks/useAuth.ts
```

**Implementation Requirements:**

```typescript
import { useContext } from 'react';
import { AuthContext } from '@/contexts/AuthContext';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

**Acceptance Criteria:**
- [ ] `src/hooks/useAuth.ts` created
- [ ] useAuth hook accesses AuthContext
- [ ] Throws error if used outside AuthProvider
- [ ] Returns full auth context (user, loading, error, login, register, logout)
- [ ] Can import and use in components

**Estimated Complexity:** Small

**Dependencies:** P2-029

---

### P2-031: Create useTasks Hook

**Title:** Create custom React hook for task CRUD operations

**Description:**
Implement useTasks hook with functions for fetching, creating, updating, deleting, and toggling tasks.

**Preconditions:**
- P2-026 complete (API client)
- P2-025 complete (Task types)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-204 through US-208 (task operations)

**Plan References:**
- PHASE_II_PLAN.md: Section 4.4 "State Management" (Task State)

**Artifacts to Create:**
```
frontend/src/hooks/useTasks.ts
```

**Implementation Requirements:**

```typescript
import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Task, TaskState } from '@/types/task';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/api/tasks');
      setTasks(response.data.tasks);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (description: string) => {
    setError(null);
    try {
      const response = await api.post('/api/tasks', { description });
      setTasks([...tasks, response.data]);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create task');
      throw err;
    }
  };

  const updateTask = async (id: number, description: string) => {
    setError(null);
    try {
      const response = await api.put(`/api/tasks/${id}`, { description });
      setTasks(tasks.map(t => (t.id === id ? response.data : t)));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update task');
      throw err;
    }
  };

  const deleteTask = async (id: number) => {
    setError(null);
    try {
      await api.delete(`/api/tasks/${id}`);
      setTasks(tasks.filter(t => t.id !== id));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete task');
      throw err;
    }
  };

  const toggleTask = async (id: number) => {
    setError(null);
    try {
      const response = await api.patch(`/api/tasks/${id}/toggle`);
      setTasks(tasks.map(t => (t.id === id ? response.data : t)));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to toggle task');
      throw err;
    }
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
  };
};
```

**Acceptance Criteria:**
- [ ] `src/hooks/useTasks.ts` created
- [ ] useTasks hook manages tasks state
- [ ] `fetchTasks()` calls GET /api/tasks
- [ ] `createTask()` calls POST /api/tasks and updates state
- [ ] `updateTask()` calls PUT /api/tasks/{id} and updates state
- [ ] `deleteTask()` calls DELETE /api/tasks/{id} and updates state
- [ ] `toggleTask()` calls PATCH /api/tasks/{id}/toggle and updates state
- [ ] Error handling for all operations
- [ ] Can import and use in components

**Estimated Complexity:** Medium

**Dependencies:** P2-026, P2-025

---

## 7. FRONTEND PAGES & COMPONENTS TASKS

---

### P2-032: Create Root Layout

**Title:** Implement root layout with AuthProvider

**Description:**
Create Next.js root layout that wraps the entire application with AuthProvider and includes global styles.

**Preconditions:**
- P2-029 complete (AuthProvider)

**Specification References:**
- PHASE_II_SPECIFICATION.md: Frontend structure

**Plan References:**
- PHASE_II_PLAN.md: Section 4.1 "Frontend Project Structure"

**Artifacts to Create:**
```
frontend/src/app/layout.tsx
frontend/src/app/globals.css
```

**Implementation Requirements:**

**src/app/layout.tsx:**
```typescript
import type { Metadata } from 'next';
import { AuthProvider } from '@/contexts/AuthContext';
import './globals.css';

export const metadata: Metadata = {
  title: 'Todo App - Phase II',
  description: 'Multi-user todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

**src/app/globals.css:**
```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

button {
  cursor: pointer;
  font-family: inherit;
}

input, textarea {
  font-family: inherit;
}
```

**Acceptance Criteria:**
- [ ] `src/app/layout.tsx` created
- [ ] Root layout wraps children with AuthProvider
- [ ] Metadata configured
- [ ] `src/app/globals.css` created with basic styles
- [ ] No TypeScript errors

**Estimated Complexity:** Small

**Dependencies:** P2-029

---

### P2-033: Create Landing Page (/)

**Title:** Implement public landing page

**Description:**
Create landing page with app description and links to login/register.

**Preconditions:**
- P2-032 complete (root layout)

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Frontend Specification" (Landing Page)

**Plan References:**
- PHASE_II_PLAN.md: Section 4.2 "Page Components" (Landing Page)

**Artifacts to Create:**
```
frontend/src/app/page.tsx
```

**Implementation Requirements:**

```typescript
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.push('/dashboard');
    }
  }, [user, loading, router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem', textAlign: 'center' }}>
      <h1>Welcome to Todo App</h1>
      <p>Manage your tasks efficiently with our simple and powerful todo application.</p>
      <div style={{ marginTop: '2rem' }}>
        <Link href="/register" style={{ marginRight: '1rem' }}>
          <button style={{ padding: '0.5rem 2rem', fontSize: '1rem' }}>Get Started</button>
        </Link>
        <Link href="/login">
          <button style={{ padding: '0.5rem 2rem', fontSize: '1rem' }}>Login</button>
        </Link>
      </div>
    </div>
  );
}
```

**Acceptance Criteria:**
- [ ] `src/app/page.tsx` created
- [ ] Landing page displays welcome message
- [ ] Buttons link to /register and /login
- [ ] Redirects to /dashboard if user is authenticated
- [ ] Displays loading state while checking auth
- [ ] No TypeScript errors

**Estimated Complexity:** Small

**Dependencies:** P2-032

---

### P2-034: Create Register Page (/register)

**Title:** Implement user registration page

**Description:**
Create registration page with form for email, password, and password confirmation with client-side validation.

**Preconditions:**
- P2-030 complete (useAuth hook)
- P2-028 complete (validation utilities)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-201 (User Registration)

**Plan References:**
- PHASE_II_PLAN.md: Section 4.2 "Page Components" (Register Page)

**Artifacts to Create:**
```
frontend/src/app/register/page.tsx
```

**Implementation Requirements:**

```typescript
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { validateEmail, validatePassword, validatePasswordConfirmation } from '@/utils/validation';
import Link from 'next/link';

export default function RegisterPage() {
  const { user, loading, register } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      router.push('/dashboard');
    }
  }, [user, loading, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validate
    const emailError = validateEmail(email);
    const passwordError = validatePassword(password);
    const confirmError = validatePasswordConfirmation(password, passwordConfirmation);

    if (emailError || passwordError || confirmError) {
      setErrors({
        email: emailError || '',
        password: passwordError || '',
        passwordConfirmation: confirmError || '',
      });
      return;
    }

    setSubmitting(true);
    try {
      await register({ email, password, password_confirmation: passwordConfirmation });
      router.push('/login?registered=true');
    } catch (err) {
      // Error handled by AuthContext
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '2rem' }}>
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {errors.email && <p style={{ color: 'red' }}>{errors.email}</p>}
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {errors.password && <p style={{ color: 'red' }}>{errors.password}</p>}
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>Confirm Password:</label>
          <input
            type="password"
            value={passwordConfirmation}
            onChange={(e) => setPasswordConfirmation(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {errors.passwordConfirmation && <p style={{ color: 'red' }}>{errors.passwordConfirmation}</p>}
        </div>
        <button type="submit" disabled={submitting} style={{ width: '100%', padding: '0.5rem' }}>
          {submitting ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p style={{ marginTop: '1rem' }}>
        Already have an account? <Link href="/login">Login</Link>
      </p>
    </div>
  );
}
```

**Acceptance Criteria:**
- [ ] `src/app/register/page.tsx` created
- [ ] Registration form with email, password, confirmation fields
- [ ] Client-side validation on submit
- [ ] Displays validation errors inline
- [ ] Calls register() from useAuth on valid submission
- [ ] Redirects to /login on successful registration
- [ ] Link to login page
- [ ] Redirects to /dashboard if already authenticated
- [ ] No TypeScript errors

**Estimated Complexity:** Medium

**Dependencies:** P2-030, P2-028

---

### P2-035: Create Login Page (/login)

**Title:** Implement user login page

**Description:**
Create login page with form for email and password with client-side validation.

**Preconditions:**
- P2-030 complete (useAuth hook)
- P2-028 complete (validation utilities)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-202 (User Login)

**Plan References:**
- PHASE_II_PLAN.md: Section 4.2 "Page Components" (Login Page)

**Artifacts to Create:**
```
frontend/src/app/login/page.tsx
```

**Implementation Requirements:**

```typescript
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { validateEmail } from '@/utils/validation';
import Link from 'next/link';

export default function LoginPage() {
  const { user, loading, login, error } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && user) {
      router.push('/dashboard');
    }
  }, [user, loading, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Validate
    const emailError = validateEmail(email);
    if (emailError || !password) {
      setErrors({
        email: emailError || '',
        password: !password ? 'Password is required' : '',
      });
      return;
    }

    setSubmitting(true);
    try {
      await login({ email, password });
      router.push('/dashboard');
    } catch (err) {
      // Error handled by AuthContext
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '2rem' }}>
      <h1>Login</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {errors.email && <p style={{ color: 'red' }}>{errors.email}</p>}
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {errors.password && <p style={{ color: 'red' }}>{errors.password}</p>}
        </div>
        <button type="submit" disabled={submitting} style={{ width: '100%', padding: '0.5rem' }}>
          {submitting ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p style={{ marginTop: '1rem' }}>
        Don't have an account? <Link href="/register">Register</Link>
      </p>
    </div>
  );
}
```

**Acceptance Criteria:**
- [ ] `src/app/login/page.tsx` created
- [ ] Login form with email and password fields
- [ ] Client-side validation on submit
- [ ] Displays validation errors inline
- [ ] Displays auth error from context
- [ ] Calls login() from useAuth on valid submission
- [ ] Redirects to /dashboard on successful login
- [ ] Link to register page
- [ ] Redirects to /dashboard if already authenticated
- [ ] No TypeScript errors

**Estimated Complexity:** Medium

**Dependencies:** P2-030, P2-028

---

### P2-036: Create Dashboard Page (/dashboard)

**Title:** Implement protected dashboard page with task list

**Description:**
Create dashboard page that displays user's tasks, requires authentication, and provides task management UI.

**Preconditions:**
- P2-030 complete (useAuth hook)
- P2-031 complete (useTasks hook)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-204 (View Personal Task List)

**Plan References:**
- PHASE_II_PLAN.md: Section 4.2 "Page Components" (Dashboard Page)

**Artifacts to Create:**
```
frontend/src/app/dashboard/page.tsx
```

**Implementation Requirements:**

```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';

export default function DashboardPage() {
  const { user, loading: authLoading, logout } = useAuth();
  const { tasks, loading: tasksLoading, fetchTasks, createTask, updateTask, deleteTask, toggleTask } = useTasks();
  const router = useRouter();
  const [showAddModal, setShowAddModal] = useState(false);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  if (authLoading || tasksLoading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null;
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1>Dashboard</h1>
          <p>Welcome, {user.email}</p>
        </div>
        <button onClick={logout}>Logout</button>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <button onClick={() => setShowAddModal(true)}>Add Task</button>
      </div>

      {tasks.length === 0 ? (
        <p>No tasks yet. Create your first task!</p>
      ) : (
        <div>
          <p>{tasks.length} tasks</p>
          {tasks.map(task => (
            <div key={task.id} style={{ padding: '1rem', marginBottom: '0.5rem', backgroundColor: 'white', borderRadius: '4px' }}>
              <input
                type="checkbox"
                checked={task.is_complete}
                onChange={() => toggleTask(task.id)}
              />
              <span style={{ textDecoration: task.is_complete ? 'line-through' : 'none', marginLeft: '0.5rem' }}>
                {task.description}
              </span>
              <button onClick={() => alert('Edit coming soon')} style={{ marginLeft: '1rem' }}>Edit</button>
              <button onClick={() => deleteTask(task.id)} style={{ marginLeft: '0.5rem' }}>Delete</button>
            </div>
          ))}
        </div>
      )}

      {showAddModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '4px', width: '400px' }}>
            <h2>Add Task</h2>
            <form onSubmit={async (e) => {
              e.preventDefault();
              const description = (e.target as any).description.value;
              await createTask(description);
              setShowAddModal(false);
            }}>
              <textarea
                name="description"
                placeholder="Task description"
                style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem' }}
                rows={3}
              />
              <div>
                <button type="submit">Add</button>
                <button type="button" onClick={() => setShowAddModal(false)} style={{ marginLeft: '0.5rem' }}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
```

**Acceptance Criteria:**
- [ ] `src/app/dashboard/page.tsx` created
- [ ] Dashboard requires authentication (redirects to /login if not authenticated)
- [ ] Displays user email and logout button
- [ ] Fetches and displays all user tasks
- [ ] Displays empty state if no tasks
- [ ] "Add Task" button opens modal
- [ ] Simple add task modal (placeholder for P2-040)
- [ ] Can toggle task completion via checkbox
- [ ] Can delete task
- [ ] Edit button placeholder (actual edit modal in P2-041)
- [ ] No TypeScript errors

**Estimated Complexity:** Large

**Dependencies:** P2-030, P2-031

---

**Note:** Tasks P2-037 through P2-042 (Navbar, TaskCard, TaskList, and Modal components) are straightforward component extractions from the dashboard page created in P2-036. Due to character limits, I'll summarize them:

**P2-037: Create Navbar Component** - Extract navbar with user email and logout button
**P2-038: Create TaskCard Component** - Extract individual task display with checkbox, edit, delete
**P2-039: Create TaskList Component** - Extract task list rendering
**P2-040: Create AddTaskModal Component** - Extract add task modal with validation
**P2-041: Create EditTaskModal Component** - Create edit task modal similar to add modal
**P2-042: Create DeleteConfirmModal Component** - Create confirmation dialog for delete

---

## 8. TESTING & DOCUMENTATION TASKS

---

### P2-043: Write Backend Auth Tests

**Title:** Create pytest tests for authentication endpoints

**Description:**
Write comprehensive tests for registration, login, logout, and token refresh endpoints.

**Preconditions:**
- P2-018 complete (all auth endpoints implemented)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-201, US-202, US-203, US-204

**Plan References:**
- PHASE_II_PLAN.md: Section 6.1 "Backend Testing" (test_auth.py)

**Artifacts to Create:**
```
backend/tests/test_auth.py
backend/tests/conftest.py
```

**Acceptance Criteria:**
- [ ] `tests/test_auth.py` created
- [ ] Test user registration (valid, invalid email, duplicate, weak password)
- [ ] Test user login (valid, invalid credentials)
- [ ] Test token refresh (valid, expired token)
- [ ] Test logout
- [ ] All tests pass
- [ ] Test fixtures in conftest.py

**Estimated Complexity:** Medium

**Dependencies:** P2-018

---

### P2-044: Write Backend Task CRUD Tests

**Title:** Create pytest tests for task endpoints

**Description:**
Write comprehensive tests for all task CRUD operations.

**Preconditions:**
- P2-024 complete (all task endpoints implemented)

**Specification References:**
- PHASE_II_SPECIFICATION.md: US-205 through US-209

**Plan References:**
- PHASE_II_PLAN.md: Section 6.1 "Backend Testing" (test_tasks.py)

**Artifacts to Create:**
```
backend/tests/test_tasks.py
```

**Acceptance Criteria:**
- [ ] `tests/test_tasks.py` created
- [ ] Test create task (valid, invalid, unauthorized)
- [ ] Test get all tasks
- [ ] Test get task by ID
- [ ] Test update task
- [ ] Test delete task
- [ ] Test toggle task
- [ ] All tests pass

**Estimated Complexity:** Medium

**Dependencies:** P2-024

---

### P2-045: Write Backend User Isolation Tests

**Title:** Create pytest tests verifying user data isolation

**Description:**
Write tests that verify users cannot access other users' tasks.

**Preconditions:**
- P2-044 complete (task tests exist)

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Authorization Errors" section

**Plan References:**
- PHASE_II_PLAN.md: Section 6.1 "Backend Testing" (test_user_isolation.py)

**Artifacts to Create:**
```
backend/tests/test_user_isolation.py
```

**Acceptance Criteria:**
- [ ] `tests/test_user_isolation.py` created
- [ ] Test User A cannot view User B's tasks
- [ ] Test User A cannot update User B's tasks
- [ ] Test User A cannot delete User B's tasks
- [ ] Test User A cannot toggle User B's tasks
- [ ] All tests pass
- [ ] ≥80% backend coverage achieved

**Estimated Complexity:** Medium

**Dependencies:** P2-044

---

### P2-046 through P2-049: Frontend Tests
- P2-046: Register page tests
- P2-047: Login page tests
- P2-048: Dashboard tests
- P2-049: Component tests (TaskCard, modals, etc.)

**Estimated Complexity:** Medium each

---

### P2-050: Run Linting and Formatting

**Title:** Apply linting and formatting to all code

**Description:**
Run Ruff/Black on backend, ESLint/Prettier on frontend, fix all issues.

**Preconditions:**
- All code tasks complete

**Acceptance Criteria:**
- [ ] Backend: `ruff check .` passes with no errors
- [ ] Backend: `black .` applied
- [ ] Frontend: `npm run lint` passes with no errors
- [ ] Frontend: `npm run format` applied

**Estimated Complexity:** Small

**Dependencies:** P2-042, P2-049

---

### P2-051: Manual Testing and Bug Fixes

**Title:** Perform manual testing of all features and fix bugs

**Description:**
Manually test all user flows, fix any bugs found, verify all acceptance criteria.

**Preconditions:**
- All implementation and automated testing complete

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Acceptance Criteria for Phase II Completion"

**Acceptance Criteria:**
- [ ] Can register new user
- [ ] Can login with registered user
- [ ] Can logout
- [ ] Can view tasks (empty state and with tasks)
- [ ] Can create task
- [ ] Can update task
- [ ] Can delete task with confirmation
- [ ] Can toggle task completion
- [ ] User A cannot access User B's tasks (verify in browser dev tools)
- [ ] All error cases handled gracefully
- [ ] Application responsive on mobile and desktop
- [ ] All bugs fixed

**Estimated Complexity:** Medium

**Dependencies:** P2-050

---

### P2-052: Create README and Documentation

**Title:** Write README and setup documentation

**Description:**
Create comprehensive README files for backend and frontend with setup instructions, environment variables, and usage guide.

**Preconditions:**
- P2-051 complete (all functionality verified)

**Specification References:**
- PHASE_II_SPECIFICATION.md: "Deliverables" section

**Plan References:**
- PHASE_II_PLAN.md: Section 9 "Development Workflow"

**Artifacts to Create:**
```
backend/README.md
frontend/README.md
README_PHASE_II.md
```

**Acceptance Criteria:**
- [ ] `backend/README.md` created with setup instructions
- [ ] `frontend/README.md` created with setup instructions
- [ ] `README_PHASE_II.md` created with overview and complete setup guide
- [ ] Environment variable documentation complete
- [ ] API documentation referenced (FastAPI auto-generated docs)
- [ ] Phase II marked as COMPLETE

**Estimated Complexity:** Small

**Dependencies:** P2-051

---

## PHASE II COMPLETION CHECKLIST

### Project Setup ✅
- [ ] P2-001: Project structure created
- [ ] P2-002: Backend environment setup
- [ ] P2-003: Frontend environment setup
- [ ] P2-004: Database connection setup
- [ ] P2-005: Alembic migrations initialized

### Database Schema ✅
- [ ] P2-006: User SQLModel created
- [ ] P2-007: Task SQLModel created
- [ ] P2-008: Initial migration applied

### Backend Core ✅
- [ ] P2-009: Password hashing implemented
- [ ] P2-010: JWT generation/validation implemented
- [ ] P2-011: Database session dependency created
- [ ] P2-012: Get current user dependency created
- [ ] P2-013: Custom exceptions defined

### Backend Auth ✅
- [ ] P2-014: Auth schemas created
- [ ] P2-015: User service implemented
- [ ] P2-016: POST /api/auth/register endpoint
- [ ] P2-017: POST /api/auth/login endpoint
- [ ] P2-018: Logout and refresh endpoints

### Backend Tasks ✅
- [ ] P2-019: Task schemas created
- [ ] P2-020: Task service with user isolation
- [ ] P2-021: GET /api/tasks endpoint
- [ ] P2-022: POST /api/tasks endpoint
- [ ] P2-023: GET/PUT/DELETE /api/tasks/{id} endpoints
- [ ] P2-024: PATCH /api/tasks/{id}/toggle endpoint

### Frontend Core ✅
- [ ] P2-025: TypeScript types defined
- [ ] P2-026: API client with interceptors
- [ ] P2-027: JWT storage utilities
- [ ] P2-028: Form validation utilities
- [ ] P2-029: AuthContext created
- [ ] P2-030: useAuth hook created
- [ ] P2-031: useTasks hook created

### Frontend Pages & Components ✅
- [ ] P2-032: Root layout created
- [ ] P2-033: Landing page created
- [ ] P2-034: Register page created
- [ ] P2-035: Login page created
- [ ] P2-036: Dashboard page created
- [ ] P2-037: Navbar component created
- [ ] P2-038: TaskCard component created
- [ ] P2-039: TaskList component created
- [ ] P2-040: AddTaskModal component created
- [ ] P2-041: EditTaskModal component created
- [ ] P2-042: DeleteConfirmModal component created

### Testing & Documentation ✅
- [ ] P2-043: Backend auth tests written
- [ ] P2-044: Backend task tests written
- [ ] P2-045: Backend user isolation tests written
- [ ] P2-046: Frontend register tests written
- [ ] P2-047: Frontend login tests written
- [ ] P2-048: Frontend dashboard tests written
- [ ] P2-049: Frontend component tests written
- [ ] P2-050: Linting and formatting applied
- [ ] P2-051: Manual testing complete, bugs fixed
- [ ] P2-052: README and documentation complete

---

## SUCCESS CRITERIA

Phase II will be considered COMPLETE when:

1. **All 52 Tasks Completed** ✅
2. **All Acceptance Criteria Met** ✅
3. **Backend Tests Pass** (≥80% coverage) ✅
4. **Frontend Tests Pass** (≥70% coverage) ✅
5. **Manual Testing Complete** ✅
6. **Linting Passes** (Ruff, ESLint) ✅
7. **Documentation Complete** (README files) ✅
8. **Constitutional Compliance Verified** ✅
9. **No Phase III Features Implemented** ✅
10. **Phase II Approved for Production** ✅

---

## APPROVAL

**Task Breakdown Status:** DRAFT
**Constitutional Compliance:** VERIFIED (Constitution v2.0, PHASE_II_SPECIFICATION.md, PHASE_II_PLAN.md)
**Ready for Implementation:** PENDING APPROVAL

**Next Steps:**
1. Review and approve this task breakdown
2. Begin implementation starting with P2-001
3. Complete tasks in dependency order
4. Mark tasks complete as they are finished
5. Verify acceptance criteria for each task

---

**END OF PHASE II IMPLEMENTATION TASKS**

*This task breakdown is subordinate to CONSTITUTION.md v2.0, PHASE_II_SPECIFICATION.md, and PHASE_II_PLAN.md and may only be amended through the constitutional amendment process.*
