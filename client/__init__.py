import os
import requests

from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from flask import Flask


DEC_CIPHER: Optional[AESGCMSIV] = None
ENC_CIPHER: Optional[AESGCMSIV] = None
NONCE: Optional[bytes] = None
CLOUD_NONCE: Optional[bytes] = None

app = Flask(__name__)

from . import network, routes
