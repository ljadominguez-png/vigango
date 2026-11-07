# Backend documentation

This directory contains implementation reports and feature-specific notes for ViganGo. Keep [`../README.md`](../README.md) focused on setup and everyday development; keep technical history here.

| Feature | Document                                                           | Scope                                                                                                           |
| ------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| F3      | [Database connection](f3-database-connection.md)                   | Supabase PostgreSQL setup, SQLAlchemy engine/sessions, and connection testing.                                  |
| F3.1    | [Google sign-in database support](f3.1-google-sign-in-database.md) | Nullable password hashes, Google IDs, and login-method constraints in the `User` model.                         |
| F3.2    | [Case-insensitive user uniqueness](f3.2-case-insensitive-users.md) | `lower(username)`/`lower(email)` unique indexes, rollout checks, and database verification.                     |
| F4.1    | [Database models](f4.1-database-models.md)                         | Database tables, model relationships, and historical model verification.                                        |
| F4.2    | [User registration and Google support](f4.2-user-registration.md)  | Password registration, Google token verification, account creation, security tests, and PostgreSQL integration. |

For each future Scrum feature, create one focused report and link it here. Never include real passwords, ID tokens, or production connection strings in documentation.
