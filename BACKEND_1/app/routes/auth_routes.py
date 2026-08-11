from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

auth_bp = Blueprint('auth_bp', __name__)


def get_users_col():
    try:
        from .. import database as db_mod
        if getattr(db_mod, 'users_collection', None) is not None:
            return db_mod.users_collection
        if hasattr(db_mod, 'get_users_collection'):
            col = db_mod.get_users_collection()
            if col is not None:
                return col
    except Exception:
        pass
    return None


# Signup route
@auth_bp.route('/register', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")

    users_collection = get_users_col()
    if users_collection is None:
        return jsonify({"message": "Database not available"}), 500

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    result = users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "email": email
    })

    return jsonify({"message": "User registered successfully", "user_id": str(result.inserted_id)}), 201


# Login route
@auth_bp.route('/user_login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users_collection = get_users_col()
    if users_collection is None:
        return jsonify({"message": "Database not available"}), 500

    user = users_collection.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Use the user's MongoDB ObjectId as the JWT identity — this is what datascience routes expect
    user_id = str(user["_id"])
    access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=12))

    return jsonify({"access_token": access_token}), 200

