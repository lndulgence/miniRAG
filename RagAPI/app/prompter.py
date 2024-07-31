from dns import check_dns_resolution
import os
import requests
from vectorDb import VectorDb



class Promtper:
    def __init__(self):
        address = os.getenv("MODEL_HTTP_HOST", "local-llama.default.svc.cluster.local")
        port = os.getenv("MODEL_HTTP_PORT", "8000")
        collection = os.getenv("CASE_COLLECTION", "docs")
        self.url = f"http://{address}:{port}/chat"
        check_dns_resolution(address)

        self.vectordb = VectorDb(collection)

    def augment_prompt(self, prompt):
        query = prompt["user_message"]  
        response = self.vectordb.query(query)
        return response
    
    def send_prompt(self, prompt):
        response = requests.post(self.url, json=prompt)
        return response.json()

prompterinstance = Promtper()