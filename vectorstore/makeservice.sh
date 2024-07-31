helm upgrade --install \
  "weaviate" \
  weaviate/weaviate \
  --namespace "default" \
  --values ./values.yaml