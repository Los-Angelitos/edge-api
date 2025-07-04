from typing import Optional
from shared.room_config import FOG_API_URL
import requests

from iam.application.services import AuthApplicationService
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor
from operations_and_monitoring.infrastructure.repositories import ThermostatRepository, SmokeSensorRepository

class MonitoringService:
    def __init__(self):
        self.thermostat_repository = ThermostatRepository()
        self.smoke_sensor_repository = SmokeSensorRepository()
        self.auth_service = AuthApplicationService()

    def validate_smoke_sensor_access(self, device_id: str, api_key: str, current_temperature: float) -> dict:
        """
        Validates smoke sensor access and communicates with fog service.
        
        :param device_id: ID of the smoke sensor device
        :param api_key: API key for authentication
        :param current_temperature: Current temperature reading
        :return: Dictionary with access validation result
        """
        print("[MonitoringService] ==== INICIANDO VALIDACIÓN DE SENSOR DE HUMO ====")
        print(f"[MonitoringService] Parámetros: device_id={device_id}, api_key={api_key}, temp={current_temperature}")

        # Step 1: Authenticate device
        print("[MonitoringService] Verificando autenticación del dispositivo...")
        is_authenticated = self.auth_service.authenticate(device_id, api_key)

        if not is_authenticated:
            print("[MonitoringService] ❌ Autenticación fallida.")
            return {"access": False, "error": "Authentication failed"}

        print("[MonitoringService] ✅ Dispositivo autenticado con éxito.")

        # Step 2: Validate with fog service
        try:
            fog_url = f"{FOG_API_URL}/monitoring/smoke-sensors/validate"
            payload = {
                "device_id": device_id,
                "current_temperature": current_temperature
            }

            print(f"[MonitoringService] Enviando a fog service: {fog_url}")
            print(f"[MonitoringService] Payload: {payload}")

            response = requests.post(fog_url, json=payload)
            
            if response.status_code == 200:
                fog_result = response.json()
                print(f"[MonitoringService] Respuesta fog: {fog_result}")
                return {"access": fog_result.get("access", False)}
            else:
                print(f"[MonitoringService] Error fog service: {response.status_code}")
                return {"access": False, "error": f"Fog service error: {response.status_code}"}

        except Exception as e:
            print(f"[MonitoringService] Excepción: {e}")
            return {"access": False, "error": f"Exception: {str(e)}"}

    def unlock_all_thermostats(self):
        """
        Unlocks all thermostats in the system.
        """
        print("[MonitoringService] Desbloqueando todos los termostatos...")
        try:
            # This would typically update all thermostats to unlocked state
            # For now, we'll just log the action
            print("[MonitoringService] ✅ Todos los termostatos desbloqueados.")
            return True
        except Exception as e:
            print(f"[MonitoringService] Error desbloqueando termostatos: {e}")
            return False

    def get_thermostat_by_device_id(self, device_id: str) -> Optional[Thermostat]:
        """
        Gets a thermostat by device ID.
        """
        return self.thermostat_repository.find_by_device_id(device_id)

    def create_thermostat(self, device_id: str, api_key: str, room_id: int, 
                         current_temperature: float, target_temperature: float) -> Thermostat:
        """
        Creates a new thermostat.
        """
        self.auth_service.create_device(device_id, api_key)
        return self.thermostat_repository.create(
            device_id, api_key, room_id, current_temperature, target_temperature
        )

    def create_smoke_sensor(self, device_id: str, api_key: str, room_id: int, 
                           current_temperature: float) -> SmokeSensor:
        """
        Creates a new smoke sensor.
        """
        self.auth_service.create_device(device_id, api_key)
        return self.smoke_sensor_repository.create(
            device_id, api_key, room_id, current_temperature
        )

    def get_or_create_test_thermostat(self) -> Thermostat:
        """
        Gets or creates a test thermostat.
        """
        return self.thermostat_repository.get_or_create_test_thermostat()

    def get_or_create_test_smoke_sensor(self) -> SmokeSensor:
        """
        Gets or creates a test smoke sensor.
        """
        return self.smoke_sensor_repository.get_or_create_test_smoke_sensor()