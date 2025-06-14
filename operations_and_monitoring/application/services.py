from operations_and_monitoring.infrastructure.repositories import MonitoringRepository

class MonitoringService:
    def __init__(self):
        self.repository = MonitoringRepository()

    def get_state_thermostat(self, ip_address: str) -> bool:
        """
        Retrieves the state of a thermostat by its IP address.
        
        :param ip_address: The IP address of the thermostat.
        :return: True if the thermostat is on, False otherwise.
        """
        return self.repository.get_state_thermostat(ip_address)