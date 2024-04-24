#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify, request

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/users", methods=["POST"])
def users():
    """end-point to register a user."""
    email = request.form.get('email')
    password = request.form.get('password')

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
