from iam.domain.entities import Device

class Thermostat(Device):
    def __init__(self, id, device_id, api_key ,ip_address, mac_address, state, temperature):
        super().__init__(device_id, api_key)
        self.id = id
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.state = state
        self.temperature = temperature

class SmokeSensor(Device):
    def __init__(self, id, device_id, api_key, ip_address, mac_address, state, last_analogic_value):
        super().__init__(device_id, api_key)
        self.id = id
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.state = state
        self.last_analogic_value = last_analogic_value
