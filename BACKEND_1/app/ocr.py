from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from datetime import datetime
import pytesseract
from PIL import Image
import os

ocr_bp = Blueprint('ocr', __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["smartspend"]
receipts_collection = db["receipts_raw"]

@ocr_bp.route('/upload_receipt', methods=['POST'])
@jwt_required()
def upload_receipt():
    if 'image' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    # Save the file temporarily
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Extract text using pytesseract
    text = pytesseract.image_to_string(Image.open(filepath))

    # Remove temporary file
    os.remove(filepath)

    # Get username from JWT
    username = get_jwt_identity()

    # Store in MongoDB
    receipts_collection.insert_one({
        "username": username,
        "upload_date": datetime.now(),
        "extracted_text": text
    })

    return jsonify({
        "msg": "Text extracted and saved",
        "extracted_text": text
    })
