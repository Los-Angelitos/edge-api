class Device:
    def __init__(self, device_id: str, api_key:str):
        self.device_id = device_id
        self.api_key = api_key

    def to_dict(self):
        return {
            'device_id': self.device_id,
            'api_key': self.api_key
        }

    def __repr__(self):
        return f"Device(id={self.id}, ip_address='{self.ip_address}', mac_address='{self.mac_address}', state='{self.state}')"