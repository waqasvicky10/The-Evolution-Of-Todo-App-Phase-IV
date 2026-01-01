# Database Migration Guide

## Overview

This project uses Alembic for database schema migrations with SQLModel.

## Initial Setup

### 1. Configure Database Connection

Edit `backend/.env` and set your Neon PostgreSQL connection string:

```bash
DATABASE_URL=postgresql://user:password@host/dbname
```

### 2. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Migrations

### Apply All Migrations

```bash
cd backend
alembic upgrade head
```

This will create the `users` and `tasks` tables in your database.

### Check Current Migration Status

```bash
alembic current
```

### View Migration History

```bash
alembic history --verbose
```

## Migration 001: Create Users and Tasks Tables

**File:** `alembic/versions/001_create_users_and_tasks_tables.py`

**Creates:**

### Users Table
- `id` (INTEGER, PRIMARY KEY, AUTO INCREMENT)
- `email` (VARCHAR(255), UNIQUE, INDEXED)
- `hashed_password` (VARCHAR(255))
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

**Indexes:**
- `ix_users_email` (UNIQUE) - Fast email lookups for login

### Tasks Table
- `id` (INTEGER, PRIMARY KEY, AUTO INCREMENT)
- `description` (VARCHAR(500))
- `is_complete` (BOOLEAN, DEFAULT FALSE)
- `user_id` (INTEGER, FOREIGN KEY → users.id, ON DELETE CASCADE)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

**Indexes:**
- `ix_tasks_user_id` - Fast user-filtered task queries

**Constraints:**
- Foreign key: `tasks.user_id` → `users.id` with CASCADE delete
- Unique constraint on `users.email`

## Creating New Migrations

After modifying SQLModel models:

```bash
# Generate migration automatically
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file
# Edit if needed to ensure correctness

# Apply the migration
alembic upgrade head
```

## Rollback Migrations

### Rollback Last Migration

```bash
alembic downgrade -1
```

### Rollback to Specific Revision

```bash
alembic downgrade <revision_id>
```

### Rollback All Migrations

```bash
alembic downgrade base
```

## Troubleshooting

### Connection Issues

If you get connection errors:
1. Verify DATABASE_URL in `.env` is correct
2. Check Neon database is accessible
3. Verify SSL settings if required

### Migration Conflicts

If migrations are out of sync:
1. Check current database state: `alembic current`
2. Compare with migration files in `alembic/versions/`
3. May need to manually sync or reset database

### Reset Database (Development Only)

**WARNING: This will delete all data!**

```bash
# Rollback all migrations
alembic downgrade base

# Re-apply all migrations
alembic upgrade head
```

## Production Deployment

1. **Backup database** before running migrations
2. Run migrations in staging environment first
3. Test thoroughly before production deployment
4. Run migrations during maintenance window if possible
5. Have rollback plan ready

```bash
# Production migration workflow
alembic upgrade head
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
