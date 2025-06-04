from peewee import *

from iam.domain.entities import Device
from shared.infrastructure.database import db

class RFIDCard(Model):
    uid = CharField(primary_key=True)
    class Meta:
        database = db
        table_name = 'rfid_cards'
