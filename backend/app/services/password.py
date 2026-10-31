"""Provide secure password hashing and verification utilities."""

from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


# Convert a plaintext password into a secure hash.
def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)


# Verify a plaintext password against its stored hash.
def verify_password(plain_password: str, stored_hash: str) -> bool:
    return password_hasher.verify(plain_password, stored_hash)
