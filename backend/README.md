# ViganGo Backend

FastAPI backend for **ViganGo**, a local activities and tourism discovery platform for Vigan and Metro Vigan.

## Current features

| Method | Endpoint                | Purpose                                                                           |
| ------ | ----------------------- | --------------------------------------------------------------------------------- |
| `GET`  | `/health`               | Check that the API is responding.                                                 |
| `POST` | `/api/v1/auth/register` | Register with a validated email, username, and securely hashed password.          |
| `POST` | `/api/v1/auth/login`    | Log in with email and password; returns the profile and a JWT access token.       |
| `POST` | `/api/v1/auth/google`   | Register or sign in with a verified Google account; returns the profile and a JWT. |
| `GET`  | `/api/v1/auth/me`       | Return the signed-in user's profile (`Authorization: Bearer <access_token>`).     |

Email/password registration returns **201** on success, **409** for duplicate usernames/emails, and **422** for invalid input. Google sign-in returns **201** for a new user, **200** for a returning Google user, **401** for an invalid Google token, **409** for an account conflict, **422** when a new user lacks a valid username, and **503** if Google verification or JWT signing is unavailable or unconfigured.

Login returns **200** on success, **401** with the same generic message for an unknown email, wrong password, or Google-only account, **422** for invalid input, and **503** if `JWT_SECRET_KEY` is missing. `/me` returns **401** for a missing, invalid, or expired token.

Login and Google sign-in return `id`, `username`, `email`, `image_url`, `access_token`, and `token_type` (`"bearer"`). Access tokens expire after **15 minutes**. Responses never contain password hashes or Google IDs. Registration with `/register` does not log the user in; call `/login` afterward.

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

Login and Google sign-in sign access tokens with `JWT_SECRET_KEY` (at least 32 bytes), also read from the process environment. Generate a random key locally and never commit or share it:

```bash
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

Changing the key signs out every user, because existing tokens stop verifying.

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

The current F4.3 feature branch defines **82 test cases** (including parameterized checks); 17 of them need `TEST_DATABASE_URL`. Run this combined suite locally to verify the final result; earlier successful runs do not replace a final run after changes. Tests use a test-only `JWT_SECRET_KEY` from `tests/conftest.py`, so no real key is needed. The test fixture validates the local test-database target. **Never use the team's Supabase URL for these tests.**

Fresh `users` tables created from the merged F3.2 model receive case-insensitive unique indexes automatically; pre-existing databases require the separately applied index SQL. See the [F3.2 database report](docs/f3.2-case-insensitive-users.md).

## Documentation

Feature-specific reports are indexed in [backend/docs/README.md](docs/README.md):

- [F3: Database connection](docs/f3-database-connection.md)
- [F3.1: Google sign-in database support](docs/f3.1-google-sign-in-database.md)
- [F3.2: Case-insensitive user uniqueness](docs/f3.2-case-insensitive-users.md)
- [F4.1: Database models](docs/f4.1-database-models.md)
- [F4.2: User registration and Google support](docs/f4.2-user-registration.md)
- [F4.3: User login and access tokens](docs/f4.3-user-login.md)

The README is the **current developer setup guide**. Reports in `docs/` preserve implementation detail, verification evidence, and outstanding work.
