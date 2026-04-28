from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Register route blueprints
from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return "SmartSpend API Running"

if __name__ == '__main__':
    app.run(debug=True)
