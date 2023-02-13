#!/bin/bash

#Script para automatizar el proceso de despliegue de la aplicación en AWS

cd ../flask-pastebin

echo "-----DELETE UNNECESSARY FILES-----"
rm -rf .elasticbeanstalk/ .gitignore
echo -e "Deleted files\n"

echo "-----CREATE APP-----"
eb init -p python-3.8 flask-pastebin --region eu-west-1
echo -e "\n"

echo "-----CREATE ENVIRONMENT-----"
eb create flask-env
echo -e "\n"

