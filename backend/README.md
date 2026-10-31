# ViganGo Backend

FastAPI backend for **ViganGo**, a local activities and tourism discovery platform for Vigan and Metro Vigan.

## Current features

| Method | Endpoint                | Purpose                                                       |
| ------ | ----------------------- | ------------------------------------------------------------- |
| `GET`  | `/health`               | Verify that the API is responding.                            |
| `POST` | `/api/v1/auth/register` | Validate and register a user with a securely hashed password. |

The registration endpoint returns **201** on success, **409** for a duplicate username/email, and **422** for invalid request data. User responses never include `password_hash`.

## Tech stack

- **API:** Python, FastAPI, Pydantic
- **Database:** PostgreSQL (team-hosted Supabase), SQLAlchemy, Psycopg
- **Password hashing:** Argon2id via `pwdlib`
- **Testing:** Pytest, HTTPX/FastAPI TestClient; Docker PostgreSQL for integration tests

## Local setup

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Create `backend/.env` with a **team-authorized** connection string:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
```

Never commit `.env` or real database credentials. Ensure `requirements.txt` includes `pwdlib[argon2]` for the registration feature.

Start the API from `backend/`:

```bash
python -m uvicorn app.main:app --reload
```

- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

## Run tests

From `backend/`:

```bash
python -m pytest -v
```

The PostgreSQL integration tests are **skipped** if `TEST_DATABASE_URL` is not set. To run them, start the isolated local PostgreSQL container documented in [F4.2: User registration](docs/f4.2-user-registration.md), then run:

```bash
TEST_DATABASE_URL='postgresql+psycopg://vigango_test:local_only_password@127.0.0.1:55432/vigango_test' \
python -m pytest -v
```

The integration tests validate the local test database connection settings before performing any database operations. **Do not use the team's Supabase connection string for tests.**

## Documentation

See the [documentation index](docs/README.md) for feature-level implementation reports:

- [F3: Database connection](docs/f3-database-connection.md)
- [F4.1: Database models](docs/f4.1-database-models.md)
- [F4.2: User registration](docs/f4.2-user-registration.md)

The README is the **current setup guide**. Feature reports under `docs/` preserve implementation details and historical progress.
