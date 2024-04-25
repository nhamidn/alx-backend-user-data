#!/usr/bin/env python3
"""main module."""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test function to register new user."""
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/users', data=data)
    msg = {"email": email, "message": "user created"}
    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """Test function to login."""
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Test function for profile unlogged."""
    cookies = {
        "session_id": ""
    }
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    assert response.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
