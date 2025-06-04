
from peewee import SqliteDatabase

from iam.infrastructure.models import Device

from operations_and_monitoring.infrastructure.models import Thermostat, SmokeSensor

from inventory.infrastructure.models import RFIDCard

db = SqliteDatabase("sweet_manager_iot_db")

def init_db():
    db.connect()
    db.create_tables([Device, Thermostat, SmokeSensor, RFIDCard ], safe=True)
