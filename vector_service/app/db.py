import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def search_vectors(query_embedding, top_k=5):
    with SessionLocal() as session:
        sql = text("""
            SELECT id, title, content, source_url, created_at,
                   1 - (embedding <=> :embedding) AS similarity
            FROM knowledge_base
            ORDER BY embedding <-> :embedding
            LIMIT :limit
        """)
        rows = session.execute(sql, {
            "embedding": query_embedding,
            "limit": top_k
        }).fetchall()
        return [dict(row._mapping) for row in rows]
