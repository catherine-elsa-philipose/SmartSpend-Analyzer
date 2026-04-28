from flask import Blueprint, request, jsonify
import pytesseract
from PIL import Image
import os

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/upload_receipt', methods=['POST'])
def upload_receipt():
    if 'receipt' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['receipt']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(file.stream)
        text = pytesseract.image_to_string(image)
        return jsonify({"extracted_text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
