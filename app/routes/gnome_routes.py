from flask import Blueprint, jsonify, request, session
from ..service.gnome_service import GnomeService
from ..db import db

gnome_bp = Blueprint("gnome", __name__, url_prefix="/api/gnome")

def handle_response(data, status_code=200):
  if "error" in data:
    status_code = 400 if status_code == 200 else status_code
  return jsonify(data), status_code
    

@gnome_bp.route("/create", methods=["POST"])
def create_gnome():
  try:
    gnome_id = GnomeService.create_gnome(session, db)

    return handle_response({"message": "Gnome created successfully", "gnome_id": gnome_id}, 201)
  except Exception as e:
      return handle_response({"error": str(e)}, 400)
  
@gnome_bp.route("/name/<gnome_id>", methods=["POST"])
def name_gnome(gnome_id):
  try:
      gnome_name = request.json.get("name")
      GnomeService.name_gnome(gnome_id, gnome_name, session, db)

      return handle_response({"message": "Gnome named successfully", "gnome_id": gnome_id}, 200)
  except Exception as e:
      return handle_response({"error": str(e)}, 400)

@gnome_bp.route("/get-current-user-gnome-id", methods=["GET"])
def get_current_user_gnome_id():
    try:
      gnome_id = GnomeService.get_current_user_gnome_id(session, db)

      return handle_response({"gnome_id": gnome_id}, 200)
    except Exception as e:
      return handle_response({"error": str(e)}, 400)
    
@gnome_bp.route("/update-age/<gnome_id>", methods=["POST"])
def update_gnome_age(gnome_id):
  try:
    new_age = request.json.get("age")
    GnomeService.update_gnome_age(gnome_id, new_age, session, db)

    return handle_response({"messsage": "Gnome age updated successfully"}, 200)
  except Exception as e:
    return handle_response({"error": str(e)}, 400)