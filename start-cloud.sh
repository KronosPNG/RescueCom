#!/usr/bin/sh

if [ ! -f ./.env ]; then
	echo -e "Create a .env file setting these variables:\nCERTIFICATE_DIR\nDB_DIR\nLOGS_DIR"
	exit
fi

source ./.env

docker volume create data
docker volume create certs
docker volume create logs

docker compose up --build cloud
