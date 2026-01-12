#!/usr/bin/sh

mkdir -p "${CERTIFICATE_DIR}"
mkdir -p "${DB_DIR}"
mkdir -p "${LOGS_DIR}"

chown -R 1000:1000 "${CERTIFICATE_DIR}"
chown -R 1000:1000 "${DB_DIR}"
chown -R 1000:1000 "${LOGS_DIR}"

exec gosu appuser:appgroup gunicorn -c gunicorn_config.py cloud:app
