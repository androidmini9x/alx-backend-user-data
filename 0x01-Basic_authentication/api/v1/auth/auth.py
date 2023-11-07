#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Define which routes don't need authentication'''
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        '''Validate all requests to secure the API'''
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''Return the curent user'''
        return None
