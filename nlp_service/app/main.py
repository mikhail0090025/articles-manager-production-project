from fastapi import FastAPI
from pydantic import BaseModel
from db import add_article, add_all_articles, engine, SessionLocal, safe_add_all_articles
from sqlalchemy import text
from typing import Optional
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global articles_initialized
    articles_initialized = False
    print("Service is starting up...")
    yield
    print("Service is shutting down...")

articles_initialized = False
app = FastAPI(lifespan=lifespan)

class Article(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None

'''
@app.on_event("startup")
async def startup_event():
    global articles_initialized
    articles_initialized = False
'''

@app.get("/")
def root():
    return {"message": "NLP service is up!"}

@app.get("/articles")
def get_articles():
    global articles_initialized
    if not articles_initialized:
        print("DEBUG: Initializing articles from JSON file...")
        import time
        time1 = time.time()
        safe_add_all_articles()
        print("Time for loading articles: ", time.time() - time1, "s")
        articles_initialized = True
        print("DEBUG: Articles initialized from JSON file.")
    with SessionLocal() as session:
        sql = text("SELECT id, title, embedding, created_at FROM knowledge_base;")
        result = session.execute(sql)
        rows = result.fetchall()

    articles = [dict(row._mapping) for row in rows]
    return articles

@app.post("/articles")
def create_article(article: Article):
    try:
        add_article(article.title, article.content, article.source_url)
        return {"message": f"Article '{article.title}' added successfully!"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
def health():
    return {"status": "ok"}
