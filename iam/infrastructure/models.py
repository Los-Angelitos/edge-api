from peewee import Model, CharField, DateTimeField
import uuid
from shared.infrastructure.database import db


class Device(Model):
    id         = CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id  = CharField()
    api_key    = CharField()
    created_at = DateTimeField()
    class Meta:
        database   = db
        table_name = 'devices'