from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/", methods=["GET"])
def hello_world():
  return "Hello, World!";

@auth_bp.route("/data", methods=["GET"])
def get_data():
  data = {"message": "This is an API endpoint", "value": 42}
  return jsonify(data)