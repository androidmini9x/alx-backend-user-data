#!/usr/bin/env python3
"""
Database Auth module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    '''SessionDBAuth Auth class'''

    def create_session(self, user_id=None):
        '''creates a Session ID for a user_id'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id,
                                   session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''Get a User ID based on a Session ID'''
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None
        user_session = user_session[0]

        if self.session_duration <= 0:
            return user_session.user_id

        expire_data = user_session.created_at \
            + timedelta(seconds=self.session_duration)
        if expire_data < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        '''Deletes the user session (Logout)'''
        if request is None or self.session_cookie(request) is None:
            return False
        session_id = self.session_cookie(request)
        user = self.user_id_for_session_id(session_id)
        if user is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return False
        user_session[0].remove()
        return True
