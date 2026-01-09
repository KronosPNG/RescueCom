#!/usr/bin/sh

if [ ! -f ./.env ]; then
	echo -e "Create a .env file setting these variables:\nCERTIFICATE_DIR\nDB_DIR"
	exit
fi

source ./.env

mkdir -p $CERTIFICATE_DIR
mkdir -p $DB_DIR

docker volume create data
docker volume create certs

docker compose up --build cloud
