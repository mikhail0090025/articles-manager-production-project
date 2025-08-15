from fastapi import FastAPI
from pydantic import BaseModel
from vector_utils import get_embedding
from db import search_vectors

app = FastAPI(title="Vector Search Service")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/search")
def search(req: SearchRequest):
    try:
        embedding = get_embedding(req.query)
        results = search_vectors(embedding, top_k=req.top_k)
        return {"query": req.query, "results": results}
    except Exception as e:
        print("Error during search:", str(e))
        return {"error": str(e)}