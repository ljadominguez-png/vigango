"""Provide Google OAuth configuration for authentication services."""

import os


# Read the Google OAuth client ID from the process environment.
def get_google_client_id() -> str:
    return os.environ.get("GOOGLE_CLIENT_ID", "").strip()
