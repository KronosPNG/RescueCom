from clientDTO import ClientDTO
from flask import Flask


app = Flask(__name__)

# format UUID: ClientDTO
CLIENTS = {}
# subset of CLIENTS
RESCUERS = {}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
