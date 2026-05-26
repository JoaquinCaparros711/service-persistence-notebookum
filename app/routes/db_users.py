"""Database CRUD endpoints for Users"""

from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

db_users_bp = Blueprint("db_users", __name__, url_prefix="/api/v1/db/users")
user_service = UserService()

@db_users_bp.get("")
def list_users():
    result = user_service.get_all()
    return jsonify(result), 200

@db_users_bp.post("")
def create_user():
    data = request.get_json()
    try:
        result = user_service.create(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400

@db_users_bp.get("/<int:user_id>")
def get_user(user_id):
    result = user_service.get_by_id(user_id)
    if result is None:
        return jsonify({"detail": "User not found"}), 404
    return jsonify(result), 200

@db_users_bp.patch("/<int:user_id>")
def update_user(user_id):
    data = request.get_json()
    try:
        result = user_service.update(user_id, data)
        if result is None:
            return jsonify({"detail": "User not found"}), 404
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400

@db_users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    success = user_service.delete(user_id)
    if not success:
        return jsonify({"detail": "User not found"}), 404
    return "", 204
