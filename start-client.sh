#!/usr/bin/sh

source ./client/.env


rm -f ${DATA_FILE}

mkdir -p ${CERTIFICATE_DIR}
mkdir -p ${DB_DIR}
touch ${DB_DIR}/${DB_NAME}

gunicorn --bind 0.0.0.0:$1 client:app
