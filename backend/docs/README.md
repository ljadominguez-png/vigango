# Backend documentation

This directory contains the ViganGo backend's implementation reports and feature-specific notes. Keep `../README.md` short and up to date; store historical feature work here instead of appending it to the main README.

| Feature | Document | Scope |
| --- | --- | --- |
| F3 | [Database connection](f3-database-connection.md) | Supabase PostgreSQL settings, engine, sessions, and connection verification. |
| F4.1 | [Database models](f4.1-database-models.md) | SQLAlchemy tables, relationships, and model verification. |
| F4.2 | [User registration](f4.2-user-registration.md) | Validation, Argon2id hashing, REST endpoint, and tests. |

For future Scrum tasks, add one focused Markdown report (for example, `f4.3-user-login.md`) and link it here. Avoid recording passwords, tokens, or production connection strings in documentation.
