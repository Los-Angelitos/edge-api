from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel, SmokeSensor as SmokeSensorModel
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor
from shared.infrastructure.database import db


class MonitoringRepository:
    @staticmethod
    def update_thermostat_state(device_id: str, api_key: str, room_id: int, new_state: str):
        try:
            thermostat = ThermostatModel.get(
                (ThermostatModel.device_id == device_id) &
                (ThermostatModel.api_key == api_key) &
                (ThermostatModel.room_id == room_id)
            )

            thermostat.state = new_state  # Solo actualizamos 'state'
            thermostat.save()

            return {
                "id": thermostat.id,
                "ip_address": thermostat.ip_address,
                "mac_address": thermostat.mac_address,
                "state": thermostat.state,
                "temperature": thermostat.temperature
            }

        except ThermostatModel.DoesNotExist:
            return None



    def get_last_changes_room(self, current_temperature: str, device_id: str):
        """
        Retrieve the last changes in temperature for a specific room.
        
        :param current_temperature: The current temperature to compare against.
        :param device_id: The ID of the device to query.
        :return: A dictionary containing the last changes in temperature.
        """
        thermostat = ThermostatModel.select().where(
            (ThermostatModel.device_id == device_id)
        ).first()

        print(f"Retrieved thermostat: {thermostat}")

        if not thermostat:
            raise ValueError("Device not found")

        thermostat_entity = Thermostat(
            id=thermostat.id,
            device_id=thermostat.device_id,
            api_key=thermostat.api_key,
            ip_address=thermostat.ip_address,
            mac_address=thermostat.mac_address,
            state=thermostat.state,
            temperature=thermostat.temperature,
        )

        return {
            'device_id': device_id,
            'current_temperature': thermostat_entity.temperature,
            'state': thermostat_entity.state,
        }
    