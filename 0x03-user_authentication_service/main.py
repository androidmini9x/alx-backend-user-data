#!/usr/bin/env python3
"""
End-to-end integration test
"""
import requests
URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Test register function"""
    postData = {"email": email, "password": password}
    response = requests.post(f'{URL}/users',
                             data=postData)
    assert response.status_code == 200, "TEST: Register failed"
    print("Passed: 'register_user'")


def log_in_wrong_password(email: str, password: str) -> None:
    """Test failed login"""
    postData = {"email": email, "password": password}
    response = requests.post(f'{URL}/sessions',
                             data=postData)
    assert response.status_code == 401, "TEST: Wrong Login failed"
    print("Passed: 'log_in_wrong_password'")


def log_in(email: str, password: str) -> str:
    """Test login"""
    postData = {"email": email, "password": password}
    response = requests.post(f'{URL}/sessions',
                             data=postData)
    assert response.status_code == 200, "TEST: Login failed"
    print("Passed: 'log_in'")
    session = response.cookies.get('session_id')
    return session


def profile_unlogged() -> None:
    """Test profile unlogged"""
    response = requests.get(f'{URL}/profile',
                            cookies={"session_id": ""})
    assert response.status_code == 403, "TEST: profile_unlogged failed"
    print("Passed: 'profile_unlogged'")


def profile_logged(session_id: str) -> None:
    """Test profile logged"""
    response = requests.get(f'{URL}/profile',
                            cookies={"session_id": session_id})
    assert response.status_code == 200, "TEST: profile logged failed"
    print("Passed: 'profile_logged'")


def log_out(session_id: str) -> None:
    """Test logout"""
    response = requests.delete(f'{URL}/sessions',
                               cookies={"session_id": session_id})
    assert response.status_code == 200, "TEST: Logout failed"
    print("Passed: 'log_out'")


def reset_password_token(email: str) -> str:
    """Test Reset passowrd"""
    response = requests.post(f'{URL}/reset_password',
                             data={"email": email})
    assert response.status_code == 200, "TEST: Reset token failed"
    print("Passed: 'reset_password_token'")
    token = response.json().get('reset_token')
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    response = requests.put(f'{URL}/reset_password',
                            data={"email": email,
                                  "reset_token": reset_token,
                                  "new_password": new_password})
    assert response.status_code == 200, "TEST: Update password Failed"
    print("Passed: 'update_password'")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
