from flask import Blueprint, request, jsonify
from flasgger import swag_from

from operations_and_monitoring.application.services import MonitoringService

monitoring_api = Blueprint('monitoring', __name__)

monitoring_service = MonitoringService()

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
                    'room_id': {'type': 'integer'},
                    'current_value': {'type': 'number'}
                },
                'required': ['device_id', 'api_key', 'room_id', 'current_value']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Smoke sensor access validation successful',
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
def validate_smoke_sensor_access():
    """
    Validates smoke sensor access and communicates with fog service.

    This endpoint authenticates the smoke sensor device and sends the access
    validation request to the fog service.
    ---
    """
    try:
        # Get data from request JSON
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        device_id = data.get('device_id')
        api_key = data.get('api_key')
        room_id = data.get('room_id')
        current_value = data.get('current_value')

        missing_fields = []
        if not device_id:
            missing_fields.append("device_id")
        if not api_key:
            missing_fields.append("api_key")
        if room_id is None:
            missing_fields.append("room_id")
        if current_value is None:
            missing_fields.append("current_value")

        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Validate access
        result = monitoring_service.validate_smoke_sensor_access(device_id, api_key, room_id, current_value)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "access": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@monitoring_api.route('/thermostats', methods=['POST'])
@swag_from({
    'tags': ['Thermostats'],
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
                    'room_id': {'type': 'integer'},
                    'current_temperature': {'type': 'number'},
                    'target_temperature': {'type': 'number'}
                },
                'required': ['device_id', 'api_key', 'room_id', 'current_temperature', 'target_temperature']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Thermostat created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'},
                            'thermostat': {
                                'type': 'object',
                                'properties': {
                                    'device_id': {'type': 'string'},
                                    'room_id': {'type': 'integer'},
                                    'current_temperature': {'type': 'number'},
                                    'target_temperature': {'type': 'number'}
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {'description': 'Bad request'},
        500: {'description': 'Internal server error'}
    }
})
def create_thermostat():
    """
    Creates a new thermostat device.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        device_id = data.get('device_id')
        api_key = data.get('api_key')
        room_id = data.get('room_id')
        current_temperature = data.get('current_temperature')
        target_temperature = data.get('target_temperature')

        if not all([device_id, api_key, room_id is not None, 
                   current_temperature is not None, target_temperature is not None]):
            return jsonify({
                "error": "Missing required fields: device_id, api_key, room_id, current_temperature, target_temperature"
            }), 400

        thermostat = monitoring_service.create_thermostat(
            device_id, api_key, room_id, current_temperature, target_temperature
        )

        return jsonify({
            "message": "Thermostat created successfully",
            "thermostat": {
                "device_id": thermostat.device_id,
                "room_id": thermostat.room_id,
                "current_temperature": thermostat.current_temperature,
                "target_temperature": thermostat.target_temperature
            }
        }), 201

    except Exception as e:
        return jsonify({
            "error": f"Error creating thermostat: {str(e)}"
        }), 500



def create_smoke_sensor():
    """
    Creates a new smoke sensor device.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        device_id = data.get('device_id')
        api_key = data.get('api_key')
        room_id = data.get('room_id')
        current_temperature = data.get('current_temperature')

        if not all([device_id, api_key, room_id is not None, current_temperature is not None]):
            return jsonify({
                "error": "Missing required fields: device_id, api_key, room_id, current_temperature"
            }), 400

        smoke_sensor = monitoring_service.create_smoke_sensor(
            device_id, api_key, room_id, current_temperature
        )

        return jsonify({
            "message": "Smoke sensor created successfully",
            "smoke_sensor": {
                "device_id": smoke_sensor.device_id,
                "room_id": smoke_sensor.room_id,
                "current_temperature": smoke_sensor.current_temperature
            }
        }), 201

    except Exception as e:
        return jsonify({
            "error": f"Error creating smoke sensor: {str(e)}"
        }), 500


@monitoring_api.route('/thermostats/test', methods=['GET'])
@swag_from({
    'tags': ['Thermostats'],
    'responses': {
        200: {
            'description': 'Test thermostat retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'thermostat': {
                        'type': 'object',
                        'properties': {
                            'device_id': {'type': 'string'},
                            'api_key': {'type': 'string'},
                            'room_id': {'type': 'integer'},
                            'current_temperature': {'type': 'number'},
                            'target_temperature': {'type': 'number'}
                        }
                    }
                }
            }
        }
    }
})
def get_test_thermostat():
    """
    Gets or creates a test thermostat device.
    """
    try:
        thermostat = monitoring_service.get_or_create_test_thermostat()
        
        return jsonify({
            "thermostat": thermostat.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error getting test thermostat: {str(e)}"
        }), 500


def get_test_smoke_sensor():
    """
    Gets or creates a test smoke sensor device.
    """
    try:
        smoke_sensor = monitoring_service.get_or_create_test_smoke_sensor()
        
        return jsonify({
            "smoke_sensor": smoke_sensor.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error getting test smoke sensor: {str(e)}"
        }), 500