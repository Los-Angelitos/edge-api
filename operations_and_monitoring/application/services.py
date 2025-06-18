from operations_and_monitoring.infrastructure.repositories import MonitoringRepository

class MonitoringService:
    def __init__(self):
        self.repository = MonitoringRepository()

    def update_thermostat_state(self, device_id: str, api_key: str, room_id: int, state: str, current_temperature: str) -> dict:
        """
        Update only the state field of a thermostat for a specific room.

        :param device_id: The ID of the thermostat device.
        :param api_key: The device's API key for authentication.
        :param room_id: The ID of the room where the device is located.
        :param state: The new state value to update.
        :return: A dictionary with the updated thermostat data or None if not found.
        """
        return self.repository.update_thermostat_state(device_id, api_key, room_id, state, current_temperature)

    def last_changes_room(self, current_temperature: str, device_id: str):
        """
        Retrieve the last changes in temperature for a specific room.
        
        :param device_id: The ID of the device to query.
        :param api_key: The API key for authentication.
        :return: A dictionary containing the last changes in temperature.
        """

        return self.repository.get_last_changes_room(current_temperature, device_id)