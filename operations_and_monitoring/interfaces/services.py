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