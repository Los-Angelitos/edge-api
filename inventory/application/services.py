from typing import Optional
from shared.room_config import FOG_API_URL
import requests

from iam.application.services import AuthApplicationService
from inventory.domain.entities import RFIDCard
from inventory.infrastructure.repositories import RFIDCardRepository

class InventoryApplicationService:
    def __init__(self):
        self.rfid_repository = RFIDCardRepository()
        self.auth_service = AuthApplicationService()

    def validate_access(self, device_id: str, api_key: str, room_id: int, rfid_uid: str) -> dict:
        """
        Valida el acceso RFID verificando que el dispositivo esté autenticado.
        Luego consulta a otra API si el acceso está permitido con room_id y rfid_uid.
        Si el acceso es concedido, actualiza el estado del termostato (opcional).
        """
        print("[InventoryService] ==== INICIANDO VALIDACIÓN DE ACCESO ====")
        print(
            f"[InventoryService] Parámetros recibidos: device_id={device_id}, api_key={api_key}, room_id={room_id}, rfid_uid={rfid_uid}")

        # Paso 1: Autenticación del dispositivo
        print("[InventoryService] Verificando autenticación del dispositivo...")
        is_authenticated = self.auth_service.authenticate(device_id, api_key)

        if not is_authenticated:
            print("[InventoryService] ❌ Autenticación fallida.")
            return {"access": False}

        print("[InventoryService] ✅ Dispositivo autenticado con éxito.")

        # Paso 2: Validar con servicio externo (fog API)
        fog_url = f"{FOG_API_URL}/monitoring/devices/validation"
        payload = {
            "room_id": room_id,
            "u_id": rfid_uid
        }

        print(f"[InventoryService] Enviando solicitud POST a {fog_url} con payload:")
        print(payload)

        try:
            response = requests.post(fog_url, json=payload)

            print(f"[InventoryService] Código de respuesta de fog API: {response.status_code}")

            if response.status_code != 200:
                print("[InventoryService] ❌ Error en la respuesta de fog API.")
                return {"access": False}

            fog_result = response.json()
            print(f"[InventoryService] Respuesta de fog API: {fog_result}")

            access_granted = fog_result.get("access", False)

            return {"access": access_granted}

        except Exception as e:
            print(f"[InventoryService] 🛑 Excepción durante la solicitud a fog API: {e}")
            return {"access": False}

    def get_rfid_device_by_all_attributes(self, device_id: str, api_key: str, room_id: int, rfid_uid: str) -> Optional[RFIDCard]:
        """
        Obtiene un dispositivo RFID que coincida exactamente con todos los atributos.
        
        :param device_id: ID del dispositivo
        :param api_key: Clave API del dispositivo
        :param room_id: ID de la habitación
        :param rfid_uid: rfid_uid de la tarjeta RFID
        :return: Objeto RFIDCard si existe una coincidencia exacta, None en caso contrario
        """
        return self.rfid_repository.find_by_all_attributes(device_id, api_key, room_id, rfid_uid)

    def create_rfid_device(self, device_id: str, api_key: str, room_id: int, rfid_uid: str) -> RFIDCard:
        """
        Crea un nuevo dispositivo RFID.
        
        :param device_id: ID del dispositivo
        :param api_key: Clave API del dispositivo
        :param room_id: ID de la habitación
        :param rfid_uid: rfid_uid de la tarjeta RFID
        :return: Objeto RFIDCard creado
        """
        self.auth_service.create_device(device_id, api_key)
        return self.rfid_repository.create(device_id, api_key, room_id, rfid_uid)

    def get_or_create_test_rfid(self) -> RFIDCard:
        """
        Obtiene o crea un dispositivo RFID de prueba.
        
        :return: Objeto RFIDCard de prueba
        """
        return self.rfid_repository.get_or_create_test_rfid()