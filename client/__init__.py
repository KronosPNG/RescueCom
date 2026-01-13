import os
import threading
import requests
import uuid
import datetime
import time
import sys
import signal

from common.services import crypto
from common.models import db, user
from pathlib import Path
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from flask import Flask
from threading import Thread, Lock
from dotenv import load_dotenv
from common.models.emergency import Emergency
from offline.service import BLEService
from offline.payload import Payload

load_dotenv(Path(__file__).parent / ".env")

UUID: Optional[str] = None
IS_RESCUER: Optional[bool] = None
DEC_CIPHER: Optional[AESGCMSIV] = None
ENC_CIPHER: Optional[AESGCMSIV] = None
NONCE: Optional[bytes] = None
CLOUD_NONCE: Optional[bytes] = None
USER: Optional[user.User] = None

DATA_PATH = Path(os.getenv("DATA_FILE"))
SKEY_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(
    os.getenv("SIGNING_KEY_NAME", None)
)
CERTIFICATE_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(
    os.getenv("CERTIFICATE_NAME", None)
)

ble_service = BLEService(
    os.getenv("BLE_LOCALNAME", None), os.getenv("BLE_TARGET", None)
)

db.DatabaseManager.get_instance(
    Path(os.getenv("DB_DIR", None)) / Path(os.getenv("DB_NAME", None))
)

CONNECTED: bool = False

mutex = Lock()


def shutdown_handler(sig, frame):
    ble_service.stop()
    sys.exit(0)


def init_info():
    global UUID, IS_RESCUER

    if not DATA_PATH.exists():
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.touch()

        with DATA_PATH.open("w") as f:
            UUID = str(uuid.uuid4())

            f.write(UUID)
    else:
        with DATA_PATH.open() as f:
            UUID = f.readline().strip()
            IS_RESCUER = f.readline().strip() != "0"


def init_certificate_and_skey():
    global SKEY_PATH, CERTIFICATE_PATH

    if not SKEY_PATH.exists() or not CERTIFICATE_PATH.exists():
        SKEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        SKEY_PATH.touch()
        CERTIFICATE_PATH.touch()

        skey, certificate = crypto.gen_certificate(
            "IT", "Salerno", "Fisciano", "Luigi Turco"
        )

        crypto.save_certificate(CERTIFICATE_PATH, certificate)
        crypto.save_edkey(SKEY_PATH, skey)

    else:
        certificate = crypto.load_certificate(CERTIFICATE_PATH)

        if certificate.not_valid_after_utc <= datetime.datetime.now(datetime.UTC):
            skey, certificate = crypto.gen_certificate(
                "IT", "Salerno", "Fisciano", "Luigi Turco"
            )

            crypto.save_certificate(CERTIFICATE_PATH, certificate)
            crypto.save_edkey(SKEY_PATH, skey)


def check_connection():
    global CONNECTED

    while True:
        connected = False

        for _ in range(3):  # max 3 attempts
            try:
                r = requests.get("http://localhost:8000/health/", timeout=5)

                if r.status_code == 200:
                    connected = True
                    break
            except requests.RequestException:
                pass  # server not reachable

            time.sleep(5)

        with mutex:
            CONNECTED = connected

        time.sleep(60)


def receive_bluetooth_payload():
    ble_service.start()
    while True:
        payload: bytes | None = ble_service.receive_payload_nowait()
        if payload:
            # DB stuff
            p: Payload = Payload.unpack_data(payload)
            em: Emergency = Emergency(
                emergency_id=p.emergency_id,
                user_uuid=p.user_uuid,
                severity=p.severity,
                position=p.position,
                emergency_type="Unknow",
                description="Emergency from Blutooth",
                created_at=datetime.datetime.now(),
            )
            dbm = db.DatabaseManager.get_instance()
            try:
                dbm.insert_emergency(em)
            except Exception as e:
                print(e)
        time.sleep(0.5)


def switch_to_bluetooth():
    ble_thread: Thread | None = None
    while True:
        with mutex:
            connected = CONNECTED

        if not connected:
            if ble_thread is None or not ble_thread.is_alive():
                ble_thread = threading.Thread(
                    target=receive_bluetooth_payload, daemon=True
                )
                ble_thread.start()

        time.sleep(2)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
init_info()
init_certificate_and_skey()

check_connection_thread: Thread = threading.Thread(target=check_connection, daemon=True)
check_connection_thread.start()
switch_to_bluetooth_thread: Thread = threading.Thread(
    target=switch_to_bluetooth, daemon=True
)
switch_to_bluetooth_thread.start()

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = None

from client import routes
