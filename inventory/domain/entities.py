class RFIDCard:
    def __init__(self, device_id: str, api_key: str, room_id: int, rfid_uid: str):
        self.device_id = device_id
        self.api_key = api_key
        self.room_id = room_id
        self.rfid_uid = rfid_uid

    def to_dict(self):
        return {
            'device_id': self.device_id,
            'api_key': self.api_key,
            'room_id': self.room_id,
            'rfid_uid': self.rfid_uid
        }

    def __repr__(self):
        return f"RFIDCard(device_id='{self.device_id}', room_id={self.room_id}, uid='{self.rfid_uid}')"