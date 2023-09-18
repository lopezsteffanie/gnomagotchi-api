from firebase_admin import auth
from ..db import db
from .custom_email_service import send_custom_email
import jwt

class AuthService:
  @staticmethod
  def register_user(email, password):
    try:
      # Create a new user with Firebase Authenticaton
      user = auth.create_user(
        email=email,
        password=password
      )

      # Save the user's UID to Firestore
      user_ref = db.collection("users").document(user.uid)
      user_ref.set({
        "uid": user.uid,
      })

      return user.uid, None
    
    except Exception as e:
      return None, str(e)
    
  @staticmethod
  def login_user(email, password):
    try:
      # Sign in user with Firebase Authentication
      user = auth.get_user_by_email(email)

      return user.uid, None
    
    except Exception as e:
      return None, str(e)
    
  @staticmethod
  def forgot_password(email):
    try:
      # Send password reset email
      reset_link = auth.generate_password_reset_link(email)
      send_custom_email(email, reset_link)
      return None
    
    except Exception as e:
      return str(e)