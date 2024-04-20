#!/usr/bin/env python3
"""
Session auth module.
"""

from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session authentication system."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method thast creates a Session ID for a user_id."""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
