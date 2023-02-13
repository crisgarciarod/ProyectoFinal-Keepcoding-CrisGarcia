#!/bin/bash

#Script para automatizar el almacenamiento del backup de la aplicación a AWS S3 mediante Terraform

cd ../terraform

echo "-----TERRAFORM INIT-----"
terraform init
echo -e "\n"

echo "-----TERRAFORM PLAN-----"
terraform plan
echo -e "\n"

echo "-----TERRAFORM APPLY-----"
terraform apply --auto-approve
echo -e "\n"

echo "-----CREATE ZIP FILE IN TGZ FORMAT-----"
tar -cvzf backup.tgz ../flask-pastebin/*
echo -e "Created tgz\n"

echo "-----UPLOAD BACKUP TO AWS S3-----"
NOMBRE_BUCKET=$(terraform output | grep -o "deadbycloud-.....")
aws s3 cp backup.tgz s3://$NOMBRE_BUCKET/
echo -e "\n"

echo "-----DELETE TGZ-----"
rm backup.tgz
echo -e "Deleted tgz file\n"