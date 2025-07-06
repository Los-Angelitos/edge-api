from flask import Blueprint, request, jsonify

from iam.application.services import AuthApplicationService

iam_api = Blueprint('iam', __name__)

auth_service = AuthApplicationService()

def authenticate_request():
    id = request.json.get('id') if request.json else None
    api_key = request.headers.get('X-API-Key')
    if not id or not api_key:
        return jsonify({"error": "Missing id or API key"}), 401
    if not auth_service.authenticate(id, api_key):
        return jsonify({"error": "Invalid id or API key"}), 401
    return None

