"""
Lightweight implementation of a LLaMa server using FastAPI. 
Uses a lightweight version of the LLaMa model to generate responses to user queries and create embeddings for text.
The server exposes two endpoints: /chat and /embeddings. The /chat endpoint generates a response to a user query based on a system message and user message. 
The /embeddings endpoint creates embeddings for a given text. The server is designed to be used with the RAG API service to augment system messages with relevant documents.
Additionally, the server provides a health endpoint for Kubernetes health checks.
"""
from fastapi import FastAPI, Request
from llama_cpp import Llama, LLAMA_POOLING_TYPE_MEAN
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

global model
global embedder

model = None
embedder = None

@app.on_event("startup")
async def startup_event():
    """
    On Server startup, load the LLaMa model and the LLaMa embedder.
    """
    global model
    global embedder
    model_path = "./model.gguf"
    model = Llama(model_path=model_path)
    # Using the LLaMa embedder with pooling type MEAN. Pooling is necessary for creating sequence embeddings (as opposed to token embeddings).
    # The pooling type MEAN averages the embeddings of all tokens in the sequence to create a single sequence embedding. 
    # This is the pooling type that has been found experimentally to work best for most use cases.
    # If using a dedicated embedding model, other pooling types should be tried to find the best one for the specific use case.
    embedder = Llama(model_path=model_path, embedding=True, pooling_type=LLAMA_POOLING_TYPE_MEAN)
    print("Model loaded successfully")

@app.get('/')
def root():
    """
    Root endpoint for the FastAPI server. Returns a welcome message.
    """
    return {"message": "Welcome to the Llama CPU server"}

@app.post('/chat')
async def generate_response(request: Request):
    """
    This endpoint receives a JSON request containing a system message, a user message, and the maximum number of tokens to generate.
    The system message is used as the context for the model, and the user message is used as the prompt.
    The model generates a response to the prompt and returns it in the response.
    """
    try:
        data = await request.json()

        # Check if the required fields are present in the JSON data
        if 'system_message' in data and 'user_message' in data and 'max_tokens' in data:
            system_message = data['system_message']
            user_message = data['user_message']
            max_tokens = int(data['max_tokens'])

            # Prompt creation
            prompt = f"""<s>[INST] <<SYS>>
            {system_message}
            <</SYS>>
            {user_message} [/INST]"""

            # Run the model
            print("Running the model")
            output = model(prompt, max_tokens=max_tokens, echo=True)
            
            return JSONResponse(content=jsonable_encoder(output), status_code=200)

        else:
            return JSONResponse(content={"Error": "Missing required fields in the JSON data"}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)
    
@app.get('/health')
def health():
    """
    Health endpoint for kubernetes health checks. Returns a JSON response with the status of the server.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post("/embeddings")
async def get_embeddings(request: Request):
    """
    This endpoint receives a JSON request containing a text field.
    The text field is used to create embeddings using the LLaMa embedder.
    The embeddings are returned in the response.
    """
    global embedder
    
    try:
        data = await request.json()

        # Check if the required fields are present in the JSON data
        if 'text' in data:
            text = data['text']

            print("Text: ", text)
            # Get the embeddings        
            print("Creating embeddings")
            embedder.embed
            embeddings = jsonable_encoder(embedder.create_embedding(text))["data"][0]["embedding"]

            resp = {
                "embeddings": embeddings
            }

            print("Embeddings created")

            return JSONResponse(content=jsonable_encoder(resp), status_code=200)

        else:
            return JSONResponse(content={"Error": "Missing required fields in the JSON data"}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)

