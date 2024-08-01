microk8s ctr image rm localhost:32000/mainapi:latest > /dev/null
helm uninstall mainapi > /dev/null
docker build -t localhost:32000/mainapi .
docker push localhost:32000/mainapi
helm install mainapi helm/ --values helm/values.yaml