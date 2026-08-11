from flask import Blueprint, jsonify

routes_blueprint = Blueprint('routes', __name__)

# Home route
@routes_blueprint.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is running"})


# ✅ Dashboard data
@routes_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    return jsonify({
        "total_spending": 5000,
        "monthly_summary": "You spent ₹5000 this month"
    })


# ✅ Daily spending (for bar chart)
@routes_blueprint.route('/expenses', methods=['GET'])
def expenses():
    return jsonify([
        {"date": "2026-04-01", "amount": 200},
        {"date": "2026-04-02", "amount": 500},
        {"date": "2026-04-03", "amount": 300}
    ])


# ✅ Category spending (for pie chart)
@routes_blueprint.route('/categories', methods=['GET'])
@routes_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})