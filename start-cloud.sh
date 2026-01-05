#!/usr/bin/sh

source ./.env

mkdir -p $CERTIFICATE_DIR
mkdir -p $DB_DIR

docker volume create data
docker volume create certs

docker compose up --build cloud
