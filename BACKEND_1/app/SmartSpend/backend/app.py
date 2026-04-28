from flask import Flask
from flask_cors import CORS
from auth_routes import auth

app = Flask(__name__)
CORS(app)
app.secret_key = "your-secret-key"

app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)
