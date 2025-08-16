from sqlalchemy import create_engine, text
import os
from contextlib import contextmanager
import pytest

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://chatbot:secret@postgres:5432/chatbot_db")

@pytest.fixture
def db_connection():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    yield conn
    conn.close()

@contextmanager
def db_connection_():
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()

def insert_user(db, name, surname, username, password_hash, born_date):
    db.execute(
        text(
            "INSERT INTO users (name, surname, username, password_hash, born_date) "
            "VALUES (:n, :s, :u, :p, :b)"
        ),
        {"n": name, "s": surname, "u": username, "p": password_hash, "b": born_date}
    )
    db.commit()

def get_user(db, username):
    result = db.execute(
        text("SELECT name, surname, username, born_date FROM users WHERE username=:u"),
        {"u": username}
    ).fetchone()
    if result:
        return {
            "name": result[0],
            "surname": result[1],
            "username": result[2],
            "born_date": str(result[3])
        }
    return None

def delete_user(db, username):
    db.execute(
        text("DELETE FROM users WHERE username=:u"),
        {"u": username}
    )
    db.commit()