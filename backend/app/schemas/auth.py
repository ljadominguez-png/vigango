"""Define request and response schemas for user authentication."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Validate incoming user registration data.
class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=12, repr=False)


# Define the user information returned by the API.
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr
    image_url: str | None = None


# Validate Google identity tokens and optional registration usernames.
class GoogleAuthRequest(BaseModel):
    id_token: str = Field(
        min_length=1,
        max_length=16384,
        repr=False,
    )
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
    )


# Validate credentials submitted during email/password login.
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=1,
        repr=False,
    )
