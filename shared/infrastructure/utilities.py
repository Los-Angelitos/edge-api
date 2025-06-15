import random
import secrets
import uuid

class Utilities:

    def __init__(self):
        pass

    @staticmethod
    def generate_ip() ->str:
        return ".".join(str(random.randint(1, 254)) for _ in range(4))
    
    @staticmethod
    def generate_mac_address() -> str:
        mac = [0x02, random.randint(0x00, 0x7F)] + [random.randint(0x00, 0xFF) for _ in range(4)]
        return ":".join(f"{b:02X}" for b in mac)
    
    @staticmethod
    def generate_device_id() -> str:
        return uuid.uuid4()
    
    @staticmethod
    def generate_api_key() -> str:
        return secrets.token_urlsafe(32)