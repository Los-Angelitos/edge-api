from flask import Blueprint, request, jsonify
from flasgger import swag_from

iam = Blueprint('iam', __name__)

@iam.route('/sign-in', methods=['GET'])
@swag_from({
    'tags': ['Authentication']
})
def auth():
    """
    Authenticate the user.
    ---
    responses:
      200:
        description: User authenticated successfully
      401:
        description: Unauthorized
    """
    # Here you would implement your authentication logic
    return jsonify({"message": "User authenticated successfully"}), 200