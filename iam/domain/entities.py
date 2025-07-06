import uuid
from datetime import datetime
from typing import Optional

class Device:
    def __init__(self, device_id: str, api_key: str, created_at: Optional[datetime] = None, id: Optional[str] = None):
        self.id = id or str(uuid.uuid4())
        self.device_id = device_id
        self.api_key = api_key
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'api_key': self.api_key
        }

    def __repr__(self):
        return f"Device(id={self.id}, device_id='{self.device_id}', api_key='{self.api_key}')"