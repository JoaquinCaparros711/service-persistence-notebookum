"""Database CRUD endpoints for Summaries"""

from flask import Blueprint, jsonify, request

from app.services.summary_service import SummaryService

db_summaries_bp = Blueprint("db_summaries", __name__, url_prefix="/api/v1/summaries")
summary_service = SummaryService()


@db_summaries_bp.get("")
def list_summaries():
    documento_id = request.args.get("documento_id", type=int)
    result = summary_service.get_all(documento_id)
    return jsonify(result), 200


@db_summaries_bp.post("")
def create_summary():
    data = request.get_json()
    try:
        result = summary_service.create(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"detail": str(e)}), 404


@db_summaries_bp.get("/<int:summary_id>")
def get_summary(summary_id):
    result = summary_service.get_by_id(summary_id)
    if result is None:
        return jsonify({"detail": "Summary not found"}), 404
    return jsonify(result), 200


@db_summaries_bp.patch("/<int:summary_id>")
def update_summary(summary_id):
    data = request.get_json()
    result = summary_service.update(summary_id, data)
    if result is None:
        return jsonify({"detail": "Summary not found"}), 404
    return jsonify(result), 200


@db_summaries_bp.delete("/<int:summary_id>")
def delete_summary(summary_id):
    success = summary_service.delete(summary_id)
    if not success:
        return jsonify({"detail": "Summary not found"}), 404
    return "", 204
