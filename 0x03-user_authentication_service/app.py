#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify, request, abort, redirect

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """end-point to update a user's password."""
    email = request.form['email']
    reset_token = request.form['reset_token']
    new_password = request.form['new_password']
    try:
        AUTH.update_password(reset_token, new_password)
        msg = {"email": email, "message": "Password updated"}
        return jsonify(msg), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """end-point to get reset password token."""
    try:
        email = request.form['email']
    except KeyError:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    msg = {"email": email, "reset_token": reset_token}
    return jsonify(msg), 200


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """end-point for profile."""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    msg = {"email": user.email}
    return jsonify(msg), 200


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """end-point to logout and redirect to home."""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """end-point for logging."""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)

    response.set_cookie("session_id", session_id)
    return response


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """end-point to register a user."""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
        res = {"email": "<registered email>",
               "message": "user created"}
        return jsonify(res)
    except ValueError:
        res = {"message": "email already registered"}
        return jsonify(res)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue"})
