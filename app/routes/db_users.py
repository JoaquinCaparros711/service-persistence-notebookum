"""Database CRUD endpoints for Users"""

from flask import Blueprint, request, jsonify
from app.database import db
from app.models.user import User

db_users_bp = Blueprint("db_users", __name__, url_prefix="/api/v1/db/users")

@db_users_bp.post("")
def create_user():
    data = request.get_json()
    email = data.get("email")
    nombre = data.get("nombre")
    
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"detail": "User already exists"}), 409
        
    new_user = User(email=email, nombre=nombre)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"detail": str(e)}), 500
    
    return jsonify(new_user.to_dict()), 201

@db_users_bp.get("/<int:user_id>")
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"detail": "User not found"}), 404
    return jsonify(user.to_dict()), 200
