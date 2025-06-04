from peewee import Model, CharField

from shared.infrastructure.database import db


class Device(Model):
    device_id = CharField(primary_key=True)
    ip_address = CharField()
    mac_address = CharField()
    state = CharField()
    class Meta:
        database = db
        table_name = 'devices'