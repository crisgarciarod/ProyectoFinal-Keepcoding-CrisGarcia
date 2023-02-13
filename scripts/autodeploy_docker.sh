#!/bin/bash

#Script para automatizar el proceso de creacion de la aplicación mediante Docker

#VARIABLE DE ENTORNO
DOCKERHUB_USER=$DOCKERHUB_USER

cd ../flask-pastebin

echo "-----CREATE IMAGE-----"
docker build -t $DOCKERHUB_USER/deadbycloud:latest .
echo -e "\n"

echo "-----DOCKER LOGIN-----"
docker login
echo -e "\n"

echo "-----PUSH IMAGE-----"
docker push $DOCKERHUB_USER/deadbycloud:latest
echo -e "\n"

echo "-----RUN APP-----"
docker-compose up -d
echo -e "\n"
