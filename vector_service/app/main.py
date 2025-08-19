from fastapi import FastAPI
from pydantic import BaseModel
from vector_utils import get_embedding
from db import search_vectors

app = FastAPI(title="Vector Search Service")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 2

class EmbeddingRequest(BaseModel):
    text: str

@app.post("/search")
def search(req: SearchRequest):
    try:
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