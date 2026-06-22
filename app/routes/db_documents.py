"""Database CRUD endpoints for Documents"""

from flask import Blueprint, jsonify, request

from app.services.document_service import DocumentService

db_documents_bp = Blueprint("db_documents", __name__, url_prefix="/api/v1/documents")
document_service = DocumentService()


@db_documents_bp.get("")
def list_documents():
    user_id = request.args.get("user_id", type=int)
    result = document_service.get_all(user_id)
    return jsonify(result), 200


@db_documents_bp.post("")
def create_document():
    data = request.get_json()
    result = document_service.create(data)
    return jsonify(result), 201


@db_documents_bp.get("/<int:doc_id>")
def get_document(doc_id):
    result = document_service.get_by_id(doc_id)
    if result is None:
        return jsonify({"detail": "Document not found"}), 404
    return jsonify(result), 200


@db_documents_bp.patch("/<int:doc_id>")
def update_document(doc_id):
    data = request.get_json()
    result = document_service.update(doc_id, data)
    if result is None:
        return jsonify({"detail": "Document not found"}), 404
    return jsonify(result), 200


@db_documents_bp.delete("/<int:doc_id>")
def delete_document(doc_id):
    success = document_service.delete(doc_id)
    if not success:
        return jsonify({"detail": "Document not found"}), 404
    return "", 204
