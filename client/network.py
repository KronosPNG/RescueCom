import os
import requests

from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from common.services import crypto


def connect(uuid: str, skey_path: Path, certificate_path: Path):
    """
    Connect to the cloud by performing key exchange

    Args:
        uuid (str): client's uuid
        skey_path (Path): client's private key path
        certificate_path (Path): client's certificate path

    Returns:
        ciphers for encryption and decryption, an encryption nonce and the cloud's nonce

    Raises:
        TypeError: if any argument is of the wrong type
        Exception: for failed connection
    """

    if not isinstance(uuid, str) or not isinstance(skey_path, Path) or not isinstance(certificate_path, Path):
        raise TypeError("Wrong types for arguments")

    skey = crypto.load_signing_key(skey_path)
    certificate = crypto.load_certificate(certificate_path)

    nonce = os.urandom(12)
    signature = crypto.sign(skey, nonce)

    resp = requests.post("http://localhost:8000/connect", json={"uuid": uuid, "nonce": nonce, "certificate": certificate, "signature": signature})
    if not resp.ok:
        raise Exception("Couldn't connect, switch to bluetooth")

    data = resp.json()

    # raise KeyError
    cloud_certificate = data["certificate"]
    cloud_pkey = data["pkey"]
    cloud_signature = data["signature"]

    crypto.verify_certificate(cloud_certificate, cloud_signature, cloud_nonce)

    skey, pkey = crypto.gen_ecdh_keys()
    encoded_pkey = crypto.encode_ecdh_pkey(pkey)

    resp = requests.post("http://localhost:8000/pkey", json={"uuid": uuid, "public_key": encoded_pkey})
    if not resp.ok:
        raise Exception("Something went wrong")

    data = resp.json()

    # raises KeyError
    cloud_pkey = crypto.decode_ecdh_pkey(data["pkey"])

    key = crypto.derive_shared_key(skey, cloud_pkey)

    enc_cipher, dec_cipher = crypto.get_ciphers(key)

    return enc_cipher, dec_cipher, nonce, cloud_nonce
