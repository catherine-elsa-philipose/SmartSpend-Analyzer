# app/datascience/routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import numpy as np
from datetime import datetime

# Blueprint for DataScience APIs

ds_bp = Blueprint('datascience', __name__)

# Utility: load expenses for a user (placeholder implementation)
def load_user_expenses(user_id):
    # TODO: replace with actual MongoDB query
    # For now, generate dummy data
    dates = pd.date_range(end=datetime.now(), periods=30)
    amounts = np.random.randint(10, 200, size=30)
    categories = np.random.choice(['Food', 'Travel', 'Shopping', 'Bills'], size=30)
    df = pd.DataFrame({'date': dates, 'amount': amounts, 'category': categories})
    return df

@ds_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    user_id = get_jwt_identity()
    df = load_user_expenses(user_id)
    total = df['amount'].sum()
    by_category = df.groupby('category')['amount'].sum().to_dict()
    return jsonify({
        'total_spent': total,
        'by_category': by_category,
        'period': 'last_30_days'
    })

@ds_bp.route('/forecast', methods=['POST'])
@jwt_required()
def forecast():
    data = request.get_json()
    horizon = data.get('horizon', 6)  # months to forecast
    user_id = get_jwt_identity()
    df = load_user_expenses(user_id)
    # Simple moving average forecast as placeholder
    monthly = df.set_index('date').resample('M')['amount'].sum()
    forecast_vals = [monthly.mean()] * horizon
    future_months = [(datetime.now().replace(day=1) + pd.DateOffset(months=i)).strftime('%Y-%m') for i in range(1, horizon+1)]
    return jsonify({
        'forecast_months': future_months,
        'forecast_amounts': forecast_vals
    })
