# MiniRAG

MiniRAG is a personal project intended to represent the minimal infrastructure for a **cloud based RAG deployment**. It contains all basic capabilities for RAG, including local model deployment, both for embedding and text generation. These models, along with a vector store and some ad-hoc microservices are used to performed semantic search as a function of user query, prompt enrichment, and the final text generation.  It is important to take into account that, due to development environment limitations, further considerations for full-scale deployment, such as horizontal scaling, have not  been taken into account. This code is meant to serve as basic scaffolding to build upon when deploying full-scale applications.

## Technologies
This project is based entirely on Open Source technologies, including [Docker](https://www.docker.com/), [microk8s](microk8s.io) (**Kubernetes**) , [LLaMa](https://llama.meta.com/), and [Weaviate](weaviate.io). The project is written entirely in Python and Go. Due to Kubernetes usage, the project is completely platform agnostic, and can be deployed in any cluster by any cloud provider.

## Installation

In order to execute MiniRAG, an existing installation of [microk8s](microk8s.io) with an enabled image registry, along with  [Docker](https://www.docker.com/). With these properly configured, deploying should be a simple matter, merely executing the Deployment.sh script. Some commands may have changed across microk8s versions, so YMMV. Due to github limitations, you will need to download the LLaMa model yourself, and put it in the model/models folder. You may obtain such models [here](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main)

## Usage

All services are developed on a kubernetes cluster, though from an user standpoint, only 2 need to be used: the RAG API /addDocument endpoint, to add documents to the vector db, along with their embeddings, and the mainAPI, to actually use the chatbot.

Running kubectl get svc will give you the IP addresses for both, and in order to use each:

POST ragAPI_IP:8000/addDocument where the request body contains a "text" field, with the document to be added.
POST mainAPI_IP :8080/chat where the request body contains a "message" field with a message for the chatbot.

If this is being deployed in a cloud environment, an ingress should be defined for both endpoints (such as Kong or nginx) in order to make them accessible from the outside.

## Additional considerations

MiniRAG was meant as a personal project to further my own understanding of how LLM-based applications are deployed in cloud-based environments. At its current state, *it is more of a toy than a serious candidate for cloud deployment*. In order to improve the project towards a potential production environment, several points need to be addressed, such as the usage of a dedicated embedding model, which would possibly perform better at RAG than the current reused llama, and the addition of GPU bindings to improve response time (it is, as of now, VERY SLOW, even using models on the lighter side, whose perdformance is somewhat hindered by their minimal-ness). Additionally, due to memory constraints, previous conversation logs are not stored in context, though this would be vital when deploying a chatbot.

Finally, since the internal python APIs are mostly called by other parts of the system, I have focused on keeping them lightweight, limiting schema validation to only the go API. However, this is not optional in a production environment.

### TODO
>With more memory, in an actual cloud environment, migration to Langchain probably offers more functionality (like conversation logs)

>Maybe a frontend? Feel free to PR

