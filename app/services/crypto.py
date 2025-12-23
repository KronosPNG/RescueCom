from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from cryptography.hazmat.primitives.asymmetric import ec, EllipticCurvePrivateKey, EllipticCurvePublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


ECDH_CURVE = ec.SECP256R1()


def gen_ecdh_keys(encoded: bool = True) -> (EllipticCurvePrivateKey, EllipticCurvePublicKey):
    """
    Generate private and corresponding public ECDH keys

    Args:
        encoded (bool): whether to encode the public key (default True)
    Returns:
        A pair of ECDH keys, private and corresponding public
    """

    skey = ec.generate_private_key(ECDH_CURVE)
    pkey = skey.public_key()

    return skey, (pkey.public_bytes(Encoding.X962, PublicFormat.CompressedPoint) if encoded else pkey)

def derive_shared_key(skey: EllipticCurvePrivateKey, pkey: EllipticCurvePublicKey, encoded: bool = True) -> bytes:
    """
    Derive a shared key after a succesful ECDH key exchange

    Args:
        skey (EllipticCurvePrivateKey): own private ECDH key
        pkey (EllipticCurvePublicKey): received public ECDH key
        encoded (bool): whether the public key is encoded (default True)
    Returns:
        The derived key
    Raises:
        TypeError: if the keys aren't of the correct types
        ValueError: if the public key is the given private key's public key
    """

    if not isinstance(skey, EllipticCurvePrivateKey) or not isinstance(pkey, EllipticCurvePublicKey):
        raise TypeError("Private and public keys are of the wrong type")

    pkey = EllipticCurvePublicKey.from_encoded_point(ECDH_CURVE, pkey) if encoded else pkey

    if skey.public_key() == pkey:
        raise ValueError("Public key must not derive from given private key")

    shared_key = skey.exchange(ec.ECDH(), pkey)

    return HKDF(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = None,
            info = None
            ).derive(shared_key)

def get_ciphers(key: bytes) -> (AESGCMSIV, AESGCMSIV):
    """
    Generate two AESGCMSIV ciphers for encryption and decryption

    Args:
        key (bytes): the shared key
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
        TypeError: if any argument if of the wrong type
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
        TypeError: if any argument if of the wrong type
        ValueError: if the nonce isn't exactly 12 bytes long
        cryptography.exception.InvalidTag: if authentication fails
    """

    if not isinstance(cipher, AESGCMSIV) or not all(isinstance(x, bytes) for x in (nonce, data, aad)):
        raise TypeError("Wrong types for arguments")

    if len(nonce) != 12:
        raise ValueError("Nonce should be exactly 12 bytes long")

    return cipher.decrypt(nonce, data, aad)
