import os
import multiprocessing

# Server settings
bind = "0.0.0.0:8000"

# Worker settings
#workers = 2 * multiprocessing.cpu_count() + 1
workers = 1

# Logging
accesslog = os.getenv("LOGS_DIR") + "/access.log"
errorlog = os.getenv("LOGS_DIR") + "/error.log"
loglevel = "debug"
