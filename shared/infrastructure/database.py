from peewee import SqliteDatabase

db = SqliteDatabase("sweet_manager.db")

def init_db():
    from operations_and_monitoring.infrastructure.models import Thermostat, SmokeSensor
    from inventory.infrastructure.models import RFIDCard

    db.connect()
    db.create_tables([Thermostat, SmokeSensor, RFIDCard ], safe=True)

    print("Database initialized successfully.")
