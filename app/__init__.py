from flask import Flask
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv
import os
import json
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()

    # Debug: Print environment variables
    # print(os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"))
    
    # Initialize Firebase app
    service_account_key_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    if not service_account_key_json:
        raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY not found in .env file")
    try:
        cred = credentials.Certificate(json.loads(service_account_key_json))
        firebase_admin.initialize_app(cred)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON in FIREBASE_SERVICE_ACCOUNT_KEY: " + str(e))

    # Enable CORS for all routes
    CORS(app)
    
    # Register Blueprints here
    from .routes import auth_bp
    app.register_blueprint(auth_bp)
    
    return app