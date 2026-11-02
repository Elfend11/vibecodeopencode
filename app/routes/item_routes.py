from flask import Blueprint, jsonify, request

from app.errors import ApiError
from app.services import item_service

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("")
def list_items():
    """GET /items — return all items with their latest stock."""
    return jsonify(item_service.list_items()), 200


@bp.post("")
def create_item():
    """POST /items — add a new lab equipment master record."""
    payload = request.get_json(silent=True)
    if payload is None:
        raise ApiError("Request body harus berupa JSON yang valid.")

    item = item_service.create_item(payload)
    return jsonify(item), 201
