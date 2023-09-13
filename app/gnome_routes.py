from flask import Blueprint, jsonify, request, session
import firebase_admin
from firebase_admin import auth, firestore
from .db import db
import random

gnome_bp = Blueprint("gnome", __name__, url_prefix="/api/gnome")

@gnome_bp.route("/create", methods=["POST"])
def create_gnome():
  try:
    # Check if user is logged in (UID is in the session)
    if "user_uid" not in session:
      return jsonify({"error": "user is not logged in"}), 401
    
    # Get user input (gnome_name)
    gnome_data = request.json
    gnome_name = gnome_data.get("name")

    # Generate random color and personality
    color = generate_random_color()
    personality = generate_random_personality()

    # Get the user's UID from the session
    user_uid = session["user_uid"]

    db.firestore.client()

    gnome_ref = db.collection("gnomes").add({
      "name": gnome_name,
      "color": color,
      "personality": personality,
      "age": 0,
      "user_uid": user_uid
    })

    user_ref = db.collection("users").document(user_uid)
    user_data = user_ref.get()

    # Get the list of gnome IDs from the user's document or initialize an empty list
    gnome_ids = user_data.get("gnome_ids", [])
    
    # Add the new gnome ID to the list
    gnome_ids.append(gnome_ref.id)
    
    # Update the user's document with the updated gnome IDs
    user_ref.update({"gnome_ids": gnome_ids})

    # Return gnome data
    return jsonify({"message": "Gnome created successfully", "gnome_id": gnome_ref.id}), 201
  
  except Exception as e:
    return jsonify({"error", str(e)}), 400
  
# Helper functions for generating random color and personality
def generate_random_color():
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
    return random.choice(colors)

def generate_random_personality():
    personalities = [
        "friendly", "grumpy", "adventurous", "bookworm", "shy",
        "funny", "mysterious", "nature-loving", "creative", "loyal",
        "curious", "stubborn", "wise", "helpful", "mischievous"
    ]
    return random.choice(personalities)

