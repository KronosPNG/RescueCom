#!/usr/bin/sh

mkdir -p "${CERTIFICATE_DIR}"

chown -R 1000:1000 "${CERTIFICATE_DIR}" || true
#chmod 700 "${CERTIFICATE_DIR}" || true

exec gosu appuser:appgroup "$@"
