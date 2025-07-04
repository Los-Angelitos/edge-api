from typing import Optional
from datetime import datetime

from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel, SmokeSensor as SmokeSensorModel
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor
from shared.infrastructure.utilities import Utilities

class ThermostatRepository:
    @staticmethod
    def find_by_device_id(device_id: str) -> Optional[Thermostat]:
        try:
            thermostat = ThermostatModel.get(ThermostatModel.device_id == device_id)
            return Thermostat(
                device_id=thermostat.device_id,
                api_key=thermostat.api_key,
                room_id=thermostat.room_id,
                current_temperature=thermostat.current_temperature,
                target_temperature=thermostat.target_temperature
            )
        except ThermostatModel.DoesNotExist:
            return None

    @staticmethod
    def create(device_id: str, api_key: str, room_id: int, 
               current_temperature: float, target_temperature: float) -> Thermostat:
        thermostat = ThermostatModel.create(
            device_id=device_id,
            api_key=api_key,
            room_id=room_id,
            current_temperature=current_temperature,
            target_temperature=target_temperature,
            created_at=datetime.now()
        )
        return Thermostat(
            device_id=thermostat.device_id,
            api_key=thermostat.api_key,
            room_id=thermostat.room_id,
            current_temperature=thermostat.current_temperature,
            target_temperature=thermostat.target_temperature
        )

    @staticmethod
    def get_or_create_test_thermostat() -> Thermostat:
        device_id = str(Utilities.generate_device_id())
        api_key = Utilities.generate_api_key()
        room_id = 101
        current_temperature = 22.5
        target_temperature = 24.0
        
        thermostat, created = ThermostatModel.get_or_create(
            device_id=device_id,
            defaults={
                'api_key': api_key,
                'room_id': room_id,
                'current_temperature': current_temperature,
                'target_temperature': target_temperature,
                'created_at': datetime.now()
            }
        )
        
        return Thermostat(
            device_id=thermostat.device_id,
            api_key=thermostat.api_key,
            room_id=thermostat.room_id,
            current_temperature=thermostat.current_temperature,
            target_temperature=thermostat.target_temperature
        )

class SmokeSensorRepository:
    @staticmethod
    def find_by_device_id(device_id: str) -> Optional[SmokeSensor]:
        try:
            sensor = SmokeSensorModel.get(SmokeSensorModel.device_id == device_id)
            return SmokeSensor(
                device_id=sensor.device_id,
                api_key=sensor.api_key,
                room_id=sensor.room_id,
                current_temperature=sensor.current_temperature
            )
        except SmokeSensorModel.DoesNotExist:
            return None

    @staticmethod
    def create(device_id: str, api_key: str, room_id: int, current_temperature: float) -> SmokeSensor:
        sensor = SmokeSensorModel.create(
            device_id=device_id,
            api_key=api_key,
            room_id=room_id,
            current_temperature=current_temperature,
            created_at=datetime.now()
        )
        return SmokeSensor(
            device_id=sensor.device_id,
            api_key=sensor.api_key,
            room_id=sensor.room_id,
            current_temperature=sensor.current_temperature
        )

    @staticmethod
    def get_or_create_test_smoke_sensor() -> SmokeSensor:
        device_id = str(Utilities.generate_device_id())
        api_key = Utilities.generate_api_key()
        room_id = 101
        current_temperature = 23.0
        
        sensor, created = SmokeSensorModel.get_or_create(
            device_id=device_id,
            defaults={
                'api_key': api_key,
                'room_id': room_id,
                'current_temperature': current_temperature,
                'created_at': datetime.now()
            }
        )
        
        return SmokeSensor(
            device_id=sensor.device_id,
            api_key=sensor.api_key,
            room_id=sensor.room_id,
            current_temperature=sensor.current_temperature
        )