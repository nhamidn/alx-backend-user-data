#!/usr/bin/env python3
"""
Auth module.
"""

from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """Class to manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method that validate is a path require authentication."""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method that get's the Authorization header.."""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Method that..."""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request."""
        if request is None:
            return None
        s_name = os.getenv('SESSION_NAME')
        return request.cookies.get(s_name)
