from typing import Optional
from datetime import datetime

from inventory.infrastructure.models import RFIDCard as RFIDCardModel
from inventory.domain.entities import RFIDCard
from shared.infrastructure.utilities import Utilities

class RFIDCardRepository:
    @staticmethod
    def find_by_all_attributes(device_id: str, api_key: str, room_id: int, uid: str) -> Optional[RFIDCard]:
        """
        Busca un registro RFID que coincida exactamente con todos los atributos proporcionados.
        
        :param device_id: ID del dispositivo
        :param api_key: Clave API del dispositivo
        :param room_id: ID de la habitación
        :param uid: UID de la tarjeta RFID
        :return: RFIDCard si existe una coincidencia exacta, None en caso contrario
        """
        try:
            rfid_card = RFIDCardModel.get(
                (RFIDCardModel.device_id == device_id) & 
                (RFIDCardModel.api_key == api_key) &
                (RFIDCardModel.room_id == room_id) &
                (RFIDCardModel.uid == uid)
            )
            return RFIDCard(
                device_id=rfid_card.device_id,
                api_key=rfid_card.api_key,
                room_id=rfid_card.room_id,
                uid=rfid_card.uid
            )
        except RFIDCardModel.DoesNotExist:
            return None

    @staticmethod
    def create(device_id: str, api_key: str, room_id: int, uid: str) -> RFIDCard:
        rfid_card = RFIDCardModel.create(
            device_id=device_id,
            api_key=api_key,
            room_id=room_id,
            uid=uid,
            created_at=datetime.now()
        )
        return RFIDCard(
            device_id=rfid_card.device_id,
            api_key=rfid_card.api_key,
            room_id=rfid_card.room_id,
            uid=rfid_card.uid
        )

    @staticmethod
    def get_or_create_test_rfid() -> RFIDCard:
        device_id = str(Utilities.generate_device_id())
        api_key = Utilities.generate_api_key()
        room_id = 101  # Room ID de prueba
        uid = f"rfid_test_{device_id[:8]}"
        
        rfid_card, created = RFIDCardModel.get_or_create(
            device_id=device_id,
            defaults={
                'api_key': api_key,
                'room_id': room_id,
                'uid': uid,
                'created_at': datetime.now()
            }
        )
        
        return RFIDCard(
            device_id=rfid_card.device_id,
            api_key=rfid_card.api_key,
            room_id=rfid_card.room_id,
            uid=rfid_card.uid
        )