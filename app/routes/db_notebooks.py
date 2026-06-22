"""Database CRUD endpoints for Notebooks"""

from flask import Blueprint, jsonify, request

from app.services.notebook_service import NotebookService

db_notebooks_bp = Blueprint("db_notebooks", __name__, url_prefix="/api/v1/notebooks")
notebook_service = NotebookService()


@db_notebooks_bp.get("")
def list_notebooks():
    user_id = request.args.get("user_id", type=int)
    result = notebook_service.get_all(user_id)
    return jsonify(result), 200


@db_notebooks_bp.post("")
def create_notebook():
    data = request.get_json()
    result = notebook_service.create(data)
    return jsonify(result), 201


@db_notebooks_bp.get("/<int:notebook_id>")
def get_notebook(notebook_id):
    result = notebook_service.get_by_id(notebook_id)
    if result is None:
        return jsonify({"detail": "Notebook not found"}), 404
    return jsonify(result), 200


@db_notebooks_bp.patch("/<int:notebook_id>")
def update_notebook(notebook_id):
    data = request.get_json()
    result = notebook_service.update(notebook_id, data)
    if result is None:
        return jsonify({"detail": "Notebook not found"}), 404
    return jsonify(result), 200


@db_notebooks_bp.delete("/<int:notebook_id>")
def delete_notebook(notebook_id):
    success = notebook_service.delete(notebook_id)
    if not success:
        return jsonify({"detail": "Notebook not found"}), 404
    return "", 204
