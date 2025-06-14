class Device:
    def __init__(self, id: int, ip_address: str, mac_address: str, state: str):
        self.id = id
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.state = state

    def __repr__(self):
        return f"Device(id={self.id}, ip_address='{self.ip_address}', mac_address='{self.mac_address}', state='{self.state}')"
        
    


