#!/bin/bash

#Script para parar nuestra app en local y eliminar nuestra aplicación junto con su backup desplegados en la nube de AWS

cd ../flask-pastebin

echo "-----STOP LOCAL APP-----"
docker-compose down
echo -e "\n"

echo "-----DELETE APP ELASTIC BEANSTALK-----"
eb terminate --all --force
echo -e "\n"

#el formato del bucket generado por elastic beanstalk es "elasticbeanstalk-$REGION-$ACCOUNT_ID"
REGION=eu-west-1
ACCOUNT_ID=$(aws sts get-caller-identity --output text --query 'Account')

echo "-----EMPTY S3 BUCKET EB-----"
aws s3 rm s3://elasticbeanstalk-$REGION-$ACCOUNT_ID --recursive --region $REGION
echo -e "\n"

echo "-----DELETE S3 BUCKET POLICY EB-----"
aws s3api delete-bucket-policy --bucket elasticbeanstalk-$REGION-$ACCOUNT_ID --region $REGION
echo -e "\n"

echo "-----DELETE S3 BUCKET EB-----"
aws s3api delete-bucket --bucket elasticbeanstalk-$REGION-$ACCOUNT_ID --region $REGION
echo -e "\n"

echo "-----TERRAFORM DESTROY BACKUP S3-----"
cd ../terraform && terraform destroy -auto-approve
echo -e "\n"