#!/usr/bin/env python3
"""
Session Expiration module.
"""

from .session_auth import SessionAuth
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expiration system."""

    def __init__(self):
        """Init method."""
        session_duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with an expiration time."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id from session considering the expiration time."""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary['user_id']
        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        s_d = self.session_duration
        if created_at + timedelta(seconds=s_d) < datetime.now():
            return None
        return session_dictionary['user_id']
