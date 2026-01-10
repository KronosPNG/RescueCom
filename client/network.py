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

    certificate_bytes = crypto.encode_certificate(certificate)

    # TODO: switch string to a proper name (maybe)
    resp = requests.post("http://localhost:8000/connect", json={
            "uuid": uuid, "nonce": nonce.hex(), "certificate": certificate_bytes.hex(), "signature": signature.hex()
        }
    )
    if not resp.ok:
        raise Exception("Something went wrong")

    data = resp.json()

    # raise KeyError
    cloud_certificate_bytes = bytes.fromhex(data["certificate"])
    cloud_nonce = bytes.fromhex(data["nonce"])
    cloud_signature = bytes.fromhex(data["signature"])

    cloud_certificate = crypto.decode_certificate(cloud_certificate_bytes)

    crypto.verify_certificate(cloud_certificate, cloud_signature, cloud_nonce)

    skey, pkey = crypto.gen_ecdh_keys()
    encoded_pkey = crypto.encode_ecdh_pkey(pkey)

    resp = requests.post("http://localhost:8000/pkey", json={"uuid": uuid, "public_key": encoded_pkey.hex()})
    if not resp.ok:
        raise Exception("Something went wrong")

    data = resp.json()

    # raises KeyError
    cloud_pkey = crypto.decode_ecdh_pkey(bytes.fromhex(data["pkey"]))

    key = crypto.derive_shared_key(skey, cloud_pkey)

    enc_cipher, dec_cipher = crypto.get_ciphers(key)

    return enc_cipher, dec_cipher, nonce, cloud_nonce
