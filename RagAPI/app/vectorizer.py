import os
from dns import check_dns_resolution
import requests

class Vectorizer:
    def __init__(self):
        
        address = os.getenv("LLAMA_HTTP_HOST", "local-llama.default.svc.cluster.local")
        port = os.getenv("LLAMA_HTTP_PORT", "8000")
        self.url = f"http://{address}:{port}/embeddings"
        check_dns_resolution(address)


    def vectorize(self, text):
        data = {
            "text": text
        }
        response = requests.post(self.url, json=data, timeout=None)
        return response.json()["embeddings"]