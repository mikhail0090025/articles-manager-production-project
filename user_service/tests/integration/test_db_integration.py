import pytest
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://chatbot:secret@postgres:5432/chatbot_db"

@pytest.fixture
def db():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    yield conn
    conn.close()

def test_user_insert_and_query(db):
    db.execute(
        text(
            "INSERT INTO users (name, surname, username, password_hash, born_date) VALUES (:n, :s, :u, :p, :b)"
        ),
        {"n": "Alice", "s": "Smith", "u": "alice123", "p": "hash", "b": "1995-05-05"}
    )

    result = db.execute(text("SELECT username FROM users WHERE username='alice123'")).fetchone()
    assert result[0] == "alice123"
