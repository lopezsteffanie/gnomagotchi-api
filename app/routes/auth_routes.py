from flask import Blueprint, jsonify, request, session
from ..service.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

def handle_response(data, status_code=200):
  """
  Helper function to format the response and set the status code.
  """
  if "error" in data:
    status_code = 400 if status_code == 200 else status_code
  return jsonify(data), status_code

def get_email_and_password():
  """
  Helper function to extract email and password from the request JSON.
  """
  user_data = request.json
  email = user_data.get("email")
  password = user_data.get("password")
  return email, password

@auth_bp.route("/register", methods=["POST"])
def register():
  """
  Route for user registration.
  """
  try:
    email, password = get_email_and_password()

    # Create a new user with Firebase Authenticaton
    uid, error = AuthService.register_user(email, password)

    if error:
      return handle_response({"error": error}, 400)

    return handle_response({"message": "User registered successfully", "uid": uid}, 201)
  except Exception as e:
    return handle_response({"error": str(e)}, 400)
  
@auth_bp.route("/login", methods=["POST"])
def login():
  """
  Route for user login.
  """
  try:
    email, password = get_email_and_password()

    # Login the user
    uid, error = AuthService.login_user(email, password)

    if error:
      return handle_response({"error": error}, 401)

    # Store user UID in the session upon successful login
    session["user_uid"] = uid

    return handle_response({"message": "User logged in successfully", "uid": uid}, 200)
  except Exception as e:
    return handle_response({"error": str(e)}, 401)
  
@auth_bp.route("/logout", methods=["POST"])
def logout():
  """
  Route for user logout.
  """
  try:
    # Check if the user is logged in (UID is in the session)
    if "user_uid" in session:
      # Clear the user's session data upon logout
      session.pop("user_uid")

      return handle_response({"message": "User logged out successfully"}, 200)
    
    return handle_response({"message": "User is not logged in"}, 401);
  except Exception as e:
    return handle_response({"error": str(e)}, 500)
