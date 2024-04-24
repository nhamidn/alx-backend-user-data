#!/usr/bin/env python3
"""Auth module."""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Method that hash a passord."""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
