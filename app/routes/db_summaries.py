"""Database CRUD endpoints for Summaries"""

from flask import Blueprint, request, jsonify
from app.database import db
from app.models.summary import Summary
from app.models.document import HistorialDocumento

db_summaries_bp = Blueprint("db_summaries", __name__, url_prefix="/api/v1/db/summaries")

@db_summaries_bp.post("")
def create_summary():
    data = request.get_json()
    documento_id = data.get("documento_id")
    contenido = data.get("contenido")
    modelo_utilizado = data.get("modelo_utilizado", "gpt-4o")
    
    doc = db.session.get(HistorialDocumento, documento_id)
    if not doc:
        return jsonify({"detail": "Document not found"}), 404
        
    new_summary = Summary(
        documento_id=documento_id,
        contenido=contenido,
        modelo_utilizado=modelo_utilizado,
        status="completed"
    )
    
    # Backward compatibility logic for old tests
    if data.get("user_id"):
        new_summary.user_id = data.get("user_id")
        
    db.session.add(new_summary)
    db.session.commit()
    
    return jsonify(new_summary.to_dict()), 201

@db_summaries_bp.get("/<int:summary_id>")
def get_summary(summary_id):
    summary = db.session.get(Summary, summary_id)
    if not summary:
        return jsonify({"detail": "Summary not found"}), 404
    return jsonify(summary.to_dict()), 200
