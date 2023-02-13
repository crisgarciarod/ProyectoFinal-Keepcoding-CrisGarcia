#!/bin/bash

#Script para ejecutar todos los scripts

echo "-----DOCKER-----"
./autodeploy_docker.sh
echo -e "\n"

echo "-----TERRAFORM-S3-----"
./autodeploy_backup_s3.sh
echo -e "\n"

echo "-----AWS-----"
./autodeploy_aws_app.sh
echo -e "\n"
