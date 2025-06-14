from flask import Blueprint, request, jsonify
from flasgger import swag_from

from operations_and_monitoring.application.services import MonitoringService

monitoring_api = Blueprint('monitoring', __name__)

monitoring_service = MonitoringService()

@monitoring_api.route('/thermostats', methods=['GET'])
@swag_from({
    'tags': ['Monitoring'],
})
def get_thermostat_state():
    """
    Retrieves the state of a thermostat by its IP address.
    
    :return: JSON response with the thermostat state.

    ---
    parameters:
      - in: query
        name: ip_address
        type: string
        required: true
    responses:
        200:
            description: The state of the thermostat.
            schema:
            type: object
            properties:
                state:
                type: boolean
                description: True if the thermostat is on, False otherwise.
        400:
            description: Bad request if the IP address is not provided.
    """
    ip_address = request.args.get('ip_address')
    if not ip_address:
        return jsonify({"error": "IP address is required"}), 400

    state = monitoring_service.get_state_thermostat(ip_address)
    return jsonify({"ip_address": ip_address, "state": state}), 200