import datetime
import os

from flask import Flask
from multiprocessing import Manager
from common.services import emergency_queue, crypto
from pathlib import Path


app = Flask(__name__)


manager = Manager()
status_lock = manager.Lock()

# format UUID: ClientDTO
CLIENTS = manager.dict(dict())
# subset of CLIENTS
RESCUERS = manager.dict(dict())

manager.register(
    'get_queue',
    callable=emergency_queue.EmergencyQueue.get_instance,
    exposed=['push_emergency', 'pop_emergency', 'update_emergency']
)

# not subject to race conditions
SKEY_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("SIGNING_KEY_NAME", None))
CERTIFICATE_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("CERTIFICATE_NAME", None))

def init_certificate_and_skey():
    global SKEY_PATH, CERTIFICATE_PATH

    if not SKEY_PATH.exists() or not CERTIFICATE_PATH.exists():
        SKEY_PATH.touch()
        CERTIFICATE_PATH.touch()

        skey, certificate = crypto.gen_certificate("IT", "Salerno", "Salerno", "RescueCom S.r.l.")

        crypto.save_certificate(CERTIFICATE_PATH, certificate)
        crypto.save_edkey(SKEY_PATH, skey)

    else:

        certificate = crypto.load_certificate(CERTIFICATE_PATH)

        if certificate.not_valid_after_utc <= datetime.datetime.now(datetime.UTC):
            skey, certificate = crypto.gen_certificate("IT", "Salerno", "Salerno", "RescueCom S.r.l.")

            crypto.save_certificate(CERTIFICATE_PATH, certificate)
            crypto.save_edkey(SKEY_PATH, skey)


init_certificate_and_skey()
