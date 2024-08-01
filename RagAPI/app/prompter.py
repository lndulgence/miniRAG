"""
This module mostly interacts with the vector database to retrieve relevant documents for augmentation.
It can also send the prompt to the Rag model for further processing.
"""
from dns import check_dns_resolution
import os
import requests
from vectorDb import VectorDb



class Promtper:
    """
    This class is responsible for augmenting the prompt with relevant documents and sending the prompt to the model.
    """
    def __init__(self):
        # All envvars can be passed via values.yaml when running on kubernetes
        address = os.getenv("MODEL_HTTP_HOST", "local-llama.default.svc.cluster.local")
        port = os.getenv("MODEL_HTTP_PORT", "8000")

        # Different instances of the RagAPI can be used to serve different collections
        # With this architecture, only one model needs to be deployed to serve multiple collections, reducing resource usage.
        # By abstracting the model behind an API, we can easily scale the system horizontally by deploying multiple instances of the API, which can be used interchangeably.
        collection = os.getenv("CASE_COLLECTION", "docs")
        self.url = f"http://{address}:{port}/chat"
        check_dns_resolution(address)

        self.vectordb = VectorDb(collection)

    def augment_prompt(self, prompt):
        """
        Augment the system message with relevant documents and return the augmented prompt.
        """
        query = prompt["user_message"]  
        response = self.vectordb.query(query)
        return response
    
    def send_prompt(self, prompt):
        """
        Send the prompt to the model and return the response.
        """
        response = requests.post(self.url, json=prompt)
        return response.json()

prompterinstance = Promtper()