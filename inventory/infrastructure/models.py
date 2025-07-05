from peewee import Model, CharField, IntegerField, DateTimeField, AutoField
from shared.infrastructure.database import db

class RFIDCard(Model):
    device_id = CharField(primary_key=True)
    api_key = CharField()
    room_id = IntegerField()
    rfid_uid = CharField()
    created_at = DateTimeField()
    
    class Meta:
        database = db
        table_name = 'rfid_cards'
        # Opcional: agregar índices únicos si es necesario
        indexes = (
            # Crear un índice único para la combinación de device_id y rfid_uid
            (('device_id', 'rfid_uid'), True),
        )