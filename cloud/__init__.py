from flask import Flask


app = Flask(__name__)

# format UUID: ClientDTO
CLIENTS = {}
# subset of CLIENTS
RESCUERS = {}

from . import routes
