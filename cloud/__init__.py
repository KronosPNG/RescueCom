import logging
import datetime
import os

from flask import Flask
from flask.logging import default_handler
from common.services import emergency_queue, crypto
from common.models import db
from pathlib import Path


app = Flask(__name__)

# format UUID: ClientDTO
CLIENTS = dict()
# subset of CLIENTS
RESCUERS = dict()

db.DatabaseManager.get_instance(Path(os.getenv("DB_DIR", None)) / Path(os.getenv("DB_NAME", None)))

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

gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.removeHandler(default_handler)
app.logger.addHandler(gunicorn_logger)
app.logger.setLevel(gunicorn_logger.level)

from . import routes
