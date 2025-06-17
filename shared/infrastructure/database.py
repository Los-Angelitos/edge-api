from peewee import SqliteDatabase

db = SqliteDatabase("sweet_manager.db")

def init_db():
    from operations_and_monitoring.infrastructure.models import Thermostat, SmokeSensor
    from inventory.infrastructure.models import RFIDCard
    from iam.infrastructure.models import Device

    db.connect()
    db.create_tables([Thermostat, SmokeSensor, RFIDCard, Device], safe=True)

    print("Database initialized successfully.")