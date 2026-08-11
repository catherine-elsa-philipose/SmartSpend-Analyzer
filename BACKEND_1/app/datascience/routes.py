# app/datascience/routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import numpy as np
from datetime import datetime
from bson.objectid import ObjectId

# Blueprint for DataScience APIs
ds_bp = Blueprint('datascience', __name__)


def get_receipts_col():
    """
    Safely retrieves the active MongoDB receipts collection.
    """
    try:
        from .. import database as db_mod
        if getattr(db_mod, 'receipts_collection', None) is not None:
            return db_mod.receipts_collection
        if hasattr(db_mod, 'get_receipts_collection'):
            col = db_mod.get_receipts_collection()
            if col is not None:
                return col
        if getattr(db_mod, 'db', None) is not None:
            db_obj = db_mod.db
            cols = db_obj.list_collection_names()
            if "Receipts" in cols:
                return db_obj["Receipts"]
            if "receipts" in cols:
                return db_obj["receipts"]
            return db_obj["Receipts"]
        if hasattr(db_mod, 'initialize_db'):
            db_mod.initialize_db()
            if getattr(db_mod, 'receipts_collection', None) is not None:
                return db_mod.receipts_collection
    except Exception:
        pass

    return None


def load_user_expenses(user_id):
    """
    Queries MongoDB for all receipts belonging to user_id,
    extracts amount, date, category, vendor, and items from parsed_data/timestamp,
    and returns a Pandas DataFrame with clean data types.
    """
    receipts_col = get_receipts_col()
    if receipts_col is None or not user_id:
        return pd.DataFrame(columns=['date', 'amount', 'category', 'vendor', 'items'])

    if ObjectId.is_valid(user_id):
        query = {"$or": [{"user_id": ObjectId(user_id)}, {"user_id": str(user_id)}]}
    else:
        query = {"user_id": str(user_id)}

    cursor = receipts_col.find(query).sort("timestamp", 1)
    
    rows = []
    for doc in cursor:
        parsed = doc.get("parsed_data") or {}
        
        # Determine amount: check parsed_data.total or parsed_data.amount
        raw_amount = parsed.get("total") if parsed.get("total") is not None else parsed.get("amount", 0.0)
        try:
            amount = float(raw_amount)
        except (ValueError, TypeError):
            amount = 0.0
            
        # Determine date: try parsed_data.date first, fallback to timestamp
        date_val = None
        raw_date = parsed.get("date")
        if raw_date:
            try:
                date_val = pd.to_datetime(raw_date, errors='coerce')
            except Exception:
                date_val = None
                
        if pd.isna(date_val) or date_val is None:
            raw_ts = doc.get("timestamp")
            if raw_ts:
                try:
                    date_val = pd.to_datetime(raw_ts, errors='coerce')
                except Exception:
                    date_val = None
                    
        if pd.isna(date_val) or date_val is None:
            date_val = pd.to_datetime(datetime.utcnow())

        category = parsed.get("category") or "Other"
        vendor = parsed.get("vendor") or "Unknown"
        items = parsed.get("items") or []

        rows.append({
            "date": date_val,
            "amount": amount,
            "category": str(category),
            "vendor": str(vendor),
            "items": items
        })

    if not rows:
        return pd.DataFrame(columns=['date', 'amount', 'category', 'vendor', 'items'])

    df = pd.DataFrame(rows)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df


@ds_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    df = load_user_expenses(user_id)

    if df.empty:
        return jsonify({
            'total_spent': 0.0,
            'by_category': {},
            'transaction_count': 0,
            'period': 'all_time',
            'message': 'No expense receipts found for user'
        }), 200

    total = round(float(df['amount'].sum()), 2)
    by_cat_raw = df.groupby('category')['amount'].sum().to_dict()
    by_category = {str(cat): round(float(amt), 2) for cat, amt in by_cat_raw.items()}

    return jsonify({
        'total_spent': total,
        'by_category': by_category,
        'transaction_count': int(len(df)),
        'period': 'all_time'
    }), 200


@ds_bp.route('/forecast', methods=['POST'])
@jwt_required()
def forecast():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    horizon = int(data.get('horizon', 6))  # months to forecast

    df = load_user_expenses(user_id)

    if df.empty or len(df) == 0:
        return jsonify({
            'success': False,
            'message': 'Insufficient historical expense data to generate a forecast. Please upload receipts first.',
            'forecast_months': [],
            'forecast_amounts': []
        }), 200

    # Calculate monthly aggregated spending
    try:
        valid_df = df.dropna(subset=['date']).copy()
        if valid_df.empty:
            return jsonify({
                'success': False,
                'message': 'Insufficient valid historical date records to generate forecast.',
                'forecast_months': [],
                'forecast_amounts': []
            }), 200

        try:
            monthly = valid_df.set_index('date').resample('ME')['amount'].sum()
        except ValueError:
            monthly = valid_df.set_index('date').resample('M')['amount'].sum()

        mean_val = float(monthly.mean()) if len(monthly) > 0 else 0.0
        if np.isnan(mean_val):
            mean_val = 0.0

        forecast_vals = [round(mean_val, 2)] * horizon
        future_months = [(datetime.utcnow().replace(day=1) + pd.DateOffset(months=i)).strftime('%Y-%m') for i in range(1, horizon + 1)]

        return jsonify({
            'success': True,
            'forecast_months': future_months,
            'forecast_amounts': forecast_vals
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Forecast calculation failed: {str(e)}'
        }), 500
