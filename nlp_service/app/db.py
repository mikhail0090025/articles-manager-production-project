import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json
import requests
import time

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://chatbot:secret@postgres:5432/chatbot_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def add_article(title, content, source_url=None, retries=3):
    embedding_response = None
    for attempt in range(retries):
        try:
            embedding_response = requests.post(
                "http://vector_service:8001/get_embedding",
                json={"text": content}
            )
            embedding_response.raise_for_status()
            break
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}/{retries} failed: {e}")
            time.sleep(3)
    if embedding_response is None:
        raise RuntimeError("Couldnt get embedding after all attempts")
    embedding = embedding_response.json().get("embedding")
    with SessionLocal() as session:
        sql = text("""
            INSERT INTO knowledge_base(title, content, embedding, source_url)
	        VALUES (:title, :content, :embedding, :source_url) ON CONFLICT (title) DO NOTHING;
        """)
        session.execute(sql, {
            "title": title,
            "content": content,
            "embedding": embedding,
            "source_url": source_url if source_url else "",
        })
        session.commit()

def add_all_articles():
    import os
    with open("articles.json", "r", encoding="utf-8") as articles_file:
        articles_data = json.load(articles_file)
    for article in articles_data:
        file_path = os.path.join("articles", article["file"])
        if not os.path.exists(file_path):
            print(f"Article file {file_path} does not exist, skipping.")
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        title = article.get("title", "Untitled")
        source_url = article.get("source_url", None)
        print(f"Adding article: {title}")
        add_article(title, content, source_url)