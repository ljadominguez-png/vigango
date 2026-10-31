# F3: Database connection

**Developer:** Bryan Balallo  
**Date:** October 29, 2026  
**Original branch:** `feat/f3-Database`  
**Status at the time:** Completed

> Historical implementation report migrated from the backend README. The main [README](../README.md) contains the current setup instructions.

## Overview

F3 connected the ViganGo FastAPI backend to the team's Supabase PostgreSQL database using SQLAlchemy and the Psycopg driver. Pydantic Settings loads the database URL from the environment so credentials are not stored in application code.

## Technologies

- Supabase PostgreSQL for the hosted database.
- SQLAlchemy for engine and database sessions.
- Psycopg for PostgreSQL connectivity.
- Pydantic Settings for `.env`-backed application configuration.
- Python virtual environment for isolated dependencies.

## Implementation

**Dependencies:** The original task installed `sqlalchemy`, `psycopg[binary]`, and `pydantic-settings` and recorded them in `backend/requirements.txt`.

**Environment:** `backend/.env` contains a connection string in this format:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
```

The original connection used the Supabase Session Pooler. `.env` is ignored by Git and must never be committed.

**Configuration (`backend/app/config.py`):** Pydantic Settings reads `DATABASE_URL` without hardcoding credentials.

**Database setup (`backend/app/database.py`):**

| Component      | Purpose                                                |
| -------------- | ------------------------------------------------------ |
| `engine`       | Establishes SQLAlchemy's connection to PostgreSQL.     |
| `SessionLocal` | Creates application database sessions.                 |
| `Base`         | Shared declarative base for SQLAlchemy models.         |
| `get_db()`     | Supplies a session to FastAPI and closes it after use. |

## Verification

The original F3 report records a successful connection to Supabase through the SQLAlchemy configuration. It did not cover user-registration inserts, which were subsequently verified in F4.2 against isolated local PostgreSQL.

## Git history

- **Original commit:** `921917f` (`feat: configure Supabase database connection`)
- **Original branch:** `feat/f3-Database`

## Follow-up from the original report

The original F3 report identified database models, constraints, and CRUD checks as subsequent work. The F4.1 database-model documentation describes the later model implementation. See [F4.1: Database models](f4.1-database-models.md).
