"""
This module is responsible for connecting to the Weaviate database and pushing and querying documents.
"""
import weaviate, os
import weaviate.classes as wvc
from vectorizer import Vectorizer
from weaviate.classes.query import MetadataQuery

class VectorDb:
    """
    This class implements an abstraction of the Weaviate database client, which is used to push and query documents.
    """

    def __init__(self, collection):
        #All envvars can be passed via values.yaml when running on kubernetes
        host= os.getenv("WEAVIATE_HTTP_HOST", "weaviate.default.svc.cluster.local")
        port=os.getenv("WEAVIATE_HTTP_PORT", 80)
        host_grpc= os.getenv("WEAVIATE_GRPC_HOST", "weaviate-grpc.default.svc.cluster.local")
        port_grpc=os.getenv("WEAVIATE_GRPC_PORT", 50051)
        self.collection = collection

        self. client = weaviate.connect_to_custom(
            http_host=host,  # URL only, no http prefix
            http_port=port,
            http_secure=False,   # Set to True if https
            grpc_host=host_grpc,
            grpc_port=port_grpc,      # Default is 50051, WCD uses 443
            grpc_secure=False,   # Edit as needed
        )

        if self.client.is_ready():
            print("Weaviate is ready")
        else:
            raise Exception("Weaviate is not ready")
        
        self.vectorizer = Vectorizer()
    
    def is_ready(self):
        """
        Check if the Weaviate client is ready to accept requests.
        """
        return self.client.is_ready()
    
    def pushDocument(self, document):
        """
        Push a document to the Weaviate database along with its vector representation.
        """
        text = document["text"]
        embeddings = self.vectorizer.vectorize(text)
        self.client.collections.get(self.collection).data.insert(
            properties={
                "text": text,
            },
            vector=embeddings
        )
    
    def query(self, text):
        """
        Query the Weaviate database for documents similar to the given text.
        """
        embeddings = self.vectorizer.vectorize(text)
        try:
            response = self.client.collections.get(self.collection).query.near_vector(
                near_vector=embeddings,
                limit=1,
                return_metadata=MetadataQuery(distance=True)
            )
        except weaviate.exceptions.WeaviateQueryError:
            response = {"Error": "No documents found"}


        return response
       

    def __del__(self):
        """
        Close the Weaviate client connection when the object is deleted.
        """
        self.client.close()
        