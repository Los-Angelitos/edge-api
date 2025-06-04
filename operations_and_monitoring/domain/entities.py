class Thermostat:
    def __init__(self, temperature, last_update):
        self.temperature = temperature
        self.last_update = last_update

class SmokeSensor:
    def __init__(self, last_analogic_value, last_alert_time=None):
        self.last_analogic_value = last_analogic_value
        self.last_alert_time = last_alert_time
