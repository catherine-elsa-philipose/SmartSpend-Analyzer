from flask import Blueprint, jsonify
from pymongo import MongoClient
from collections import defaultdict
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

# Connect to MongoDB (adjust URI if needed)
client = MongoClient("mongodb://localhost:27017/")
db = client["SmartSpend"]
collection = db["expenses"]

@dashboard_bp.route('/dashboard_summary', methods=['GET'])
def dashboard_summary():
    expenses = list(collection.find())

    category_summary = defaultdict(float)
    daily_spending = defaultdict(float)
    monthly_total = 0.0
    recent_transactions = []

    for item in expenses:
        try:
            category = item.get('category', 'Others')
            amount = float(item.get('amount', 0))
            date_str = item.get('date')
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                daily_spending[date.strftime('%Y-%m-%d')] += amount
            category_summary[category] += amount
            monthly_total += amount
            recent_transactions.append({
                "date": date_str,
                "merchant": item.get('merchant', 'Unknown'),
                "amount": amount
            })
        except Exception as e:
            continue

    # Sort transactions by date
    recent_transactions = sorted(recent_transactions, key=lambda x: x["date"], reverse=True)[:5]

    return jsonify({
        "monthly_total": round(monthly_total, 2),
        "category_summary": dict(category_summary),
        "daily_spending": dict(daily_spending),
        "recent_transactions": recent_transactions
    })
