#!/usr/bin/env python3
"""
Session auth module.
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth Class."""

    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kw = {
            'user_id': user_id,
            'session_id': session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID from database based on session_id."""
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID."""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
