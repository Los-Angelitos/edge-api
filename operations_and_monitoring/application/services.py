from operations_and_monitoring.infrastructure.repositories import MonitoringRepository

class MonitoringService:
    def __init__(self):
        self.repository = MonitoringRepository()

    def last_changes_room(self, current_temperature: str, device_id: str):
        """
        Retrieve the last changes in temperature for a specific room.
        
        :param device_id: The ID of the device to query.
        :param api_key: The API key for authentication.
        :return: A dictionary containing the last changes in temperature.
        """

        return self.repository.get_last_changes_room(current_temperature, device_id)