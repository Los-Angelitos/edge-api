from iam.domain.entities import Device

class Thermostat(Device):
    def __init__(self, id, ip_address, mac_address, state, temperature, last_update):
        super().__init__(id, ip_address, mac_address, state)
        self.temperature = temperature
        self.last_update = last_update

class SmokeSensor(Device):
    def __init__(self, id, ip_address, mac_address, state, last_analogic_value, last_alert_time=None):
        super().__init__(id, ip_address, mac_address, state)
        self.last_analogic_value = last_analogic_value
        self.last_alert_time = last_alert_time
