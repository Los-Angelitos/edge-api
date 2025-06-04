class Device:
    def __init__(self, ip_address, mac_address, state, device_id):
        self.device_id = device_id
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.state = state


