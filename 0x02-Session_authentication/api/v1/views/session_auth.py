#!/usr/bin/env python3
""" Session authentication interface
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    '''handles login process'''
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"}), 400

    fetch_user = User.search({'email': email})

    if len(fetch_user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user_obj = None
    for user in fetch_user:
        if user.is_valid_password(password):
            user_obj = user
            break

    if user_obj is None:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user_obj.id)
    resp = jsonify(user_obj.to_json())
    resp.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    '''handles logout process'''
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if not destroy_session:
        abort(404)
    return jsonify({}), 200
