from fastapi import FastAPI, Request
from pydantic import BaseModel
from vector_utils import get_embedding
from db import search_vectors, add_query_to_history, get_history
import requests
app = FastAPI(title="Vector Search Service")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 2

class EmbeddingRequest(BaseModel):
    text: str

@app.post("/search")
def search(req: SearchRequest, request: Request):
    try:
        session_id = request.cookies.get("session_id")
        is_authenticated = requests.get(
            "http://user_service:8000/authenticated",
            cookies={"session_id": session_id}
        )
        if is_authenticated.status_code != 200:
            return {"error": "Unauthorized", "status_code": 401}
        
        user_service_response = requests.get(
            "http://user_service:8000/me",
            cookies={"session_id": session_id}
        )
        if user_service_response.status_code != 200:
            return {"error": "Failed to retrieve user data", "status_code": user_service_response.status_code}
        user_data = user_service_response.json()
        print("DEBUG: User data:", user_data)
        print("DEBUG: Session ID:", session_id)
        add_query_to_history(req.query, user_data["username"])
        embedding = get_embedding(req.query)
        results = search_vectors(embedding, top_k=req.top_k)
        result = {"query": req.query, "results": results}
        return result
    except Exception as e:
        print("Error during search:", str(e))
        return {"error": str(e)}

@app.post("/get_embedding")
def get_embedding_endpoint(req: EmbeddingRequest):
    try:
        embedding = get_embedding(req.text)
        return {"embedding": embedding.tolist()}
    except Exception as e:
        print("Error during creating embedding:", str(e))
        return {"error": str(e)}

@app.get("/history")
def get_search_history(request: Request):
    try:
        session_id = request.cookies.get("session_id")
        is_authenticated = requests.get(
            "http://user_service:8000/authenticated",
            cookies={"session_id": session_id}
        )
        if is_authenticated.status_code != 200:
            return {"error": "Unauthorized", "status_code": 401}
        user_service_response = requests.get(
            "http://user_service:8000/me",
            cookies={"session_id": session_id}
        )
        if user_service_response.status_code != 200:
            return {"error": "Failed to retrieve user data", "status_code": user_service_response.status_code}
        user_data = user_service_response.json()
        print("DEBUG: User data:", user_data)
        print("DEBUG: Session ID:", session_id)
        history = get_history(user_data["username"])
        return {"history": history}
    except Exception as e:
        print("Error during retrieving search history:", str(e))
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"}