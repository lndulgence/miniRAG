"""
Vectorizer class to vectorize the text using the llama service
"""
import os
from dns import check_dns_resolution
import requests

class Vectorizer:
    """
    This class abstracts the vectorization of text using the llama service.
    """
    def __init__(self):
        
        #All envvars can be passed via values.yaml when running on kubernetes
        address = os.getenv("LLAMA_HTTP_HOST", "local-llama.default.svc.cluster.local")
        port = os.getenv("LLAMA_HTTP_PORT", "8000")
        self.url = f"http://{address}:{port}/embeddings"
        check_dns_resolution(address)


    def vectorize(self, text):
        """
        Vectorize the given text using the llama service.
        """
        data = {
            "text": text
        }
        response = requests.post(self.url, json=data, timeout=None)
        return response.json()["embeddings"]