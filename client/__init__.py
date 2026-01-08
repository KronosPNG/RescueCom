import os
import requests

from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from flask import Flask
from client import network


DEC_CIPHER: Optional[AESGCMSIV] = None
ENC_CIPHER: Optional[AESGCMSIV] = None
NONCE: Optional[bytes] = None
CLOUD_NONCE: Optional[bytes] = None


app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1337)
