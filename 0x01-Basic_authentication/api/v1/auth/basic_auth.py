#!/usr/bin/env python3
"""
Basic_auth module.
"""

from .auth import Auth


class BasicAuth(Auth):
    """BasicAuth..."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
