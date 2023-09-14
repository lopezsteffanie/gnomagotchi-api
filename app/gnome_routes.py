from flask import Blueprint, jsonify, request, session
import firebase_admin
from firebase_admin import auth, firestore
from .db import db
import json
import random
import os

gnome_bp = Blueprint("gnome", __name__, url_prefix="/api/gnome")

# Helper functions
def generate_random_color():
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]
    return random.choice(colors)

def generate_random_personality():
    # Construct the path to personalities.json
    json_file_path = os.path.join('app', 'personalities.json')
    # Load personality data from the JSON file
    with open(json_file_path, 'r') as json_file:
      try:
          personality_data = json.load(json_file)
      except json.JSONDecodeError as e:
          return jsonify({"error": f"Error decoding JSON: {str(e)}"}), 500

    
    # Get a list of personality profiles
    personality_profiles = list(personality_data.keys())

    # Randomly select a personality profile
    selected_profile = random.choice(personality_profiles)

    # Return both the name of the personality and its stats
    return {"name": selected_profile, "stats": personality_data[selected_profile]}

def is_user_in_session():
  # Check if user is logged in (UID is in the session)
  return "user_uid" in session

def get_current_user():
  return session["user_uid"]
    

@gnome_bp.route("/create", methods=["POST"])
def create_gnome():
  try:
    # Check if user is logged in (UID is in the session)
    if not is_user_in_session():
      return jsonify({"error": "user is not logged in"}), 401

    # Generate random color and personality
    color = generate_random_color()
    personality = generate_random_personality()

    # Get the user's UID from the session
    user_uid = session["user_uid"]

    gnome_ref = db.collection("gnomes").add({
        "color": color,
        "personality": personality,
        "user_uid": user_uid
    })

    gnome_id = gnome_ref[1].id # Access the ID from the tuple

    user_ref = db.collection("users").document(user_uid)
    user_data = user_ref.get().to_dict()

    # Get the list of gnome IDs from the user's document or initialize an empty list
    gnome_ids = user_data.get("gnome_ids", [])

    # Add the new gnome ID to the list
    gnome_ids.append(gnome_id)

    # Update the user's document with the updated gnome IDs
    user_ref.update({"gnome_ids": gnome_ids})

    # Return gnome data
    return jsonify({"message": "Gnome created successfully", "gnome_id": gnome_id}), 201
  
  except Exception as e:
      return jsonify({"error": str(e)}), 400
  
@gnome_bp.route("/name/<gnome_id>", methods=["POST"])
def name_gnome(gnome_id):
  try:
      # Check if user is logged in (UID is in the session)
      if not is_user_in_session():
        return jsonify({"error": "user is not logged in"}), 401
      
      # Get user input (gnome_name)
      gnome_data = request.json
      gnome_name = gnome_data.get("name")

      # Get the user's UID from the session
      user_uid = get_current_user()

      # Update the gnome document with the gnome_name and age
      gnome_ref = db.collection("gnomes").document(gnome_id)
      gnome_ref.update({
          "name": gnome_name,
          "age": 0,
          "user_uid": user_uid
      })

      return jsonify({"message": "Gnome named successfully", "gnome_id": gnome_id}), 200
  
  except Exception as e:
      return jsonify({"error": str(e)}), 400

@gnome_bp.route("/get-current-user-gnome-id", methods=["GET"])
def get_current_user_gnome_id():
    try:
      # Check if user is logged in (UID is in the session)
      if not is_user_in_session():
        return jsonify({"error": "user is not logged in"}), 401
        
      # Get the user's UID from the session
      user_uid = get_current_user()

      # Fetch the user's document from Firestore
      user_ref = db.collection("users").document(user_uid)
      user_data = user_ref.get().to_dict()

      # Get the list of fnome IDs associated with the current user
      gnome_ids = user_data.get("gnome_ids", [])

      if not gnome_ids:
        return jsonify({"error": "No gonmes associated with the current user"}), 404
      
      # Get the latest added gnome ID (the most recent in the list)
      latest_gnome_id = gnome_ids[-1]

      return jsonify({"gnome_id": latest_gnome_id}), 200

    except Exception as e:
      return jsonify({"error": str(e)}), 400
    
@gnome_bp.route("/update-age/<gnome_id>", methods=["POST"])
def update_gnome_age(gnome_id):
  try:
    # Check if user is logged in (UID is in the session)
    if not is_user_in_session():
      return jsonify({"erroor": "user is not logged in"}), 401
    
    # Get the user's UID from the session
    user_uid = get_current_user()

    # Check if the gnome with the specified ID exists and belongs to the uesr
    gnome_ref = db.collection("gnomes").document(gnome_id)
    gnome_data = gnome_ref.get().to_dict()

    if not gnome_data:
      return jsonify({"error": "Gnome not found"}), 404
    
    if gnome_data["user_uid"] != user_uid:
      return jsonify({"error": "Gnome does not belong to the current user"}), 403
    
    # Get the new age value from the request data
    request_data = request.json
    new_age = request_data.get("age")

    # Update the gnome's age in Firestore
    gnome_ref.update({"age": new_age})

    return jsonify({"messsage": "Gnome age updated successfully"}), 200
  
  except Exception as e:
    return jsonify({"error": str(e)}), 400