from peewee import Model, CharField, IntegerField, DateTimeField
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