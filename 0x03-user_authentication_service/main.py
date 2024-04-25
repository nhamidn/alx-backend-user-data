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


def log_in(email: str, password: str) -> str:
    """Test function for succesful login."""
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    msg = {"email": email, "message": "logged in"}
    assert response.status_code == 200
    assert response.json() == msg
    session_id = response.cookies.get("session_id")
    return session_id


def profile_logged(session_id: str) -> None:
    """Test function  for profile logged in."""
    cookies = {
        "session_id": session_id
    }
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    msg = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """Test function for logging out."""
    cookies = {
        "session_id": session_id
    }
    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)
    msg = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == msg


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
