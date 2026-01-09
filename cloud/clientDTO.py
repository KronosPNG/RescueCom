from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

@dataclass
class ClientDTO:
    ip: str
    enc_cipher: AESGCMSIV
    dec_cipher: AESGCMSIV
    nonce: bytes
    cloud_nonce: bytes
    is_rescuer: bool
    busy: bool = False
