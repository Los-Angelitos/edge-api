from peewee import *
from shared.infrastructure.database import db

class Thermostat(Model):
    id = AutoField(primary_key=True)
    ip_address = CharField(unique=True, max_length=15)
    mac_address = CharField(unique=True, max_length=17)
    state = CharField(choices=[('on', 'On'), ('off', 'Off')], default='off')
    temperature = FloatField()
    last_update = DateTimeField()
    class Meta:
        database = db
        table_name = 'thermostats'

class SmokeSensor(Model):
    id = AutoField(primary_key=True)
    ip_address = CharField(unique=True, max_length=15)
    mac_address = CharField(unique=True, max_length=17)
    state = CharField(choices=[('on', 'On'), ('off', 'Off')], default='off')
    last_analogic_value = FloatField()
    last_alert_time = DateTimeField(null=True)
    class Meta:
        database = db
        table_name = 'smoke_sensors'
