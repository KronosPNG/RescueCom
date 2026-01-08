from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_private_key
from cryptography.x509 import (
        load_pem_x509_certificate, random_serial_number, Certificate, CertificateBuilder, Name, NameAttribute
)
from cryptography.x509.oid import NameOID

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey, EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from datetime import datetime
from pathlib import Path

def load_signing_key(path: Path) -> Ed25519PrivateKey:
    """
    Load signing key at a given path

    Args:
        path (Path): path where the key is located

    Returns:
        The private key found at path

    Raises:
        TypeError: if any argument is of the wrong type
        Exception: for unexpected errors
    """

    if not isinstance(path, Path):
        raise TypeError("Wrong types for arguments")

    try:
        with path.open() as f:
            return load_pem_private_key(f.read(), b"")
    except Exception as e:
        raise e

    return certificate

def load_certificate(path: Path) -> Certificate:
    """
    Load a certificate at a given path

    Args:
        path (Path): path where the certificate is located

    Returns:
        The certificate found at `path`

    Raises:
        TypeError: if any argument is of the wrong type
        Exception: for unexpected errors
    """

    if not isinstance(path, Path):
        raise TypeError("Wrong types for arguments")

    try:
        with path.open() as f:
            certificate = load_pem_x509_certificate(f.read())
    except Exception as e:
        raise e

    return certificate

def gen_certificate(country: str, state_or_province: str, locality: str, common_name: str, duration: int = 30) -> tuple[Ed25519PrivateKey, Certificate]:
    """
    Generate a private key and self-signed certificate to authenticate

    Args:
        country (str): country of residence
        state_or_province (str): state or province of residence within the country
        locality (str): locality within the state or province (often a city)
        common_name (str): name and surname
        duration (int): duration of the validity of the certificate in days (default: 30)
    Returns:
        The generated private key and certificate
    Raises:
        TypeError: if any argument is of the wrong type
        ValueError: for invalid duration
    """

    if not all(isinstance(x, str) for x in (country, state_or_province, locality, common_name)) or not isinstance(duration, int):
        raise TypeError("Wrong types for arguments")

    if duration < 1:
        raise ValueError("Duration should be 1 or more days")

    skey = Ed25519PrivateKey.generate()

    # self signed (might switch to Let's Encrypt)
    subject = issuer = Name([
        NameAttribute(NameOID.COUNTRY_NAME, country),
        NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province),
        NameAttribute(NameOID.LOCALITY_NAME, locality),
        NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    certificate = CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            skey.public_key()
        ).serial_number(
            random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + datetime.timedelta(days=duration)
        ).sign(
            skey, None
        )

    return skey, certificate

def verify_certificate(certificate: Certificate, signature: bytes, nonce: bytes) -> bool:
    """
    Verify a certificate and a nonce signature

    Args:
        certificate (Certificate): certificate to verify
        signature (bytes): challenge signature to verify
        nonce (bytes): challenge nonce whose signature must match `signature`
    Returns:
        Whether the certificate and signature are correct
    Raises:
        TypeError: if any argument is of the wrong type
        Warning: if the certificate is invalid
    """

    if not isinstance(certificate, Certificate) or not all(isinstance(x, bytes) for x in (signature, nonce)):
        raise TypeError("Wrong types for arguments")

    if certificate.not_valid_after_utc <= datetime.utcnow():
        raise Warning("Certificate expired, acquire a new one as soon as possible")

    pkey = certificate.public_key()

    try:
        # not self signed
        if certificate.issuer != certificate.subject:
            raise Exception

        pkey.verify(certificate.signature, certificate.tbs_certificate_bytes)
        pkey.verify(signature, nonce)
        return True

    except Exception as e:
        return False

def sign(skey: Ed25519PrivateKey, data: bytes) -> bytes:
    """
    Sign data using a private key

    Args:
        skey (Ed25519PrivateKey): private key to use to sign
        data (bytes): data to sign
    Returns:
        Signed data
    Raises:
        TypeError: if any argument is of the wrong type
    """

    if not isinstance(skey, Ed25519PrivateKey) or not isinstance(data, bytes):
        raise TypeError("Wrong types for arguments")

    return skey.sign(data)

def decode_ecdh_pkey(data: bytes) -> EllipticCurvePublicKey:
    """
    Decode an ECDH public key from encoded bytes

    Args
        data (bytes): encoded public key
    Returns:
        Decoded public key
    Raises:
        TypeError: if any argument is of the wrong type
        ValueError: if an invalid point is supplied
    """

    if not isinstance(data, bytes):
        raise TypeError("Wrong types for arguments")

    return EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), data)

def encode_ecdh_pkey(pkey: EllipticCurvePublicKey) -> bytes:
    """
    Encode an ECDH public key to a bytes object

    Args
        pkey (EllipticCurvePublicKey): public key to encode
    Returns:
        data (bytes): encoded public key
    Raises:
        TypeError: if any argument is of the wrong type
    """

    if not isinstance(data, EllipticCurvePublicKey):
        raise TypeError("Wrong types for arguments")

    return pkey.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

def gen_ecdh_keys() -> tuple[EllipticCurvePrivateKey, EllipticCurvePublicKey]:
    """
    Generate private and corresponding public ECDH keys

    Returns:
        A pair of ECDH keys, private and corresponding public
    """

    skey = ec.generate_private_key(ec.SECP256R1())
    pkey = skey.public_key()

    return skey, pkey

def derive_shared_key(skey: EllipticCurvePrivateKey, pkey: EllipticCurvePublicKey) -> bytes:
    """
    Derive a shared key after a succesful ECDH key exchange

    Args:
        skey (EllipticCurvePrivateKey): own private ECDH key
        pkey (EllipticCurvePublicKey): received public ECDH key
    Returns:
        The derived key
    Raises:
        TypeError: if the keys aren't of the correct types
        ValueError: if the public key is the given private key's public key
    """

    if not isinstance(skey, EllipticCurvePrivateKey) or not isinstance(pkey, EllipticCurvePublicKey):
        raise TypeError("Private and public keys are of the wrong type")

    if skey.public_key() == pkey:
        raise ValueError("Public key must not derive from given private key")

    shared_key = skey.exchange(ec.ECDH(), pkey)

    return HKDF(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = None,
            info = None
            ).derive(shared_key)

def get_ciphers(key: bytes) -> tuple[AESGCMSIV, AESGCMSIV]:
    """
    Generate two AESGCMSIV ciphers for encryption and decryption

    Args:
        key (bytes): the (derived) shared key
    Returns:
        A pair of symmetric AESGCMSIV ciphers, one for encryption, one for decryption
    Raises:
        TypeError: if the key isn't bytes
        ValueError: if the key isn't exactly 32 bytes long
    """

    if not isinstance(key, bytes):
        raise TypeError("Key should be bytes")

    if len(key) != 32:
        raise ValueError("Key should be 32 bytes long")

    return AESGCMSIV(key), AESGCMSIV(key)

def encrypt(cipher: AESGCMSIV, nonce: bytes, data: bytes, aad: bytes) -> bytes:
    """
    Encrypts with an AESGCMSIV cipher

    Args:
        cipher (AESGCMSIV): cipher to encrypt with
        nonce (bytes): 12 bytes long nonce to use for encryption
        data (bytes): data to encrypt
        aad (bytes): additional data that is authenticated but not encrypted
    Returns:
        Encrypted and authenticated data
    Raises:
        TypeError: if any argument is of the wrong type
        ValueError: if the nonce isn't exactly 12 bytes long
    """

    if not isinstance(cipher, AESGCMSIV) or not all(isinstance(x, bytes) for x in (nonce, data, aad)):
        raise TypeError("Wrong types for arguments")

    if len(nonce) != 12:
        raise ValueError("Nonce should be exactly 12 bytes long")

    return cipher.encrypt(nonce, data, aad)

def decrypt(cipher: AESGCMSIV, nonce: bytes, data: bytes, aad: bytes) -> bytes:
    """
    Decrypts with an AESGCMSIV cipher

    Args:
        cipher (AESGCMSIV): cipher to decrypt with
        nonce (bytes): 12 bytes long nonce to use for decryption
        data (bytes): data to decrypt
        aad (bytes): additional data to verify authentication
    Returns:
        Original plaintext
    Raises:
        TypeError: if any argument is of the wrong type
        ValueError: if the nonce isn't exactly 12 bytes long
        InvalidTag: if authentication fails
    """

    if not isinstance(cipher, AESGCMSIV) or not all(isinstance(x, bytes) for x in (nonce, data, aad)):
        raise TypeError("Wrong types for arguments")

    if len(nonce) != 12:
        raise ValueError("Nonce should be exactly 12 bytes long")

    return cipher.decrypt(nonce, data, aad)
