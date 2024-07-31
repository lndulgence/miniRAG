microk8s ctr image rm localhost:32000/local-llama:latest > /dev/null
helm uninstall local-llama > /dev/null
docker build -t localhost:32000/local-llama .
docker push localhost:32000/local-llama
helm install local-llama helm/ --values helm/values.yaml
