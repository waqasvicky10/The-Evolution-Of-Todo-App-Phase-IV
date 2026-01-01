# Phase II Setup Guide

Complete guide for setting up and running the Todo App Phase II application.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Database Configuration](#database-configuration)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [Environment Variables](#environment-variables)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.12+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 18+ and npm**
   - Download: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **Git** (optional, for cloning)
   - Download: https://git-scm.com/downloads
   - Verify: `git --version`

### Required Services

1. **Neon PostgreSQL Database**
   - Sign up: https://neon.tech/
   - Create a new project and database
   - Copy your connection string (format: `postgresql://user:password@host/database?sslmode=require`)

---

## Initial Setup

### 1. Clone or Navigate to Project

```bash
cd E:\heckathon-2
```

### 2. Project Structure Verification

Ensure your project has this structure:

```
E:\heckathon-2\
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── .env.local.example
│   └── .env.local
├── CONSTITUTION.md
├── PHASE_II_SPECIFICATION.md
├── PHASE_II_PLAN.md
└── PHASE_II_TASKS.md
```

---

## Database Configuration

### Step 1: Create Neon PostgreSQL Database

1. Go to https://neon.tech/ and sign in
2. Create a new project
3. Create a new database (or use the default)
4. Copy the connection string from the dashboard

### Step 2: Update Backend Environment

Edit `backend/.env`:

```bash
# Replace this line
DATABASE_URL=postgresql://user:password@localhost/todo_db

# With your Neon connection string (example format)
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/todo_db?sslmode=require
```

**Important Security Notes:**
- Keep your `.env` file private (already in .gitignore)
- Never commit database credentials to version control
- For production, use environment-specific configurations

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages:**
- FastAPI 0.104.0
- Uvicorn 0.24.0
- SQLModel 0.0.14
- Alembic 1.12.1
- Pydantic Settings 2.12.0
- And 28+ other packages

### Step 4: Run Database Migrations

```bash
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, create users and tasks tables
```

### Step 5: Verify Backend Configuration

Check your `.env` file has all required variables:

```env
# Database
DATABASE_URL=postgresql://[your-neon-connection-string]

# Security
SECRET_KEY=your-secret-key-at-least-32-characters-long-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Security Warning:**
- **MUST** change `SECRET_KEY` for production
- Generate a secure secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd ../frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

**Expected output:**
- Installing 652 packages
- May take 3-5 minutes

### Step 3: Verify Frontend Configuration

Check your `.env.local` file:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**Notes:**
- This should point to your backend URL
- For production, update to your deployed backend URL

---

## Running the Application

### Option 1: Manual Startup (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Expected output:**
```
▲ Next.js 14.2.35
- Local:        http://localhost:3000
- Environments: .env.local

✓ Starting...
✓ Ready in 4.3s
```

### Option 2: Background Processes (Windows)

**Start Backend:**
```bash
cd backend
start /B uvicorn app.main:app --reload
```

**Start Frontend:**
```bash
cd frontend
start /B npm run dev
```

---

## Accessing the Application

### Frontend (User Interface)

- **URL**: http://localhost:3000
- **Pages**:
  - Landing: http://localhost:3000/
  - Register: http://localhost:3000/register
  - Login: http://localhost:3000/login
  - Dashboard: http://localhost:3000/dashboard (requires login)

### Backend (API)

- **Base URL**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | Required | PostgreSQL connection string |
| `SECRET_KEY` | Required | JWT signing key (32+ characters) |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 15 | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Refresh token lifetime |
| `CORS_ORIGINS` | http://localhost:3000 | Allowed CORS origins (comma-separated) |
| `ENVIRONMENT` | development | Environment name |

### Frontend (`frontend/.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | http://localhost:8000 | Backend API URL |

---

## Troubleshooting

### Backend Issues

#### Issue: ModuleNotFoundError: No module named 'pydantic_settings'
```bash
pip install pydantic-settings
```

#### Issue: Cannot connect to database
- Verify DATABASE_URL in `.env` is correct
- Check Neon database is running and accessible
- Ensure `?sslmode=require` is in connection string
- Test connection: `psql [your-connection-string]`

#### Issue: Port 8000 already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

#### Issue: Module not found errors
```bash
rm -rf node_modules package-lock.json
npm install
```

#### Issue: Port 3000 already in use
```bash
# Use different port
npm run dev -- -p 3001

# Or kill existing process
# Windows: taskkill /IM node.exe /F
# Linux/macOS: lsof -ti:3000 | xargs kill -9
```

#### Issue: Tailwind styles not loading
```bash
# Rebuild
npm run build
npm run dev
```

### Common Issues

#### Issue: CORS errors in browser console
- Verify `CORS_ORIGINS` in backend `.env` includes frontend URL
- Ensure frontend is accessing correct backend URL
- Check browser console for specific CORS error

#### Issue: Authentication not working
- Verify database migrations ran successfully
- Check SECRET_KEY is set in backend `.env`
- Clear browser local storage: `localStorage.clear()`

#### Issue: Tasks not loading
- Verify user is logged in (check browser dev tools → Application → Local Storage)
- Check backend logs for database errors
- Verify database migrations created tables correctly

---

## Development Workflow

### Making Changes

**Backend changes:**
- Uvicorn auto-reloads on file changes
- No restart needed for most changes
- Migrations needed for model changes: `alembic revision --autogenerate -m "description"`

**Frontend changes:**
- Next.js hot-reloads automatically
- Restart only needed for `.env.local` changes

### Database Migrations

**Create new migration:**
```bash
cd backend
alembic revision --autogenerate -m "description of changes"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback migration:**
```bash
alembic downgrade -1
```

### Code Quality

**Backend linting:**
```bash
cd backend
ruff check .
black .
```

**Frontend linting:**
```bash
cd frontend
npm run lint
npm run format
```

### Testing

**Backend tests:**
```bash
cd backend
pytest
pytest --cov
```

**Frontend tests:**
```bash
cd frontend
npm test
npm run test:coverage
```

---

## Next Steps

1. ✅ Complete setup following this guide
2. ✅ Test user registration and login
3. ✅ Create and manage tasks
4. 📚 Review API documentation at http://localhost:8000/docs
5. 🚀 Consider deployment (see DEPLOYMENT.md)

---

## Support

For issues or questions:
1. Check [TEST_RESULTS.md](./TEST_RESULTS.md) for known limitations
2. Review [PHASE_II_SPECIFICATION.md](./PHASE_II_SPECIFICATION.md) for requirements
3. Check backend logs for error messages
4. Check browser console for frontend errors

---

## Security Checklist for Production

Before deploying to production:

- [ ] Change SECRET_KEY in backend/.env to a secure random string
- [ ] Update CORS_ORIGINS to only include production frontend URL
- [ ] Use environment variables for all sensitive data
- [ ] Enable HTTPS for both frontend and backend
- [ ] Set ENVIRONMENT=production in backend/.env
- [ ] Review and update password strength requirements if needed
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Review and test all security measures

---

**Setup Complete!** 🎉

You now have a fully functional Phase II Todo App running locally.
