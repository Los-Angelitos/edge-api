from peewee import *

from iam.domain.entities import Device
from shared.infrastructure.database import db


class Thermostat(Device):
    temperature = FloatField()
    last_update = DateTimeField()
    class Meta:
        database = db
        table_name = 'thermostats'

class SmokeSensor(Device):
    last_analogic_value = FloatField()
    last_alert_time = DateTimeField(null=True)
    class Meta:
        database = db
        table_name = 'smoke_sensors'
