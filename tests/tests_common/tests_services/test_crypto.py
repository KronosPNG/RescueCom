import pytest
import os

from tests import utils
from common.services import crypto
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey, EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


@pytest.fixture
def skey_cert_fixture() -> tuple[Ed25519PrivateKey, Certificate]:
    return crypto.gen_certificate('IT', 'Salerno', 'Fisciano', 'Luigi Turco', 30)

@pytest.fixture
def encoded_cert_fixture(skey_cert_fixture) -> bytes:
    return crypto.encode_certificate(skey_cert_fixture[1])

@pytest.fixture
def edkey_path_fixture(tmp_path) -> Path:
    path = tmp_path / 'skey'
    crypto.save_edkey(path, Ed25519PrivateKey.generate())
    return path

@pytest.fixture
def signature_fixture() -> tuple[bytes, bytes]:
    key = Ed25519PrivateKey.generate()
    nonce = os.urandom(12)
    return nonce, crypto.sign(key, nonce)

@pytest.fixture()
def ecdh_keys_fixture() -> tuple[EllipticCurvePrivateKey, EllipticCurvePublicKey]:
    return crypto.gen_ecdh_keys()

@pytest.fixture
def encoded_ecdh_pkey_fixture(ecdh_keys_fixture) -> bytes:
    return crypto.encode_ecdh_pkey(ecdh_keys_fixture[1])

@pytest.fixture
def cipher_fixture() -> AESGCMSIV:
    return AESGCMSIV(os.urandom(32))


def test_save_edkey(tmp_path):
    key = Ed25519PrivateKey.generate()
    crypto.save_edkey(tmp_path / 'key', key)

    utils.test_type_combs(crypto.save_edkey, 2, 0, [Path, Ed25519PrivateKey])

    with pytest.raises(Exception):
        crypto.save_edkey(tmp_path, key) # tmp_path is a directory

def test_encode_certificate(skey_cert_fixture):
    _, cert = skey_cert_fixture

    assert isinstance(crypto.encode_certificate(cert), bytes)

    utils.test_type_combs(crypto.encode_certificate, 1, 0, [Certificate])

def test_decode_certificate(encoded_cert_fixture):
    encoded_cert = encoded_cert_fixture

    assert isinstance(crypto.decode_certificate(encoded_cert), Certificate)

    utils.test_type_combs(crypto.decode_certificate, 1, 0, [bytes], no_correct=False)

    with pytest.raises(Exception):
        crypto.decode_certificate(b'')
        crypto.decode_certificate(encoded_cert + b'abc')

def test_load_signing_key(edkey_path_fixture):
    path = edkey_path_fixture

    assert isinstance(crypto.load_signing_key(path), Ed25519PrivateKey)

    utils.test_type_combs(crypto.load_signing_key, 1, 0, [Path])

    with pytest.raises(Exception):
        crypto.decode_certificate(path / 'abc')

def test_save_certificate(tmp_path, skey_cert_fixture):
    path = tmp_path / 'cert.pem'
    _, cert = skey_cert_fixture

    crypto.save_certificate(path, cert)

    utils.test_type_combs(crypto.save_certificate, 2, 0, [Path, Certificate])

    with pytest.raises(Exception):
        crypto.save_certificate(tmp_path, key) # tmp_path is a directory

def test_gen_certificate():
    working_args = ['IT', 'Salerno', 'Fisciano', 'Luigi Turco', 30]

    assert isinstance(crypto.gen_certificate(*working_args), tuple)
    assert len(crypto.gen_certificate(*working_args)) == 2
    assert isinstance(crypto.gen_certificate(*working_args)[0], Ed25519PrivateKey)
    assert isinstance(crypto.gen_certificate(*working_args)[1], Certificate)

    utils.test_type_combs(crypto.gen_certificate, 4, 1, [str, str, str, str, int], no_correct=True)

    with pytest.raises(ValueError):
        crypto.gen_certificate(*working_args[:-1], 0)
        crypto.gen_certificate(*working_args[:-1], 1)
        crypto.gen_certificate(*working_args[:-1], -1)
        crypto.gen_certificate('', *working_args[1:])
        crypto.gen_certificate('a', *working_args[1:])
        crypto.gen_certificate('aaa', *working_args[1:])

def test_sign():
    key = Ed25519PrivateKey.generate()
    nonce = os.urandom(12)

    assert isinstance(crypto.sign(key, nonce), bytes)

    utils.test_type_combs(crypto.gen_certificate, 2, 0, [Ed25519PrivateKey, bytes])

def test_decode_ecdh_pkey(encoded_ecdh_pkey_fixture):
    enc_pkey = encoded_ecdh_pkey_fixture

    assert isinstance(crypto.decode_ecdh_pkey(enc_pkey), EllipticCurvePublicKey)

    utils.test_type_combs(crypto.decode_ecdh_pkey, 1, 0, [bytes], no_correct=False)

    # I don't know how to generate the ValueError

def test_encode_ecdh_pkey(ecdh_keys_fixture):
    _, pkey = ecdh_keys_fixture

    assert isinstance(crypto.encode_ecdh_pkey(pkey), bytes)

    utils.test_type_combs(crypto.encode_ecdh_pkey, 1, 0, [EllipticCurvePublicKey])

def test_ecdh_keys():
    ret = crypto.gen_ecdh_keys()

    assert isinstance(ret, tuple)
    assert len(ret) == 2

    skey, pkey = ret

    assert isinstance(skey, EllipticCurvePrivateKey)
    assert isinstance(pkey, EllipticCurvePublicKey)

def test_derive_shared_key(ecdh_keys_fixture):
    skey, pkey = ecdh_keys_fixture

    peer_pkey = crypto.gen_ecdh_keys()[1] # can't be skey's public key

    derived = crypto.derive_shared_key(skey, peer_pkey)

    assert isinstance(derived, bytes)
    assert len(derived) == 32

    utils.test_type_combs(crypto.derive_shared_key, 2, 0, [EllipticCurvePrivateKey, EllipticCurvePublicKey])

    with pytest.raises(ValueError):
        crypto.derive_shared_key(skey, pkey)

def test_get_ciphers():
    key = os.urandom(32)

    ret = crypto.get_ciphers(key)

    assert isinstance(ret, tuple)
    assert len(ret) == 2

    ec, dc = ret

    assert isinstance(ec, AESGCMSIV)
    assert isinstance(dc, AESGCMSIV)

    with pytest.raises(ValueError):
        crypto.get_ciphers(b'')
        crypto.get_ciphers(b'\0')
        crypto.get_ciphers(b'\0'*31)
        crypto.get_ciphers(b'\0'*33)

def test_encrypt(cipher_fixture):
    cipher = cipher_fixture

    nonce = os.urandom(12)
    data = os.urandom(int.from_bytes(os.urandom(1)))
    aad = os.urandom(10)

    enc = crypto.encrypt(cipher, nonce, data, aad)

    assert isinstance(enc, bytes)

    utils.test_type_combs(crypto.encrypt, 4, 0, [AESGCMSIV, bytes, bytes, bytes])

    with pytest.raises(ValueError):
        crypto.encrypt(cipher, b'', data, aad)
        crypto.encrypt(cipher, b'\0', data, aad)
        crypto.encrypt(cipher, b'\0'*11, data, aad)
        crypto.encrypt(cipher, b'\0'*13, data, aad)

def test_decrypt(cipher_fixture):
    cipher = cipher_fixture

    nonce = os.urandom(12)
    data = os.urandom(int.from_bytes(os.urandom(1)))
    aad = os.urandom(10)

    ct = crypto.encrypt(cipher, nonce, data, aad)
    pt = crypto.decrypt(cipher, nonce, ct, aad)

    assert isinstance(ct, bytes)

    utils.test_type_combs(crypto.decrypt, 4, 0, [AESGCMSIV, bytes, bytes, bytes])

    with pytest.raises(InvalidTag):
        crypto.decrypt(cipher, nonce, data, aad)

    with pytest.raises(ValueError):
        crypto.decrypt(cipher, b'', ct, aad)
        crypto.decrypt(cipher, b'\0', ct, aad)
        crypto.decrypt(cipher, b'\0'*11, ct, aad)
        crypto.decrypt(cipher, b'\0'*13, data, aad)
