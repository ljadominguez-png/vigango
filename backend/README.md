# ViganGo Backend

FastAPI backend for **ViganGo**, a local activities and tourism discovery platform for Vigan and Metro Vigan.

## Current features

| Method | Endpoint                | Purpose                                                                           |
| ------ | ----------------------- | --------------------------------------------------------------------------------- |
| `GET`  | `/health`               | Check that the API is responding.                                                 |
| `POST` | `/api/v1/auth/register` | Register with a validated email, username, and securely hashed password.          |
| `POST` | `/api/v1/auth/google`   | Register a verified Google account or retrieve an existing Google-backed account. |

Email/password registration returns **201** on success, **409** for duplicate usernames/emails, and **422** for invalid input. Google registration returns **201** for a new user, **200** for a returning Google user, **401** for an invalid Google token, **409** for an account conflict, **422** when a new user lacks a valid username, and **503** if Google verification is unavailable or unconfigured.

Responses expose only approved user fields; they do not contain password hashes or Google IDs. **Neither registration endpoint issues a ViganGo access token or establishes a login session.**

## Tech stack

- **API:** Python, FastAPI, Pydantic
- **Database:** PostgreSQL (team-hosted Supabase), SQLAlchemy, Psycopg
- **Password hashing:** Argon2id via `pwdlib`
- **Google identity verification:** `google-auth`, with `requests` transport
- **Testing:** Pytest, HTTPX/FastAPI TestClient, isolated Docker PostgreSQL

## Local setup

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

If an existing `.venv` is already configured, activate it rather than recreating it. Keep `requirements.txt` updated with `pwdlib[argon2]`, `google-auth`, and `requests`.

Create `backend/.env` with a **team-authorized** database connection string:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
```

Do not commit `.env` or real credentials. For Google registration, obtain the OAuth **Web Client ID** from the frontend/OAuth configuration team and set it as a process environment variable **before** starting the API:

```bash
export GOOGLE_CLIENT_ID="your-google-web-client-id"
```

This backend currently reads `GOOGLE_CLIENT_ID` from the process environment using `app/services/google_config.py`; adding it directly to `.env` is **not** supported by the current `app/config.py` settings class without a settings change.

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

PostgreSQL integration tests are **skipped** if `TEST_DATABASE_URL` is unset. Start the disposable local PostgreSQL container described in [F4.2: User registration and Google support](docs/f4.2-user-registration.md), then run:

```bash
TEST_DATABASE_URL='postgresql+psycopg://vigango_test:local_only_password@127.0.0.1:55432/vigango_test' \
python -m pytest -v -ra
```

The current F4.2 feature branch defines **42 test cases** (including parameterized token checks). Run this combined suite locally to verify the final result; earlier successful runs do not replace a final run after changes. The test fixture validates the local test-database target. **Never use the team's Supabase URL for these tests.**

Fresh `users` tables created from the merged F3.2 model receive case-insensitive unique indexes automatically; pre-existing databases require the separately applied index SQL. See the [F3.2 database report](docs/f3.2-case-insensitive-users.md).

## Documentation

Feature-specific reports are indexed in [backend/docs/README.md](docs/README.md):

- [F3: Database connection](docs/f3-database-connection.md)
- [F3.1: Google sign-in database support](docs/f3.1-google-sign-in-database.md)
- [F3.2: Case-insensitive user uniqueness](docs/f3.2-case-insensitive-users.md)
- [F4.1: Database models](docs/f4.1-database-models.md)
- [F4.2: User registration and Google support](docs/f4.2-user-registration.md)

The README is the **current developer setup guide**. Reports in `docs/` preserve implementation detail, verification evidence, and outstanding work.
