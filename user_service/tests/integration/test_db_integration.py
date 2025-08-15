import pytest
from sqlalchemy import create_engine, text
import os
from db import insert_user, db_connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://chatbot:secret@postgres:5432/chatbot_db")

@pytest.fixture(autouse=True)
def cleanup_users(db_connection):
    db_connection.execute(text("DELETE FROM users"))
    db_connection.commit()

def test_user_insert_and_query(db_connection):
    insert_user(db_connection, "Alice", "Smith", "alice123", "hash", "1995-05-05")

    result = db_connection.execute(text("SELECT username FROM users WHERE username='alice123'")).fetchone()
    assert result[0] == "alice123"
