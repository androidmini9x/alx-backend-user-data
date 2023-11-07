#!/usr/bin/env python3
"""
Basic Auth module for the API
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from api.v1.views.users import User


class BasicAuth(Auth):
    """Basic Auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''Extract base64 from header request'''
        if authorization_header is None or \
                type(authorization_header) is not str or \
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        '''Decode base64 authorization'''
        if base64_authorization_header is None or \
                type(base64_authorization_header) is not str:
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)
            decoded = decoded.decode('utf-8')
        except Exception:
            return None

        return decoded

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        '''Extract credentials from decoded header'''
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) is not str or \
                ":" not in decoded_base64_authorization_header:
            return None, None
        user, email = decoded_base64_authorization_header.split(":", 1)
        return user, email

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''Fetch User based on credentials'''
        if type(user_email) is not str or \
                type(user_pwd) is not str:
            return None

        fetch_user = User.search({'email': user_email})

        for user in fetch_user:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''retrieves the User instance for a request'''
        header = self.authorization_header(request)
        extracted_base64 = self.extract_base64_authorization_header(header)
        decode_credintials = self.decode_base64_authorization_header(
            extracted_base64)
        username, password = self.extract_user_credentials(decode_credintials)
        user = self.user_object_from_credentials(username, password)
        return user
