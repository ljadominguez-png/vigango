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

## 8. Setup Instructions for Team Members

1. Clone the repository and navigate to the backend folder.
2. Create a .env file and add the database connection string:
   DATABASE_URL=your_supabase_connection_string
3. Create and activate the Python virtual environment:
   python -m venv venv
   .\venv\Scripts\Activate.ps1
4. Install the dependencies:
   pip install -r requirements.txt
5. Start the backend:
   uvicorn app.main:app --reload
6. Visit http://127.0.0.1:8000/docs to access Swagger UI.
Note: Team members must obtain the Supabase connection string from an authorized project member. Never commit or upload .env to GitHub.


---

# ViganGo -- F4: Database Models Documentation

**Developer:** [Your Name]\
**Date:** October 30, 2026\
**Branch:** `feat/f3-Database`\
**Status:** Completed

## 1. Overview

This task added the SQLAlchemy models for the ViganGo database. The
tables were created in Supabase using the team's SQL schema script, and
the models describe those same tables in Python so the FastAPI backend
can read and write data without writing raw SQL.

The models were tested against the live Supabase database. A test script
successfully loaded the categories and a listing, including its related
category and area.

## 2. What Is a Model?

A model is a Python class that represents one database table.

-   **The class** is the table (for example, `Listing` is the
    `listings` table).
-   **Each attribute** is a column (for example, `title`, `latitude`).
-   **Each object** created from the class is one row (for example, one
    listing such as Calle Crisologo).
-   **Relationships** let the code move between related rows, such as
    `listing.category.name` or `user.favorites`, without writing joins.

The models do not create tables in Supabase. They only describe tables
that already exist. The tables, the sign-up trigger, and the row-level
security rules come from the SQL schema script.

## 3. Models and Their Purpose

  -----------------------------------------------------------------------
  Model             Table               Purpose
  ----------------- ------------------- ---------------------------------
  `Category`        `categories`        The 8 category shortcuts:
                                        Heritage, Food, Culture,
                                        Recreation, Events, Local
                                        Products, Nature, Nightlife.

  `Area`            `areas`             Towns in Metro Vigan (Vigan City,
                                        Bantay, Caoayan, Santa, and
                                        others).

  `Listing`         `listings`          The main table. One place,
                                        activity, event, or product with
                                        its description, coordinates,
                                        fees, duration, and featured
                                        flag.

  `ListingImage`    `listing_images`    Photos for a listing. The image
                                        marked `is_cover` is the
                                        thumbnail.

  `OperatingHour`   `operating_hours`   Regular weekly schedule, one row
                                        per day (0 = Sunday to 6 =
                                        Saturday). Used for the "open
                                        now" filter.

  `EventSchedule`   `event_schedules`   Date-based schedules for
                                        festivals and recurring events.

  `Tag`             `tags`              Keywords such as "empanada" or
                                        "kalesa" that improve search.

  `listing_tags`    `listing_tags`      Join table linking listings and
                                        tags (many-to-many).

  `User`            `users`             App account with `username`,
                                        `email`, `password_hash`
                                        (hashed, never the plain
                                        password), and an optional
                                        profile `image_url`.

  `Favorite`        `favorites`         A user saving a listing. One row
                                        per user and listing.

  `ListingStats`    `listing_stats`     Stores how many users favorited
                                        each listing. Updated
                                        automatically by a database
                                        trigger.
  -----------------------------------------------------------------------

## 4. Relationships

-   A **Category** has many **Listings**.
-   An **Area** has many **Listings**.
-   A **Listing** has many **ListingImages**, **OperatingHours**, and
    **EventSchedules**.
-   A **Listing** and a **Tag** are many-to-many through `listing_tags`.
-   A **User** has many **Favorites**, and a **Listing** can be saved
    in many **Favorites**.
-   A **Listing** has one **ListingStats** row holding its favorite
    count.

Examples of what this allows in code:

``` python
listing.category.name      # "Heritage"
listing.area.name          # "Vigan City"
listing.images             # list of ListingImage objects
listing.tags               # list of Tag objects
user.favorites             # list of Favorite objects
```

## 5. Design Notes

-   **Shared base class:** All models use the `Base` from
    `app/database.py`, so they share the same engine and sessions.
-   **Column types match PostgreSQL:** Fees use `Numeric(10, 2)` for
    exact money values, coordinates use `Double`, and timestamps are
    timezone-aware.
-   **Defaults:** Values such as `fee_min`, `is_featured`, `status`, and
    `created_at` have database-side defaults, so rows can be inserted
    without providing them.
-   **Constraints are mirrored:** The status must be draft, published,
    or hidden. `fee_max` must be at least `fee_min`. `day_of_week` must
    be 0 to 6. A user cannot favorite the same listing twice.
-   **Cascade deletes:** Deleting a listing also removes its images,
    hours, schedules, tag links, and favorites. Deleting a user removes
    their favorites.
-   **Favorite counts:** `listing_stats.favorite_count` is maintained
    by database triggers. It goes up when a row is added to `favorites`
    and down when one is removed, so the app never updates it by hand.
    A second trigger creates the stats row for every new listing.
-   **Users and passwords:** Accounts are stored in our own `users`
    table and login is handled by the FastAPI backend, not Supabase
    Auth. Passwords are hashed (bcrypt or argon2) before saving, and
    only the hash is stored in `password_hash`.
-   **Privacy of user data:** The `users` and `favorites` tables have
    row-level security enabled with no public policies, so they cannot
    be read through Supabase's public API key. Only the backend can
    access them.
-   **No placeholder data:** The database only contains the 8
    categories and the area names. Listings are added with real data.

## 6. Files Created and Modified

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `backend/app/models/__init__.py`    Imports all models so they can be
                                      used as `from app.models import
                                      Listing`.

  `backend/app/models/category.py`    `Category` model.

  `backend/app/models/area.py`        `Area` model.

  `backend/app/models/listing.py`     `Listing`, `ListingImage`,
                                      `OperatingHour`, and
                                      `EventSchedule` models.

  `backend/app/models/tag.py`         `Tag` model and the `listing_tags`
                                      join table.

  `backend/app/models/user.py`        `User` and `Favorite` models.

  `backend/requirements.txt`          Re-saved as UTF-8 so it installs on
                                      all platforms.
  -----------------------------------------------------------------------

## 7. Verification

A test script (`check_models.py`) opened a database session, loaded all
categories, and loaded one listing together with its category and area.
The models returned the expected data from Supabase.

## 8. Example Usage

``` python
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Listing

with SessionLocal() as db:
    featured = db.scalars(
        select(Listing).where(Listing.is_featured == True)
    ).all()
    for listing in featured:
        print(listing.title, listing.category.name)
```

## 9. Remaining Tasks

-   Add real listing data (places, images, operating hours, tags) in
    Supabase.
-   Create the Pydantic schemas for API responses.
-   Create the API routers for categories, listings with filters, the
    map, and favorites.
-   Test the CRUD operations through the API.