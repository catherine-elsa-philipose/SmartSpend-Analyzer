from flask import Blueprint, request, jsonify
import pytesseract
from PIL import Image

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
def home():
    return 'SmartSpend API running!'

@routes_blueprint.route('/upload_receipt', methods=['POST'])
def upload_receipt():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        image = Image.open(image_file.stream)
        extracted_text = pytesseract.image_to_string(image)
        return jsonify({'extracted_text': extracted_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
