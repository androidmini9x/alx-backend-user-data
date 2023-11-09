#!/usr/bin/env python3
"""
Session Exp Auth module for the API
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth Auth class"""

    def __init__(self):
        """Initialize expiration date for session"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get a User ID based on a Session ID"""
        if session_id is None \
                or self.user_id_by_session_id.get(session_id) is None:
            return None
        user_session = self.user_id_by_session_id.get(session_id)

        if 'created_at' not in user_session:
            return None

        if self.session_duration <= 0:
            return user_session.get('user_id')

        expire_data = user_session.get('created_at') \
            + timedelta(seconds=self.session_duration)
        if expire_data < datetime.now():
            return None
        return user_session.get('user_id')
