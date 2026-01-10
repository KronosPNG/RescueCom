#!/usr/bin/sh

mkdir -p "${CERTIFICATE_DIR}"
mkdir -p "${DB_DIR}"

chown -R 1000:1000 "${CERTIFICATE_DIR}"
chown -R 1000:1000 "${DB_DIR}"

exec gosu appuser:appgroup gunicorn --bind 0.0.0.0:8000 cloud:app
