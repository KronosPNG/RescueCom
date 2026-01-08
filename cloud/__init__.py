from flask import Flask
from multiprocessing import Manager
from common.services import emergency_queue


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

from . import routes
