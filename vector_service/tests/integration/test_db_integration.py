import pytest
from vector_utils import get_embedding
from sqlalchemy import create_engine, text
import json
from db import DATABASE_URL

@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    yield conn
    conn.close()

def test_embedding_saved_to_db(db):
    test_text = "Test integration"
    emb = json.dumps(get_embedding(test_text).tolist())
    
    db.execute(text("INSERT INTO knowledge_base (title, content, embedding) VALUES (:t, :c, :e)"),
               {"t": "Test", "c": test_text, "e": emb})
    
    result = db.execute(text("SELECT content FROM knowledge_base WHERE title='Test'")).fetchone()
    assert result[0] == test_text
