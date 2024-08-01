"""
This file contains the FastAPI server that serves as the API for the RAG service.
"""
from prompter import prompterinstance as prompter
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request

app = FastAPI()

@app.get('/')
def root():
    """
    Root endpoint for the FastAPI server.
    Prints a welcome message.
    """
    return {"message": "Welcome to the RAG API server!"}

@app.get('/health')
def health():
    """
    Health endpoint for the FastAPI server.
    Returns a JSON response with the status of the server.
    This endpoint is used for kubernetes health checks.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post('/augment')
async def retrieve(request: Request):
    """
    This endpoint receives a JSON request containing a user message and a system message.
    The user message is used to query the vector database to retrieve relevant documents.
    The system message is augmented with the retrieved documents and returned in the response.
    """
    body = await request.json()
    try:
        objects = prompter.augment_prompt(body).objects
        print(objects)
        documents = [i.properties["text"] for i in objects]
    except KeyError:
        return {"Error": "Missing required fields in the JSON data"}
    
    for i in documents:
        body["system_message"] += f"\n\n#SOURCE#\n{i}" 
    
    return body
@app.post('/addDocument')
async def add_document(request: Request):
    """
    This endpoint receives a JSON request containing a document.
    The document is added to the vector database, along with its vector representation (sequence embedding).
    """
    body = await request.json()
    try:
        prompter.vectordb.pushDocument(body)
    except KeyError:
        return {"Error": "Missing required fields in the JSON data"}
    return JSONResponse(content={"status": "Document added successfully"}, status_code=200)