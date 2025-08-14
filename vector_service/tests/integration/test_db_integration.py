import pytest
from vector_service.vector_utils import get_embedding
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://chatbot:secret@postgres:5432/chatbot_db"

@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    yield conn
    conn.close()

def test_embedding_saved_to_db(db):
    text = "Test integration"
    emb = get_embedding(text)
    
    db.execute(text("INSERT INTO knowledge_base (title, content, embedding) VALUES (:t, :c, :e)"),
               {"t": "Test", "c": text, "e": emb})
    
    result = db.execute(text("SELECT content FROM knowledge_base WHERE title='Test'")).fetchone()
    assert result[0] == text
