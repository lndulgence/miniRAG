microk8s ctr image rm localhost:32000/ragapi:latest > /dev/null
helm uninstall ragapi > /dev/null
docker build -t localhost:32000/ragapi .
docker push localhost:32000/ragapi
helm install ragapi helm/ --values helm/values.yaml