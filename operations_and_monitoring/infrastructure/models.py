from peewee import *
from shared.infrastructure.database import db

class Thermostat(Model):
    id = AutoField(primary_key=True)
    device_id = CharField(unique=True, max_length=50)
    api_key = CharField(max_length=50)
    ip_address = CharField(max_length=15)
    mac_address = CharField(max_length=17)
    state = BooleanField(default=False)
    temperature = IntegerField()
    class Meta:
        database = db
        table_name = 'thermostats'

class SmokeSensor(Model):
    id = AutoField(primary_key=True)
    device_id = CharField(unique=True, max_length=50)
    api_key = CharField(max_length=50)
    ip_address = CharField(max_length=15)
    mac_address = CharField(max_length=17)
    state = BooleanField(default=False)
    last_analogic_value = FloatField()
    class Meta:
        database = db
        table_name = 'smoke_sensors'
