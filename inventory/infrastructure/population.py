# populate_rfid_cards.py
import requests
from datetime import datetime

from shared.room_config import ROOM_ID, FOG_API_URL
from inventory.infrastructure.models import RFIDCard
from shared.infrastructure.database import db


def populate_rfid_cards():
    db.connect()

    print(f"[Population] Fetching RFID cards for room_id: {ROOM_ID}")
    url = f"{FOG_API_URL}/monitoring/devices/rfid-readers/{ROOM_ID}"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"[Population] Error fetching RFID cards: {response.status_code}")
        db.close()
        return

    data = response.json()
    created_count = 0

    for item in data:
        try:
            device_id = item["device_id"]
            api_key = item["api_key"]
            rfid_uid = item["u_id"]

            RFIDCard.get_or_create(
                device_id=device_id,
                defaults={
                    "api_key": api_key,
                    "room_id": ROOM_ID,
                    "rfid_uid": rfid_uid,
                    "created_at": datetime.now()
                }
            )
            created_count += 1

        except KeyError as e:
            print(f"[Population] Missing field in RFID card: {e}")
        except Exception as e:
            print(f"[Population] Error creating RFID card {item}: {e}")

    print(f"[Population] {created_count} RFID cards populated.")
    db.close()
