# populate_thermostats.py
import requests
from datetime import datetime

from shared.room_config import ROOM_ID
from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel
from shared.infrastructure.database import db


def populate_thermostats():
    db.connect()

    print(f"[Population] Fetching thermostats for room_id: {ROOM_ID}")
    url = f"https://tu-api.com/thermostats?room_id={ROOM_ID}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[Population] Error fetching thermostats: {response.status_code}")
        db.close()
        return

    data = response.json()
    created_count = 0

    for item in data:
        try:
            thermostat_id = item["id"]
            api_key = item["api_key"]
            ip_address = item.get("ip_address", "")
            mac_address = item.get("mac_address", "")
            state = item.get("state", "OFF")
            temperature = item.get("temperature", "0")

            ThermostatModel.get_or_create(
                device_id=thermostat_id,
                defaults={
                    "api_key": api_key,
                    "ip_address": ip_address,
                    "mac_address": mac_address,
                    "state": state,
                    "temperature": temperature,
                    "room_id": ROOM_ID,
                    "created_at": datetime.now()
                }
            )
            created_count += 1

        except KeyError as e:
            print(f"[Population] Missing field in thermostat: {e}")
        except Exception as e:
            print(f"[Population] Error creating thermostat {item}: {e}")

    print(f"[Population] {created_count} thermostats populated.")
    db.close()
