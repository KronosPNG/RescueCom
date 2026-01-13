import os
import threading
import requests
import uuid
import datetime
import time

from common.services import crypto
from common.models import db, user
from pathlib import Path
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from flask import Flask
from threading import Thread, Lock
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

UUID: Optional[str] = None
IS_RESCUER: Optional[bool] = None
DEC_CIPHER: Optional[AESGCMSIV] = None
ENC_CIPHER: Optional[AESGCMSIV] = None
NONCE: Optional[bytes] = None
CLOUD_NONCE: Optional[bytes] = None
USER: Optional[user.User] = None
ACCEPTED_GDPR: Optional[bool] = None

DATA_PATH = Path(os.getenv("DATA_FILE"))
SKEY_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(
    os.getenv("SIGNING_KEY_NAME", None)
)
CERTIFICATE_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(
    os.getenv("CERTIFICATE_NAME", None)
)

db.DatabaseManager.get_instance(Path(os.getenv("DB_DIR", None)) / Path(os.getenv("DB_NAME", None)))

CONNECTED: bool = False

mutex = Lock()


def init_info():
    global UUID, IS_RESCUER, ACCEPTED_GDPR

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
            ACCEPTED_GDPR = f.readline().strip() != "0"


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


init_info()
init_certificate_and_skey()

check_connection_thread: Thread = threading.Thread(target=check_connection, daemon=True)
check_connection_thread.start()

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = None

from client import routes
