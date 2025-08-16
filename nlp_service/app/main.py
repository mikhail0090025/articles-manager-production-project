from fastapi import FastAPI
from pydantic import BaseModel
from db import add_article, add_all_articles, engine, SessionLocal
from sqlalchemy import text

add_all_articles()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "User service is up!"}

@app.get("/articles")
def get_articles():
    with SessionLocal() as session:
        sql = text("SELECT id, title, embedding, created_at FROM knowledge_base;")
        result = session.execute(sql)
        rows = result.fetchall()

    articles = [dict(row._mapping) for row in rows]
    return articles
