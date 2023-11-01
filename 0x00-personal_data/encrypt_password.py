#!/usr/bin/env python3
'''5. Encrypting passwords
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''Encrypt given password'''
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''validate that the password matches the hashed password'''
    return bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password)
