from flask import Blueprint, jsonify, request, session
import firebase_admin
from firebase_admin import auth, credentials
from .db import db

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
  try:
    # Get user registration data from the request
    user_data = request.json
    email = user_data.get("email")
    password = user_data.get("password")

    # Create a new user with Firebase Authenticaton
    user = auth.create_user(
      email=email,
      password=password
    )

    # Sae the user's UID to Firestore
    user_ref = db.collection("users").document(user.uid)
    user_ref.set({
      "uid": user.uid,
    })

    return jsonify({"message": "User registered successfully", "uid": user.uid}), 201
  
  except Exception as e:
    return jsonify({"error": str(e)}), 400
  
@auth_bp.route("/login", methods=["POST"])
def login():
  try:
    # Get user login data from the request
    user_data = request.json
    email = user_data.get("email")
    password = user_data.get("password")

    # Sign in user with Firebase Authentication
    user = auth.get_user_by_email(email)

    # Store user UID in the session upon successful login
    session["user_uid"] = user.uid

    return jsonify({"message": "User logged in successfully", "uid": user.uid}), 200
  
  except Exception as e:
    return jsonify({"error": str(e)}), 401
  
@auth_bp.route("/logout", methods=["POST"])
def logout():
  try:
    # Check if the user is logged in (UID is in the session)
    if "user_uid" in session:
      # Clear the user's session data upon logout
      session.pop("user_uid")

      return jsonify({"message": "User logged out successfully"}), 200
    
    return jsonify({"message": "User is not logged in"});
  
  except Exception as e:
    return jsonify({"error": str(e)}), 500