from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

class ClientDTO:
    def __init__(self, ip: str, enc_cipher: AESGCMSIV, dec_cipher: AESGCMSIV, nonce: bytes, is_rescuer: bool, busy: bool = False):
        self.ip = ip
        self.enc_cipher = enc_cipher
        self.dec_cipher = dec_cipher
        self.nonce = nonce
        self.is_rescuer = is_rescuer
        self.busy = busy if is_rescuer else False
