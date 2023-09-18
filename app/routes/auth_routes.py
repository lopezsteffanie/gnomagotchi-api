from flask import Blueprint, jsonify, request, session
from ..service.auth_service import AuthService
import os
import datetime
import jwt

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

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

    # Generate a JWT token
    jwt_token = generate_jwt_token(uid)

    return handle_response({"message": "User logged in successfully", "uid": uid, "token": jwt_token}, 200)
  except Exception as e:
    return handle_response({"error": str(e)}, 401)
  
@auth_bp.route("/logout", methods=["POST"])
def logout():
  """
  Route for user logout.
  """
  try:
    # Get the JWT token from the request headers
    token = request.headers.get('Authorization')

    if not token:
      return handle_response({"error": "User is not logged in"}, 401)
    try:
      # Verify and decode the JWT token
      payload =jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
      return handle_response({"message": "User logged out successfully"}, 200)
    except jwt.ExpiredSignatureError:
      return handle_response({"error": "Token has expired"}, 401)
    except jwt.InvalidTokenError:
      return handle_response({"error": "Invalid token"}, 401)
  except Exception as e:
    return handle_response({"error": str(e)}, 500)

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
  """
  Route for user forgot password.
  """
  try:
    email = request.json.get("email")

    if error := AuthService.forgot_password(email):
      return handle_response({"error": error}, 400)

    return handle_response({"message": "Password reset email sent successfully"}, 200)
  except Exception as e:
    return handle_response({"error": str(e)}, 400)
  
def generate_jwt_token(user_uid):
  payload = {
      'uid': user_uid,
      'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
  }

  return jwt.encode(payload, SECRET_KEY, algorithm='HS256')