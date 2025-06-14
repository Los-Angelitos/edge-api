from peewee import *
from shared.infrastructure.database import db

class RFIDCard(Model):
    device_id = CharField(primary_key=True)
    uid = CharField()
    class Meta:
        database = db
        table_name = 'rfid_cards'
