import os
import requests
import uuid
import datetime

from common.services import crypto
from pathlib import Path
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from flask import Flask
from dotenv import load_dotenv

load_dotenv(__file__[:__file__.rfind('/')] + '/.env')

UUID: Optional[str] = None
DEC_CIPHER: Optional[AESGCMSIV] = None
ENC_CIPHER: Optional[AESGCMSIV] = None
NONCE: Optional[bytes] = None
CLOUD_NONCE: Optional[bytes] = None

DATA_PATH = Path(os.getenv("DATA_FILE"))
SKEY_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("SIGNING_KEY_NAME", None))
CERTIFICATE_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("CERTIFICATE_NAME", None))

def init_info():
    if not DATA_PATH.exists():
        DATA_PATH.touch()

        with DATA_PATH.open('w') as f:
            f.write(f'uuid = {str(uuid.uuid4())}')
    else:
        with DATA_PATH.open() as f:
            line = f.readline().strip()
            UUID = line[line.index('=')+2:]

def init_certificate_and_skey():
    if not SKEY_PATH.exists():
        SKEY_PATH.touch()

        skey, certificate = crypto.gen_certificate("IT", "Salerno", "Fisciano", "Luigi Turco")

        crypto.save_certificate(CERTIFICATE_PATH, certificate)
        crypto.save_edkey(SKEY_PATH, skey)

    else:
        certificate = crypto.load_certificate(CERTIFICATE_PATH)

        if certificate.not_valid_after_utc <= datetime.datetime.now(datetime.UTC):
            skey, certificate = crypto.gen_certificate("IT", "Salerno", "Fisciano", "Luigi Turco")

            crypto.save_certificate(CERTIFICATE_PATH, certificate)
            crypto.save_edkey(SKEY_PATH, skey)


init_info()
init_certificate_and_skey()

app = Flask(__name__)

from client import routes
