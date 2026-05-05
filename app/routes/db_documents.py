"""Database CRUD endpoints for Documents"""

from flask import Blueprint, request, jsonify
from app.database import db
from app.models.document import HistorialDocumento
from app.models.user import User

db_documents_bp = Blueprint("db_documents", __name__, url_prefix="/api/v1/db/documents")

@db_documents_bp.post("")
def create_document():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    nombre_archivo = data.get("nombre_archivo")
    tamanio_bytes = data.get("tamanio_bytes")
    
    user = db.session.get(User, usuario_id)
    if not user:
        return jsonify({"detail": "User not found"}), 404
        
    new_doc = HistorialDocumento(
        usuario_id=usuario_id,
        nombre_archivo=nombre_archivo,
        tamanio_bytes=tamanio_bytes,
        estado="pending"
    )
    db.session.add(new_doc)
    db.session.commit()
    
    return jsonify(new_doc.to_dict()), 201

@db_documents_bp.get("/<int:doc_id>")
def get_document(doc_id):
    doc = db.session.get(HistorialDocumento, doc_id)
    if not doc:
        return jsonify({"detail": "Document not found"}), 404
    return jsonify(doc.to_dict()), 200

@db_documents_bp.patch("/<int:doc_id>")
def update_document(doc_id):
    doc = db.session.get(HistorialDocumento, doc_id)
    if not doc:
        return jsonify({"detail": "Document not found"}), 404
        
    data = request.get_json()
    if "estado" in data:
        doc.estado = data["estado"]
    if "extracto_texto" in data:
        doc.extracto_texto = data["extracto_texto"]
        
    db.session.commit()
    return jsonify(doc.to_dict()), 200

@db_documents_bp.delete("/<int:doc_id>")
def delete_document(doc_id):
    doc = db.session.get(HistorialDocumento, doc_id)
    if not doc:
        return jsonify({"detail": "Document not found"}), 404
        
    db.session.delete(doc)
    db.session.commit()
    return "", 204
