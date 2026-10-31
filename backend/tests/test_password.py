"""Test password hashing and credential verification utilities."""

from app.services.password import hash_password, verify_password


# Verify that hashing does not return the original password.
def test_hash_password():
    password = "ExamplePassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$argon2id$")


# Verify that the correct password is accepted.
def test_verify_correct_password():
    password = "ExamplePassword123!"
    hashed = hash_password(password)

    result = verify_password(password, hashed)

    assert result is True


# Verify that an incorrect password is rejected.
def test_verify_incorrect_password():
    password = "ExamplePassword123!"
    hashed = hash_password(password)

    result = verify_password("WrongPassword123!", hashed)

    assert result is False
