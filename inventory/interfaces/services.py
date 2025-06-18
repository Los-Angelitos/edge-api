from flask import Blueprint, request, jsonify
from flasgger import swag_from

from inventory.application.services import InventoryApplicationService

inventory_api = Blueprint('inventory', __name__)

inventory_service = InventoryApplicationService()

@inventory_api.route('/validate-access', methods=['POST'])
@swag_from({
    'tags': ['Inventory'],
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
                    'rfid_uid': {'type': 'string'}
                },
                'required': ['device_id', 'api_key', 'room_id', 'rfid_uid']
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
    Validates RFID access and communicates with fog service.

    This endpoint authenticates the RFID device and sends the access
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
        room_id = data.get('room_id')
        rfid_uid = data.get('rfid_uid')

        missing_fields = []
        if not device_id:
            missing_fields.append("device_id")
        if not api_key:
            missing_fields.append("api_key")
        if room_id is None:  # cuidado con 0 válido
            missing_fields.append("room_id")
        if not rfid_uid:
            missing_fields.append("rfid_uid")

        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Validar acceso
        result = inventory_service.validate_access(device_id, api_key, room_id, rfid_uid)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "access": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@inventory_api.route('/rfid-devices', methods=['POST'])
@swag_from({
    'tags': ['Inventory'],
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
                    'rfid_uid': {'type': 'string'}
                },
                'required': ['device_id', 'api_key', 'room_id', 'rfid_uid']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'RFID device created successfully',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'},
                            'device': {
                                'type': 'object',
                                'properties': {
                                    'device_id': {'type': 'string'},
                                    'room_id': {'type': 'integer'},
                                    'rfid_uid': {'type': 'string'}
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
}, validation=True)  # <--- Esto es importante
def create_rfid_device():
    """
    Creates a new RFID device.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        device_id = data.get('device_id')
        api_key = data.get('api_key')
        room_id = data.get('room_id')
        rfid_uid = data.get('rfid_uid')

        if not all([device_id, api_key, room_id is not None, rfid_uid]):
            return jsonify({
                "error": "Missing required fields: device_id, api_key, room_id, rfid_uid"
            }), 400

        rfid_device = inventory_service.create_rfid_device(device_id, api_key, room_id, rfid_uid)

        return jsonify({
            "message": "RFID device created successfully",
            "device": {
                "device_id": rfid_device.device_id,
                "room_id": rfid_device.room_id,
                "rfid_uid": rfid_device.rfid_uid
            }
        }), 201

    except Exception as e:
        return jsonify({
            "error": f"Error creating RFID device: {str(e)}"
        }), 500

@inventory_api.route('/rfid-devices/test', methods=['GET'])
@swag_from({
    'tags': ['Inventory'],
    'responses': {
        200: {
            'description': 'Test RFID device retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'device': {
                        'type': 'object',
                        'properties': {
                            'device_id': {'type': 'string'},
                            'api_key': {'type': 'string'},
                            'room_id': {'type': 'integer'},
                            'rfid_uid': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
})
def get_test_rfid_device():
    """
    Gets or creates a test RFID device.
    ---
    """
    try:
        rfid_device = inventory_service.get_or_create_test_rfid()
        
        return jsonify({
            "device": rfid_device.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error getting test RFID device: {str(e)}"
        }), 500

