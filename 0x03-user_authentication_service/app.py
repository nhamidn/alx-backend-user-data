#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify, request, abort

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """end-point to logout."""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


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


@app.route("/users", methods=["POST"])
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
