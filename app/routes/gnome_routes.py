from flask import Blueprint, jsonify, request
from ..service.gnome_service import GnomeService
from ..db import db
import os

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

gnome_bp = Blueprint("gnome", __name__, url_prefix="/api/gnome")

def handle_response(data, status_code=200):
  if "error" in data:
    status_code = 400 if status_code == 200 else status_code
  return jsonify(data), status_code

@gnome_bp.route("/create", methods=["POST"])
def create_gnome():
  try:
    # Get the JWT token from the request headers
    token = request.headers.get('Authorization')

    # Verify the JWT token and get the user UID
    user_uid, token_error = GnomeService.verify_jwt_token(token)

    if token_error:
      return handle_response({"error": token_error}, 401)
    
    gnome_id, color, personality = GnomeService.create_gnome(user_uid, db)

    return handle_response({"message": "Gnome created successfully", "gnome_id": gnome_id, "color": color, "personality": personality}, 201)
  except Exception as e:
      return handle_response({"error": str(e)}, 400)
  
@gnome_bp.route("/name/<gnome_id>", methods=["POST"])
def name_gnome(gnome_id):
  try:
      # Get the JWT token from the request headers
      token = request.headers.get('Authorization')

      # Verify the JWT token and get the user UID
      user_uid, token_error = GnomeService.verify_jwt_token(token)

      if token_error:
        return handle_response({"error": token_error}, 401)
      
      gnome_name = request.json.get("name")
      GnomeService.name_gnome(gnome_id, gnome_name, db, user_uid)

      return handle_response({"message": "Gnome named successfully", "gnome_id": gnome_id}, 200)
  except Exception as e:
      return handle_response({"error": str(e)}, 400)

@gnome_bp.route("/get-current-user-gnome-id", methods=["GET"])
def get_current_user_gnome_id():
    try:
      # Get the JWT token from the request headers
      token = request.headers.get('Authorization')

      # Verify the JWT token and get the user UID
      user_uid, token_error = GnomeService.verify_jwt_token(token)

      if token_error:
        return handle_response({"error": token_error}, 401)
      
      gnome_id = GnomeService.get_current_user_gnome_id(db, user_uid)

      return handle_response({"gnome_id": gnome_id}, 200)
    except Exception as e:
      return handle_response({"error": str(e)}, 400)
    
@gnome_bp.route("/get-gnome/<gnome_id>", methods=["GET"])
def get_gnome(gnome_id):
  try:
    # Get the JWT token from the request headers
    token = request.headers.get('Authorization')

    # Verify the JWT token and get the user UID
    user_uid, token_error = GnomeService.verify_jwt_token(token)

    if token_error:
      return handle_response({"error": token_error}, 401)
    
    gnome = GnomeService.get_gnome(gnome_id, db, user_uid)

    return handle_response({"gnome": gnome}, 200)
  except Exception as e:
    return handle_response({"error": str(e)}, 400)
    
@gnome_bp.route("/update-age/<gnome_id>", methods=["POST"])
def update_gnome_age(gnome_id):
  try:
    # Get the JWT token from the request headers
    token = request.headers.get('Authorization')

    # Verify the JWT token and get the user UID
    user_uid, token_error = GnomeService.verify_jwt_token(token)

    if token_error:
      return handle_response({"error": token_error}, 401)
    
    new_age = request.json.get("age")
    GnomeService.update_gnome_age(gnome_id, new_age, db, user_uid)

    return handle_response({"messsage": "Gnome age updated successfully"}, 200)
  except Exception as e:
    return handle_response({"error": str(e)}, 400)