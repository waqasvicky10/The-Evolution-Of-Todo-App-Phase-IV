# Neon PostgreSQL Database Setup Guide

This guide will help you set up Neon Serverless PostgreSQL database for Phase II of the Todo App.

---

## Step 1: Create Neon Account and Database

1. **Go to Neon Console**
   - Visit: https://console.neon.tech
   - Sign up for a free account (or log in if you already have one)

2. **Create a New Project**
   - Click "New Project"
   - Choose a project name (e.g., "todo-app")
   - Select a region closest to you
   - Choose PostgreSQL version (recommended: 15 or 16)

3. **Get Connection String**
   - After project creation, you'll see a connection string like:
     ```
     postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
     ```
   - **Copy this connection string** - you'll need it in the next step

---

## Step 2: Configure Backend Environment

1. **Navigate to Backend Directory**
   ```bash
   cd backend
   ```

2. **Create or Edit `.env` File**
   ```bash
   # Copy example if .env doesn't exist
   cp .env.example .env
   ```

3. **Edit `.env` File**
   Open `backend/.env` and set your Neon connection string:
   ```env
   # Database - Neon PostgreSQL
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require

   # Security
   SECRET_KEY=your-secret-key-at-least-32-characters-long-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7

   # CORS
   CORS_ORIGINS=http://localhost:3000

   # OpenAI Integration (optional)
   OPENAI_API_KEY=your-openai-api-key-here

   # Environment
   ENVIRONMENT=production
   ```

   **Important:**
   - Replace `DATABASE_URL` with your actual Neon connection string
   - Generate a strong `SECRET_KEY` (at least 32 characters)
   - Keep your `.env` file secure and never commit it to git

---

## Step 3: Install Dependencies

Make sure you have the required Python packages:

```bash
cd backend
pip install -r requirements.txt
```

Required packages include:
- `sqlmodel` - ORM for database operations
- `psycopg2-binary` or `asyncpg` - PostgreSQL driver
- `alembic` - Database migrations

---

## Step 4: Run Database Migrations

1. **Initialize Alembic** (if not already done)
   ```bash
   alembic init alembic
   ```

2. **Run Migrations**
   ```bash
   # Create all tables
   alembic upgrade head
   ```

   This will create:
   - `users` table (id, email, hashed_password, created_at, updated_at)
   - `tasks` table (id, description, is_complete, user_id, created_at, updated_at)

3. **Verify Tables Created**
   You can check in Neon Console:
   - Go to your project
   - Click "SQL Editor"
   - Run: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';`
   - You should see `users` and `tasks` tables

---

## Step 5: Test Database Connection

1. **Start Backend Server**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Check Health Endpoint**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Test Database Connection**
   ```bash
   # Register a test user
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "Test123!@#", "password_confirmation": "Test123!@#"}'
   ```

   If successful, you should see:
   ```json
   {
     "id": 1,
     "email": "test@example.com",
     "created_at": "2026-01-24T..."
   }
   ```

4. **Verify in Neon Console**
   - Go to Neon Console → Your Project → SQL Editor
   - Run: `SELECT * FROM users;`
   - You should see your test user

---

## Step 6: Environment Variables for Production

For production deployment, set these environment variables:

### Backend (Render/Railway/Vercel)
- `DATABASE_URL` - Your Neon connection string
- `SECRET_KEY` - Strong secret key (32+ characters)
- `CORS_ORIGINS` - Your frontend URL (e.g., `https://your-app.vercel.app`)
- `ENVIRONMENT` - Set to `production`

### Frontend
- `NEXT_PUBLIC_API_BASE_URL` - Your backend API URL

---

## Troubleshooting

### Connection Issues

**Error: "Connection refused" or "Connection timeout"**
- Check your Neon connection string is correct
- Verify `sslmode=require` is in the connection string
- Check if your IP is whitelisted (Neon allows all IPs by default)

**Error: "Database does not exist"**
- Verify the database name in your connection string matches your Neon database
- Check project name in Neon Console

**Error: "Authentication failed"**
- Verify username and password in connection string
- Reset password in Neon Console if needed

### Migration Issues

**Error: "Table already exists"**
- Run: `alembic downgrade -1` then `alembic upgrade head`
- Or manually drop tables in Neon SQL Editor

**Error: "No such revision"**
- Check `alembic/versions/` folder has migration files
- Run: `alembic revision --autogenerate -m "Initial migration"`

### SSL Issues

**Error: "SSL connection required"**
- Add `?sslmode=require` to your connection string
- Neon requires SSL connections

---

## Neon Console Features

### SQL Editor
- Run SQL queries directly
- View table data
- Debug database issues

### Connection Details
- View connection strings
- Reset passwords
- Manage database settings

### Monitoring
- View query performance
- Check database size
- Monitor connections

---

## Security Best Practices

1. **Never commit `.env` files**
   - Already in `.gitignore`
   - Use environment variables in production

2. **Rotate Secrets Regularly**
   - Change `SECRET_KEY` periodically
   - Reset database passwords if compromised

3. **Use Connection Pooling**
   - Neon handles this automatically
   - Don't create too many connections

4. **Enable SSL**
   - Always use `sslmode=require` in connection string
   - Neon enforces SSL by default

---

## Next Steps

After setting up Neon PostgreSQL:

1. ✅ Database is configured
2. ✅ Migrations are run
3. ✅ Backend can connect to database
4. ✅ Test user registration works
5. ✅ Ready for Phase IV deployment

---

## Resources

- **Neon Documentation**: https://neon.tech/docs
- **Neon Console**: https://console.neon.tech
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/

---

## Support

If you encounter issues:
1. Check Neon Console for error messages
2. Verify connection string format
3. Check backend logs for detailed errors
4. Review this guide's troubleshooting section

---

**Status**: ✅ Ready for Neon PostgreSQL setup
