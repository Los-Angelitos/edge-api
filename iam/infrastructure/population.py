# population.py
import requests
from datetime import datetime

from shared.room_config import ROOM_ID, FOG_API_URL
from iam.infrastructure.models import Device as DeviceModel
from shared.infrastructure.database import db



def populate_devices():
    db.connect()

    print(f"[Population] Fetching thermostats for room_id: {ROOM_ID}")
    url = f"{FOG_API_URL}/monitoring/devices/thermostats"
    params = {"room_id": ROOM_ID}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"[Population] Error fetching thermostats: {response.status_code}")
        db.close()
        return

    data = response.json()
    created_count = 0

    for device in data:
        try:
            device_id = device["id"]
            api_key = device["api_key"]

            DeviceModel.get_or_create(
                device_id=device_id,
                defaults={
                    "api_key": api_key,
                    "created_at": datetime.now()
                }
            )
            created_count += 1

        except KeyError as e:
            print(f"[Population] Missing field in device: {e}")
        except Exception as e:
            print(f"[Population] Error creating device {device}: {e}")

    print(f"[Population] {created_count} devices populated.")
    db.close()
