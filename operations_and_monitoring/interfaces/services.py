from flask import Blueprint, request, jsonify
from flasgger import swag_from

from operations_and_monitoring.application.services import MonitoringService

monitoring_api = Blueprint('monitoring', __name__)

monitoring_service = MonitoringService()

@monitoring_api.route('/thermostats', methods=['POST'])
@swag_from({
    'tags': ['Monitoring'],
})
def recover_last_changes_temperature_room():
    """
    Retrieve the last changes in temperature for a specific room.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            device_id:
              type: string
              description: The ID of the device to query.
            api_key:
              type: string
              description: The API key for authentication.
            current_temperature:
              type: integer
              description: The current temperature to compare against.
    responses:
        200:
            description: A dictionary containing the last changes in temperature.
        400:
            description: Invalid request, device_id and api_key are required.
        500:
            description: Internal server error.
    """

    # recover from body
    data = request.get_json()
    if not data or 'device_id' not in data or 'api_key' not in data:
        return jsonify({'error': 'Invalid request, device_id and api_key are required'}), 400
    
    device_id = data['device_id']
    api_key = data['api_key']
    current_temperature = data.get('current_temperature', None)

    print(data)

    try:
        result = monitoring_service.last_changes_room(current_temperature, device_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@monitoring_api.route('/validate-access', methods=['POST'])
@swag_from({
    'tags': ['Smoke Sensors'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'device_id': {'type': 'string'},
                    'api_key': {'type': 'string'},
                    'current_temperature': {'type': 'string'}
                },
                'required': ['device_id', 'api_key', 'current_temperature']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Access validation successful',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'access': {
                                'type': 'boolean',
                                'description': 'Whether access is granted or not'
                            }
                        }
                    }
                }
            }
        },
        400: {'description': 'Bad request - missing required fields'},
        401: {'description': 'Unauthorized - invalid device credentials'},
        500: {'description': 'Internal server error'}
    }
})
def validate_access():
    """
    Validates smoke sensor access and communicates with fog service.

    This endpoint authenticates the smoke sensor device and sends the access
    validation request to the fog service.
    ---
    """
    try:
        # Obtener datos del request JSON
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Ahora api_key también viene en el body
        device_id = data.get('device_id')
        api_key = data.get('api_key')
        current_temperature = data.get('current_temperature')

        missing_fields = []
        if not device_id:
            missing_fields.append("device_id")
        if not api_key:
            missing_fields.append("api_key")
        if not current_temperature:
            missing_fields.append("current_temperature")

        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Validar acceso
        result = monitoring_service.validate_access(device_id, api_key, current_temperature)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "access": False,
            "error": f"Internal server error: {str(e)}"
        }), 500