from peewee import SqliteDatabase

db = SqliteDatabase("sweet_manager")

def init_db():
    from iam.infrastructure.models import Device
    from operations_and_monitoring.infrastructure.models import Thermostat, SmokeSensor
    from inventory.infrastructure.models import RFIDCard

    db.connect()
    db.create_tables([Device, Thermostat, SmokeSensor, RFIDCard ], safe=True)
