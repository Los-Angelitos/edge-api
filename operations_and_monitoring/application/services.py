from operations_and_monitoring.infrastructure.repositories import MonitoringRepository
from typing import Optional
from shared.room_config import FOG_API_URL
import requests
from shared.infrastructure.database import db
from iam.application.services import AuthApplicationService
from operations_and_monitoring.infrastructure.models import Thermostat


class MonitoringService:
    def __init__(self):
        self.repository = MonitoringRepository()
        self.auth_service = AuthApplicationService()

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

    def unlock_all_thermostats(self):
        try:
            query = Thermostat.update(state=True)
            rows_updated = query.execute()
            print(f"[Repository] {rows_updated} thermostats updated to unlocked.")
        except Exception as e:
            print(f"[Repository] Error updating thermostats: {e}")

    def last_changes_room(self, current_temperature: str, device_id: str):
        """
        Retrieve the last changes in temperature for a specific room.
        
        :param device_id: The ID of the device to query.
        :param api_key: The API key for authentication.
        :return: A dictionary containing the last changes in temperature.
        """

    def validate_access(self, device_id: str, api_key: str, current_temperature: str):
        """
        Send the current temperature, API key and device ID to the fog service to retrieve the last changes in the room.
        """
        # Paso 1: Autenticación del dispositivo
        print("[OperationsAndMonitoringService] Verificando autenticación del dispositivo...")
        is_authenticated = self.auth_service.authenticate(device_id, api_key)

        if not is_authenticated:
            print("[OperationsAndMonitoringService] ❌ Autenticación fallida.")
            return {"access": False}

        print("[OperationsAndMonitoringService] ✅ Dispositivo autenticado con éxito.")

        # Paso 2: Validar con servicio externo (fog API)
        fog_url = f"{FOG_API_URL}/monitoring/devices/validation"
        payload = {
            "current_temperature": current_temperature
        }

        print(f"[OperationsAndMonitoringService] Enviando solicitud POST a {fog_url} con payload:")
        print(payload)

        try:
            response = requests.post(fog_url, json=payload)

            print(f"[OperationsAndMonitoringService] Código de respuesta de fog API: {response.status_code}")

            if response.status_code != 200:
                print("[OperationsAndMonitoringService] ❌ Error en la respuesta de fog API.")
                return {"access": False}

            fog_result = response.json()
            print(f"[OperationsAndMonitoringService] Respuesta de fog API: {fog_result}")

            access_granted = fog_result.get("access", False)

            return {"access": access_granted}

        except Exception as e:
            print(f"[InventoryService] 🛑 Excepción durante la solicitud a fog API: {e}")
            return {"access": False}