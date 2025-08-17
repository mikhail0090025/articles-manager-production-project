from fastapi import FastAPI
from pydantic import BaseModel
from db import add_article, add_all_articles, engine, SessionLocal
from sqlalchemy import text
from typing import Optional
from fastapi.responses import JSONResponse

add_all_articles()

app = FastAPI()

class Article(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None

@app.get("/")
def root():
    return {"message": "NLP service is up!"}

@app.get("/articles")
def get_articles():
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