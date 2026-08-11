from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

auth_bp = Blueprint('auth_bp', __name__)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["smartspend"]
users_collection = db["users"]

# Signup route
@auth_bp.route('/register', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully"}), 201

# Login route
@auth_bp.route('/user_login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, os.getenv("SECRET_KEY"), algorithm="HS256")

    return jsonify({"access_token": token})
