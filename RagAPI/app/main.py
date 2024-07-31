from prompter import prompterinstance as prompter
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome to the RAG API server!"}

@app.get('/health')
def health():
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post('/augment')
async def retrieve(request: Request):
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
    body = await request.json()
    try:
        prompter.vectordb.pushDocument(body)
    except KeyError:
        return {"Error": "Missing required fields in the JSON data"}
    return JSONResponse(content={"status": "Document added successfully"}, status_code=200)