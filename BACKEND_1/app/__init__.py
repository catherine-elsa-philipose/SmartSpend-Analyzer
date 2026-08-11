# SmartSpendAnalyser/backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the database initialization function
from .database import initialize_db

def create_app():
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = False 


    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    UPLOAD_FOLDER_PATH = os.path.join(PROJECT_ROOT, 'uploads')

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Example: 16 MB max upload size

    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER_PATH):
        os.makedirs(UPLOAD_FOLDER_PATH)
        print(f"Created upload folder: {UPLOAD_FOLDER_PATH}")

    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"], "supports_credentials": True}})

    # JWT Configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") 
    if not app.config["JWT_SECRET_KEY"]:
        raise ValueError("JWT_SECRET_KEY is not set in environment variables!")
    jwt = JWTManager(app)

    # Initialize MongoDB connection when the app is created
    initialize_db()

    # Register blueprint (defined in routes.py)
    from app.routes.routes import routes_blueprint as main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.ocr_routes import ocr_bp
    app.register_blueprint(main_bp, url_prefix='/api') 
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(ocr_bp, url_prefix='/api')
    # Register DataScience blueprint
    from app.datascience.routes import ds_bp
    app.register_blueprint(ds_bp, url_prefix='/api/ds')
    return app