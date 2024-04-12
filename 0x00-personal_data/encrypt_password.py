#!/usr/bin/env python3
"""encrypt_password module."""

import bcrypt


def hash_password(password: str) -> bytes:
    """function that returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function that checks if a passord is correct."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
