
# ViganGo Backend

FastAPI backend for the ViganGo tourism discovery platform.

## Tech Stack

- Python
- FastAPI
- Pytest
- HTTPX (API testing)

## Local Setup

Run these commands from the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Running the API

From the `backend/` directory:

```bash
python -m uvicorn app.main:app --reload
```

Local endpoints:

- API health: http://127.0.0.1:8000/health
- API documentation: http://127.0.0.1:8000/docs

## Running Tests

From the `backend/` directory:

```bash
python -m pytest -q
```

## Current API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Returns API health status |

Expected response:

```json
{
  "status": "ok"
}
```

## Current Scope

- FastAPI foundation
- Health endpoint
- Automated API testing

Database integration and activity-related endpoints will be implemented in future sprint tasks, based on team agreements.




# ViganGo -- F3: Database Connection Documentation

**Developer:** Bryan Balallo\
**Date:** October 29, 2026\
**Branch:** `feat/f3-Database`\
**Status:** Completed

## 1. Overview

This task focused on establishing a connection between the ViganGo
FastAPI backend and the Supabase PostgreSQL database. SQLAlchemy was
configured to manage database connections and sessions, while
environment variables were used to keep database credentials separate
from the source code.

## 2. Technologies Used

-   **Supabase:** Hosted PostgreSQL database.
-   **FastAPI:** Backend framework for the ViganGo API.
-   **SQLAlchemy:** ORM for database connectivity and session
    management.
-   **Psycopg:** PostgreSQL database driver.
-   **Pydantic Settings:** Environment-based configuration management.
-   **Python Virtual Environment:** Isolated environment for backend
    dependencies.

## 3. Implementation

### 3.1 Dependency Installation

Installed the necessary Python packages for database integration:

``` powershell
pip install sqlalchemy "psycopg[binary]" pydantic-settings
```

Updated `requirements.txt` to record the backend dependencies.

### 3.2 Environment Configuration

Created a `.env` file inside the backend directory to store the database
connection string.

``` env
DATABASE_URL=postgresql+psycopg://...
```

The connection uses the Supabase Session Pooler. The `.env` file is
excluded from Git through `.gitignore` to prevent database credentials
from being uploaded to the repository.

### 3.3 Application Configuration

Created `backend/app/config.py` to load environment variables using
Pydantic Settings.

This allows the application to access database configuration without
hardcoding credentials in the Python source code.

### 3.4 Database Connection

Created `backend/app/database.py` to configure SQLAlchemy.

The implementation includes:

-   **Engine:** Establishes the connection to the PostgreSQL database.
-   **SessionLocal:** Creates database sessions for backend operations.
-   **Base:** Serves as the base class for future database models.
-   **get_db():** Provides database sessions to API endpoints and
    ensures they are closed after use.

### 3.5 Connection Verification

Tested the database configuration by importing the SQLAlchemy components
and verifying that the backend could successfully establish a connection
to Supabase.

The connection test was successful.

## 4. Files Created and Modified

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `backend/app/config.py`             Loads database configuration and
                                      environment variables.

  `backend/app/database.py`           Configures SQLAlchemy engine,
                                      sessions, and database dependency.

  `backend/requirements.txt`          Records the required Python
                                      dependencies.

  `.gitignore`                        Prevents sensitive environment
                                      files and virtual environments from
                                      being tracked.
  -----------------------------------------------------------------------

## 5. Git Integration

After completing the database connection setup, the changes were
committed and pushed to the project's remote repository.

**Commit:**

``` text
921917f feat: configure Supabase database connection
```

**Branch:** `feat/f3-Database`

The local branch and remote branch were confirmed to point to the same
commit.

## 6. Current Result

The ViganGo FastAPI backend is now successfully configured to connect to
the Supabase PostgreSQL database. The project has the necessary database
connection infrastructure and session management in place for future
development.

## 7. Remaining Tasks

The next phase will focus on designing the ViganGo database schema,
creating the required tables and relationships, implementing SQLAlchemy
models, and testing database operations such as Create, Read, Update,
and Delete (CRUD).

------------------------------------------------------------------------

**End of Documentation**
