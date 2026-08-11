from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from PIL import Image
import io
import os
import tempfile
import datetime

from ..ocr_utils import extract_text_from_image
from ..ocr_cleaner import clean_extracted_text

ocr_bp = Blueprint("ocr_bp", __name__)


def get_receipts_col():
    try:
        from .. import database as db_mod
        if getattr(db_mod, 'receipts_collection', None) is not None:
            return db_mod.receipts_collection
        if hasattr(db_mod, 'get_receipts_collection'):
            col = db_mod.get_receipts_collection()
            if col is not None:
                return col
    except Exception:
        pass
    return None


@ocr_bp.route("/ocr", methods=["POST"])
@jwt_required()
def ocr():
    """
    Upload an image, extract text using OCR,
    clean the extracted text, save to MongoDB, and return the result.
    """
    user_id = get_jwt_identity()

    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    temp_path = None

    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        # Extract and clean text
        extracted_text = extract_text_from_image(temp_path)
        cleaned_data = clean_extracted_text(extracted_text)

        # Save receipt to MongoDB
        receipts_col = get_receipts_col()
        if receipts_col is not None:
            receipt_doc = {
                "user_id": user_id,
                "image_path": temp_path,
                "extracted_text": extracted_text,
                "parsed_data": cleaned_data,
                "timestamp": datetime.datetime.utcnow()
            }
            receipts_col.insert_one(receipt_doc)

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