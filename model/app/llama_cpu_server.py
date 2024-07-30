from fastapi import FastAPI, Request
from llama_cpp import Llama
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

global model
global embedder

model = None
embedder = None

@app.on_event("startup")
async def startup_event():
    global model
    global embedder
    model_path = "./model.gguf"
    model = Llama(model_path=model_path)
    embedder = Llama(model_path=model_path, embedding=True)
    print("Model loaded successfully")

@app.get('/')
def root():
    return {"message": "Welcome to the Llama CPU server"}

@app.post('/chat')
async def generate_response(request: Request):
    
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
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post("/embeddings")
async def get_embeddings(request: Request):
    global embedder
    
    try:
        data = await request.json()

        # Check if the required fields are present in the JSON data
        if 'text' in data:
            text = data['text']

            # Get the embeddings        
            print("Creating embeddings")
            embeddings = embedder.create_embedding(text)
            resp = {
                "embeddings": embeddings
            }
            return JSONResponse(content=jsonable_encoder(resp), status_code=200)

        else:
            return JSONResponse(content={"Error": "Missing required fields in the JSON data"}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)

