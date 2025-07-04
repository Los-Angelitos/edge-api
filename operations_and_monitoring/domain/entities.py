class Thermostat:
    def __init__(self, device_id: str, api_key: str, room_id: int, 
                 current_temperature: float, target_temperature: float):
        self.device_id = device_id
        self.api_key = api_key
        self.room_id = room_id
        self.current_temperature = current_temperature
        self.target_temperature = target_temperature

    def to_dict(self):
        return {
            'device_id': self.device_id,
            'api_key': self.api_key,
            'room_id': self.room_id,
            'current_temperature': self.current_temperature,
            'target_temperature': self.target_temperature
        }

    def __repr__(self):
        return f"Thermostat(device_id='{self.device_id}', room_id={self.room_id}, current_temp={self.current_temperature}°C, target_temp={self.target_temperature}°C)"

class SmokeSensor:
    def __init__(self, device_id: str, api_key: str, room_id: int, current_value: float):
        self.device_id = device_id
        self.api_key = api_key
        self.room_id = room_id
        self.current_value = current_value

    def to_dict(self):
        return {
            'device_id': self.device_id,
            'api_key': self.api_key,
            'room_id': self.room_id,
            'current_value': self.current_value
        }

    def __repr__(self):
        return f"SmokeSensor(device_id='{self.device_id}', room_id={self.room_id}, current_value={self.current_value})"
