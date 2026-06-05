from flask import Blueprint, request, jsonify
from app.services.conversation_service import ConversationService

db_conversations_bp = Blueprint("db_conversations", __name__, url_prefix="/api/v1/conversations")
conversation_service = ConversationService()

@db_conversations_bp.get("")
def list_conversations():
    notebook_id = request.args.get("notebook_id", type=int)
    return jsonify(conversation_service.get_all(notebook_id)), 200

@db_conversations_bp.post("")
def create_conversation():
    return jsonify(conversation_service.create(request.get_json())), 201

@db_conversations_bp.get("/<int:conv_id>")
def get_conversation(conv_id):
    result = conversation_service.get_by_id(conv_id)
    return jsonify(result) if result else (jsonify({"detail": "Not found"}), 404)

@db_conversations_bp.delete("/<int:conv_id>")
def delete_conversation(conv_id):
    return ("", 204) if conversation_service.delete(conv_id) else (jsonify({"detail": "Not found"}), 404)
