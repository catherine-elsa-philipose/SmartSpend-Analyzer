from flask import Blueprint, request, jsonify
from PIL import Image
import io
import os
import tempfile

from ..ocr_utils import extract_text_from_image
from ..ocr_cleaner import clean_extracted_text

ocr_bp = Blueprint("ocr_bp", __name__)


@ocr_bp.route("/ocr", methods=["POST"])
def ocr():
    """
    Upload an image, extract text using OCR,
    clean the extracted text, and return the result.
    """

    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    temp_path = None

    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        # Extract text using the reusable OCR utility
        extracted_text = extract_text_from_image(temp_path)

        # Clean the extracted text using the reusable cleaner
        cleaned_data = clean_extracted_text(extracted_text)

        return jsonify({
            "success": True,
            "data": cleaned_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)