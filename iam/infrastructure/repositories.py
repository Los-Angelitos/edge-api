# iam/infrastructure/repositories.py
from typing import Optional

from iam.infrastructure.models import Device as DeviceModel
from iam.domain.entities import Device
from shared.infrastructure.utilities import Utilities
from datetime import datetime


class DeviceRepository:
    @staticmethod
    def find_by_id_and_api_key(device_id: str, api_key: str) -> Optional[Device]:
        try:
            device = DeviceModel.get((DeviceModel.device_id == device_id) & (DeviceModel.api_key == api_key))
            return Device(device.device_id, device.api_key, device.created_at)
        except DeviceModel.DoesNotExist:  # Corregido: era DeviceModel.get().DoesNotExist
            return None

    @staticmethod
    def create(device_id: str, api_key: str) -> Device:
        device_model = DeviceModel.create(
            device_id=device_id,
            api_key=api_key,
            created_at=datetime.now()
        )
        return Device(
            device_id=device_model.device_id,
            api_key=device_model.api_key,
            created_at=device_model.created_at
        )

    @staticmethod
    def get_or_create_test_device() -> Optional[Device]:
        device_id = str(Utilities.generate_device_id())
        api_key = Utilities.generate_api_key()
        
        device, created = DeviceModel.get_or_create(
            device_id=device_id,
            defaults={
                'api_key': api_key,
                'created_at': datetime.now()
            }
        )
        return Device(device.device_id, device.api_key, device.created_at)