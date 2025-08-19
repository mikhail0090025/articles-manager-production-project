import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://chatbot:secret@postgres:5432/chatbot_db")

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
            "embedding": json.dumps(query_embedding.tolist()),
            "limit": top_k
        }).fetchall()
        return [dict(row._mapping) for row in rows]

def add_query_to_history(query, username):
    sql_query = text("""
        INSERT INTO messages (text, user_id)
        VALUES (:msg, (
            SELECT id FROM users WHERE username = :username
        ))
        RETURNING id;
    """)
    with SessionLocal() as session:
        result = session.execute(sql_query, {"msg": query, "username": username})
        session.commit()

def get_history(username=None):
    sql_query = text("""
        SELECT messages.id AS message_id,
            messages.text,
            messages.created_at,
            messages.user_id,
            users.username
        FROM messages
        JOIN users ON messages.user_id = users.id
        WHERE (:username IS NULL OR users.username = :username)
        ORDER BY messages.created_at DESC;
    """)
    with SessionLocal() as session:
        result = session.execute(sql_query, {"username": username})
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows] if rows else []