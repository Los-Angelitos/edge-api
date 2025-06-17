from typing import Optional

from inventory.domain.entities import RFIDCard
from inventory.infrastructure.repositories import RFIDCardRepository

class InventoryApplicationService:
    def __init__(self):
        self.rfid_repository = RFIDCardRepository()

    def validate_access(self, device_id: str, api_key: str, room_id: int, rfid_uid: str) -> dict:
        """
        Valida el acceso RFID verificando que todos los valores coincidan exactamente
        con un registro en la tabla rfid_codes.
        
        :param device_id: ID del dispositivo RFID
        :param api_key: Clave API del dispositivo
        :param room_id: ID de la habitación
        :param rfid_uid: UID de la tarjeta RFID
        :return: Respuesta con el estado de acceso
        """
        # Verificar que todos los atributos coincidan exactamente con un registro
        rfid_card = self.rfid_repository.find_by_all_attributes(device_id, api_key, room_id, rfid_uid)
        
        if rfid_card is not None:
            return {"access": True}
        else:
            return {"access": False}

    def get_rfid_device_by_all_attributes(self, device_id: str, api_key: str, room_id: int, uid: str) -> Optional[RFIDCard]:
        """
        Obtiene un dispositivo RFID que coincida exactamente con todos los atributos.
        
        :param device_id: ID del dispositivo
        :param api_key: Clave API del dispositivo
        :param room_id: ID de la habitación
        :param uid: UID de la tarjeta RFID
        :return: Objeto RFIDCard si existe una coincidencia exacta, None en caso contrario
        """
        return self.rfid_repository.find_by_all_attributes(device_id, api_key, room_id, uid)

    def create_rfid_device(self, device_id: str, api_key: str, room_id: int, uid: str) -> RFIDCard:
        """
        Crea un nuevo dispositivo RFID.
        
        :param device_id: ID del dispositivo
        :param api_key: Clave API del dispositivo
        :param room_id: ID de la habitación
        :param uid: UID de la tarjeta RFID
        :return: Objeto RFIDCard creado
        """
        return self.rfid_repository.create(device_id, api_key, room_id, uid)

    def get_or_create_test_rfid(self) -> RFIDCard:
        """
        Obtiene o crea un dispositivo RFID de prueba.
        
        :return: Objeto RFIDCard de prueba
        """
        return self.rfid_repository.get_or_create_test_rfid()