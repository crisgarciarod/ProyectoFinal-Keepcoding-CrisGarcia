#!/bin/bash

echo "-----CREATE MINIKUBE-----"
minikube start --memory=4096 
echo -e "\n"

echo "-----INGRESS ADDONS-----"
minikube addons enable ingress
echo -e "\n"

echo "-----DELETE VALIDATING WEBHOOK CONFIGURATION-----"
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
echo -e "\n"

echo "-----DOCKER LOGIN-----"
docker login
echo -e "\n"

echo "-----CREATE NAMESPACE-----"
kubectl create namespace app-k8s
echo -e "\n"
kubectl create namespace monitoring
echo -e "\n"

echo "-----APPLICATION K8s-----"
kubectl -n app-k8s apply -f ingress.yaml
echo -e "\n"
kubectl -n app-k8s apply -f service.yaml
echo -e "\n"
kubectl set image -f deployment.yaml python=$DOCKERHUB_USER/deadbycloud:latest --local -o yaml | kubectl -n app-k8s apply -f -
echo -e "\n"
kubectl -n app-k8s apply -f clusterRole.yaml
echo -e "\n"

echo "-----PROMETHEUS K8s-----"
kubectl -n monitoring apply -f prometheus-configmap.yaml
echo -e "\n"
kubectl -n monitoring apply -f prometheus-deployment.yaml
echo -e "\n"
kubectl -n monitoring apply -f prometheus-service.yaml
echo -e "\n"

echo "-----ALERTMANAGER K8s-----"
kubectl -n monitoring apply -f alertmanager-configmap.yaml
echo -e "\n"
kubectl -n monitoring apply -f alertmanager-deployment.yaml
echo -e "\n"
kubectl -n monitoring apply -f alertmanager-service.yaml
echo -e "\n"


echo "-----GRAFANA K8s-----"
kubectl -n monitoring apply -f grafana-deployment.yaml
echo -e "\n"
kubectl -n monitoring apply -f grafana-service.yaml
echo -e "\n"