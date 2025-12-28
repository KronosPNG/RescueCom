from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from common.models import *
from common.services.crypto import *
import os, requests

# TODO: do better
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH", "./certificates/cert.pem")


def multicast_emergency_to_rescuers():
    """
    Multicast an emergency to available Rescuers
    """

    pass

def assign_emergency_to_rescuer():
    """
    If more than one Rescuer accepts an emergency, choose one to assign it to
    """

    pass

def sync_new_request():
    """
    Synchronise a new emergency to figure out how important and urgent it is relative to known unresolved emergency
    """

    pass

def establish_connection(client_ip: str, client_nonce: bytes) -> tuple[AESGCMSIV, AESGCMSIV]:
    """
    Establish a connection with a client by performing key exchange

    Args:
        client_ip (str): client's ip address
        client_nonce (bytes): client's nonce for the session
    Returns:
        Encryption and decryption ciphers to use while communicating with the client
    Raises:
        TypeError: if any argument is of the wrong type
    """

    if not isinstance(client_ip, str) or not isinstance(client_nonce, bytes):
        raise TypeError("Wrong types for arguments")

    certificate = load_certificate(CERTIFICATE_PATH)

    nonce = os.urandom(12)

    skey, pkey = gen_ecdh_keys()

    signature = sign(skey, nonce)

    resp = requests.post(client_ip + "/certificate/verify", json={"certificate": cert, "nonce": nonce, "signature": signature})
    if not resp.ok:
        raise requests.RequestException("Request failed")

    # raises KeyError
    client_pkey_bytes = resp.json["pkey"]

    # raises ValueError
    client_pkey = decode_ecdh_pkey(client_pkey_bytes)

    encoded_pkey = encode_ecdh_pkey(pkey)
    resp = requests.post(client_ip + "/publickey/register", json={"public_key": encoded_pkey})

    key = derive_shared_key(skey, client_pkey)

    enc_cipher, dec_cipher = get_ciphers(key)

    return enc_cipher, dec_cipher
