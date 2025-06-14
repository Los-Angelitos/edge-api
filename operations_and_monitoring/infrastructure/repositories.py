from shared.infrastructure.database import db
from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel, SmokeSensor as SmokeSensorModel

class MonitoringRepository:
    def get_state_thermostat(self, ip_address: str) -> bool:
        try:
            thermostat = ThermostatModel.get(ThermostatModel.ip_address == ip_address)
            
            return thermostat.state == 'on'
        except Exception as e:
            print(f"Error retrieving thermostat state: {e}")
            return False