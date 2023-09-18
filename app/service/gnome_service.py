import random
import os
import json
import jwt

class GnomeService:
  @staticmethod
  def create_gnome(user_uid, db):
    color = GnomeService.generate_random_color()
    personality = GnomeService.generate_random_personality()

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

    return gnome_id, color, personality
  
  @staticmethod
  def generate_random_color():
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink"]
    return random.choice(colors)
  
  @staticmethod
  def generate_random_personality():
    json_file_path = os.path.join('app', 'personalities.json')
    with open(json_file_path, 'r') as json_file:
      try:
        personality_data = json.load(json_file)
      except json.JSONDecodeError as e:
        raise Exception(f"Error decoding JSON: {str(e)}")
      
    personality_profiles = list(personality_data.keys())
    selected_profile = random.choice(personality_profiles)

    return {"name": selected_profile, "stats": personality_data[selected_profile]}
  
  @staticmethod
  def name_gnome(gnome_id, gnome_name, db):
    user_uid = GnomeService.get_user_id_from_jwt(jwt_token)

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
  def get_current_user_gnome_id(db, user_uid):
    user_ref = db.collection("users").document(user_uid)
    user_data = user_ref.get().to_dict()

    if gnome_ids := user_data.get("gnome_ids", []):
      return gnome_ids[-1]
    else:
      raise Exception("No gnomes associated with the current user")
    
  @staticmethod
  def get_gnome(gnome_id, db, user_uid):
    gnome_ref = db.collection("gnomes").document(gnome_id)
    gnome_data = gnome_ref.get().to_dict()

    if not gnome_data:
      raise Exception("Gnome not found")
    
    if gnome_data["user_uid"] != user_uid:
      raise Exception("Gnome does not belong to the current user")
    
    return gnome_data
    
  @staticmethod
  def update_gnome_age(gnome_id, new_age, db, user_uid):
    gnome_ref = db.collection("gnomes").document(gnome_id)
    gnome_data = gnome_ref.get().to_dict()

    if not gnome_data:
      raise Exception("Gnome not found")
    
    if gnome_data["user_uid"] != user_uid:
      raise Exception("Gnome does not belong to the current user")
    
    gnome_ref.update({"age": new_age})

  @staticmethod
  def verify_jwt_token(token):
    try:
      # Verify and decode the JWT token
      payload = jwt.decode(token, os.environ.get("FLASK_SECRET_KEY"), algorithms=['HS256'])

      user_uid = payload['uid']

      return user_uid, None
    except jwt.ExpiredSignatureError:
      return None, "Token has expired"
    except jwt.InvalidTokenError:
      return None, "Invalid token"