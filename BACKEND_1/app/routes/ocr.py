from flask import Blueprint, request, jsonify
import pytesseract
from PIL import Image
import os

ocr_bp = Blueprint('ocr_bp', __name__)

@ocr_bp.route('/ocr', methods=['POST'])
def ocr():
    try:
        # Check if a file is included in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image = request.files['image']

        # Save the image temporarily
        image_path = os.path.join('temp_image.png')
        image.save(image_path)

        # Use Tesseract OCR to extract text
        extracted_text = pytesseract.image_to_string(Image.open(image_path))

        # Remove the temp image
        os.remove(image_path)

        # Return the extracted text
        return jsonify({'extracted_text': extracted_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
