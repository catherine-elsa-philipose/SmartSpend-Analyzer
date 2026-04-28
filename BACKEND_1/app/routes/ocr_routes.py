from flask import Blueprint, request, jsonify
import pytesseract
from PIL import Image
import io

ocr_bp = Blueprint('ocr_bp', __name__)

def clean_ocr_data(raw_text):
    """
    Cleans OCR extracted text.
    Removes unwanted characters, extra spaces, and fixes common issues.
    """
    import re

    # Remove unnecessary newlines and combine lines
    cleaned_text = re.sub(r'\n+', '\n', raw_text.strip())

    # Remove any non-ASCII characters (if needed)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)

    # Remove very short lines (noise)
    lines = cleaned_text.split('\n')
    lines = [line.strip() for line in lines if len(line.strip()) > 2]
    cleaned_text = '\n'.join(lines)

    return cleaned_text

@ocr_bp.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        extracted_text = pytesseract.image_to_string(image)
        cleaned = clean_ocr_data(extracted_text)

        return jsonify({"extracted_text": cleaned})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
