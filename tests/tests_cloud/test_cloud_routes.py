import os
import tempfile
import pytest
import base64
from pathlib import Path
from unittest.mock import MagicMock, patch

# --- 1. SETUP ENVIRONMENT BEFORE IMPORTING CLOUD ---
# We must create the certificate directory and set env vars
temp_dir_obj = tempfile.TemporaryDirectory()
cert_dir = Path(temp_dir_obj.name) / "certs"
db_dir = Path(temp_dir_obj.name) / "db"
os.makedirs(cert_dir, exist_ok=True)
os.makedirs(db_dir, exist_ok=True)

os.environ["CERTIFICATE_DIR"] = str(cert_dir)
os.environ["SIGNING_KEY_NAME"] = "signing.key"
os.environ["CERTIFICATE_NAME"] = "cert.pem"
os.environ["DB_DIR"] = str(db_dir)
os.environ["DB_NAME"] = "test.db"

# --- 2. IMPORTS ---
from cloud import app
import cloud


# --- 3. FIXTURES ---


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_persistence():
    with patch("cloud.routes.persistence") as mock:
        yield mock


@pytest.fixture
def mock_requests():
    with patch("cloud.routes.requests") as mock:
        yield mock


@pytest.fixture
def mock_crypto():
    with patch("cloud.routes.crypto") as mock:
        mock.decrypt.return_value = b'{"dummy": "data"}'
        mock.encrypt.return_value = b"encrypted_bytes"

        mock.verify_certificate.return_value = True
        mock.decode_certificate.return_value = "cert_obj"
        mock.load_certificate.return_value = "server_cert"
        mock.encode_certificate.return_value = b"server_cert_bytes"
        mock.load_signing_key.return_value = "skey"
        mock.sign.return_value = b"signature"
        mock.decode_ecdh_pkey.return_value = "client_pkey"
        mock.gen_ecdh_keys.return_value = ("skey", "pkey")
        mock.derive_shared_key.return_value = b"shared_key"
        mock.get_ciphers.return_value = ("enc_cipher", "dec_cipher")
        mock.encode_ecdh_pkey.return_value = b"server_pkey_bytes"
        yield mock


@pytest.fixture
def mock_cloud_state():
    """
    Replaces the Multiprocessing Manager dictionaries with standard Python dictionaries.
    This prevents 'PicklingError' when we try to store MagicMock objects
    (which cannot be pickled) inside the global CLIENTS/RESCUERS dicts.
    """
    original_clients = cloud.CLIENTS
    original_rescuers = cloud.RESCUERS

    cloud.CLIENTS = {}
    cloud.RESCUERS = {}

    yield

    cloud.CLIENTS = original_clients
    cloud.RESCUERS = original_rescuers


@pytest.fixture
def mock_emergency_model():
    """
    Mocks the Emergency class used in cloud.routes.
    This is critical because Emergency.unpack() will crash if we feed it
    the dummy bytes from mock_crypto.
    """
    with patch("cloud.routes.Emergency") as mock:
        mock_instance = MagicMock()
        mock_instance.emergency_id = 1
        mock_instance.user_uuid = "user-123"
        mock.unpack.return_value = mock_instance
        yield mock


# --- 4. TESTS ---


def test_user_save_success(client, mock_persistence):
    payload = {
        "uuid": "user-123",
        "is_rescuer": False,
        "name": "John",
        "surname": "Doe",
        "birthday": "1990-01-01",
        "blood_type": "APOS",
        "health_info_json": "{}",
    }
    response = client.post("/user/save/", json=payload)

    assert response.status_code == 200
    mock_persistence.save_user.assert_called_once()


def test_user_update_success(client, mock_persistence):
    payload = {
        "uuid": "user-123",
        "is_rescuer": False,
        "name": "Jane",
        "surname": "Doe",
        "birthday": "1990-01-01",
        "blood_type": "APOS",
        "health_info_json": '{"allergies": "peanuts"}',
    }
    response = client.post("/user/update/", json=payload)

    assert response.status_code == 200
    mock_persistence.update_user.assert_called_once()
    assert mock_persistence.update_user.call_args[0][0] == "user-123"


def test_user_delete_success(client, mock_persistence):
    payload = {"uuid": "user-123"}
    response = client.post("/user/delete/", json=payload)

    assert response.status_code == 200
    mock_persistence.delete_user.assert_called_once_with("user-123")


def test_emergency_submit_success(
    client, mock_persistence, mock_crypto, mock_cloud_state, mock_emergency_model
):
    """Tests submitting an emergency."""
    user_uuid = "user-123"

    mock_client_dto = MagicMock()
    mock_client_dto.dec_cipher = "mock_cipher"
    mock_client_dto.nonce = b"mock_nonce"
    cloud.CLIENTS[user_uuid] = mock_client_dto

    payload = {
        "emergency_id": 1,
        "user_uuid": user_uuid,
        "severity": 1,
        "blob": base64.b64encode(b"encrypted_data").decode("utf-8"),
        "routing_info_json": "{}",
    }
    response = client.post("/emergency/submit/", json=payload)

    assert response.status_code == 200
    mock_crypto.decrypt.assert_called()
    mock_emergency_model.unpack.assert_called()


def test_emergency_update_success(client, mock_persistence):
    payload = {
        "emergency_id": 1,
        "user_uuid": "user-123",
        "severity": 2,
        "blob": base64.b64encode(b"updated_encrypted_data").decode("utf-8"),
        "routing_info_json": "{}",
    }

    response = client.post("/emergency/update/", json=payload)

    assert response.status_code == 200
    mock_persistence.update_encrypted_emergency.assert_called_once()


def test_emergency_delete_success(client, mock_persistence):
    payload = {"emergency_id": 1, "user_uuid": "user-123"}

    response = client.post("/emergency/delete/", json=payload)

    assert response.status_code == 200
    mock_persistence.delete_encrypted_emergency.assert_called_once_with("user-123", 1)


def test_emergency_accept_success(
    client, mock_persistence, mock_crypto, mock_cloud_state, mock_requests
):
    """
    Tests the complex flow where a Rescuer accepts an emergency,
    and the server sends a notification back to the original Client.
    """
    client_uuid = "client-123"
    rescuer_uuid = "rescuer-456"
    client_ip = "192.168.1.50:5000"

    mock_client_dto = MagicMock()
    mock_client_dto.ip = client_ip
    mock_client_dto.cloud_nonce = b"c_nonce"

    mock_rescuer_dto = MagicMock()
    mock_rescuer_dto.dec_cipher = "r_cipher"
    mock_rescuer_dto.nonce = b"r_nonce"

    cloud.CLIENTS[client_uuid] = mock_client_dto
    cloud.RESCUERS[rescuer_uuid] = mock_rescuer_dto

    payload = {
        "uuid": rescuer_uuid,
        "emergency_id": 1,
        "user_uuid": client_uuid,
        "severity": 1,
        "blob": base64.b64encode(b"encrypted_for_rescuer").decode("utf-8"),
        "routing_info_json": "{}",
    }

    response = client.post("/emergency/accept/", json=payload)

    assert response.status_code == 200

    mock_requests.post.assert_called_once()
    assert mock_requests.post.call_args[0][0] == f"{client_ip}/notification/receive"

    mock_crypto.encrypt.assert_called()

