from flask import Blueprint, request, jsonify, session
from user_model import create_user, verify_user

auth = Blueprint('auth', __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    success = create_user(data["username"], data["password"])
    return jsonify({"success": success}), 201 if success else 400

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    if verify_user(data["username"], data["password"]):
        session["username"] = data["username"]
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 401
