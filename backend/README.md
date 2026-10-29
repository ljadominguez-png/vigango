
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
