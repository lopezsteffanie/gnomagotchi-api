from ..db import db
import random
import os
import json

class GnomeService:
  @staticmethod
  def is_user_in_session(session):
    return "user_uid" in session
  
  @staticmethod
  def create_gnome(session, db):  # sourcery skip: raise-specific-error
    if not GnomeService.is_user_in_session(session):
      raise Exception("User is not logged in")
    
    color = GnomeService.generate_random_color()
    personality = GnomeService.generate_random_personality()

    user_uid = session["user_uid"]

    gnome_ref = db.collection("gnomes").add({
        "color": color,
        "personality": personality,
        "user_uid": user_uid
    })

    gnome_id = gnome_ref[1].id # Access the ID from the tuple

    user_ref = db.collection("users").document(user_uid)
    user_data = user_ref.get().to_dict()

    gnome_ids = user_data.get("gnome_ids", [])
    gnome_ids.append(gnome_id)

    user_ref.update({"gnome_ids": gnome_ids})

    return gnome_id
  
  @staticmethod
  def generate_random_color():
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink"]
    return random.choice(colors)
  
  @staticmethod
  def generate_random_personality():  # sourcery skip: raise-from-previous-error, raise-specific-error
    # Construct the path to personalities.json
    json_file_path = os.path.join('app', 'personalities.json')
    # Load personality data from the JSON file
    with open(json_file_path, 'r') as json_file:
      try:
        personality_data = json.load(json_file)
      except json.JSONDecodeError as e:
        raise Exception(f"Error decoding JSON: {str(e)}")
      
    # Get a list of personality profiles
    personality_profiles = list(personality_data.keys())

    # Randomly select a personality profile
    selected_profile = random.choice(personality_profiles)

    # Return both the name of the personality and its stats
    return {"name": selected_profile, "stats": personality_data[selected_profile]}
  
  @staticmethod
  def name_gnome(gnome_id, gnome_name, session, db):
    # sourcery skip: raise-specific-error
    if not GnomeService.is_user_in_session(session):
      raise Exception("User is not logged in")
    
    user_uid = session["user_uid"]

    gnome_ref = db.collection("gnomes").document(gnome_id)
    gnome_data = gnome_ref.get().to_dict()

    if not gnome_data:
      raise Exception("Gnome not found")
    
    if gnome_data["user_uid"] != user_uid:
      raise Exception("Gnome does not belong to the current user")
    
    gnome_ref.update({
      "name": gnome_name,
      "age": 0,
      "user_uid": user_uid
    })

  @staticmethod
  def get_current_user_gnome_id(session, db):
    # sourcery skip: raise-specific-error
    if not GnomeService.is_user_in_session(session):
      raise Exception("User is not logged in")

    user_uid = session["user_uid"]

    user_ref = db.collection("users").document(user_uid)
    user_data = user_ref.get().to_dict()

    if gnome_ids := user_data.get("gnome_ids", []):
      return gnome_ids[-1]
    else:
      raise Exception("No gnomes associated with the current user")
    
  @staticmethod
  def update_gnome_age(gnome_id, new_age, session, db):
    # sourcery skip: raise-specific-error
    if not GnomeService.is_user_in_session(session):
      raise Exception("User is not logged in")
    
    user_uid = session["user_uid"]

    gnome_ref = db.collection("gnomes").document(gnome_id)
    gnome_data = gnome_ref.get().to_dict()

    if not gnome_data:
      raise Exception("Gnome not found")
    
    if gnome_data["user_uid"] != user_uid:
      raise Exception("Gnome does not belong to the current user")
    
    gnome_ref.update({"age": new_age})
      