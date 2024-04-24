#!/usr/bin/env python3
"""Flask app module."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue"})
