from flask import Blueprint, request, jsonify
from app.services.message_service import MessageService

db_messages_bp = Blueprint("db_messages", __name__, url_prefix="/api/v1/messages")
message_service = MessageService()

@db_messages_bp.get("")
def list_messages():
    conversation_id = request.args.get("conversation_id", type=int)
    return jsonify(message_service.get_all(conversation_id)), 200

@db_messages_bp.post("")
def create_message():
    return jsonify(message_service.create(request.get_json())), 201
