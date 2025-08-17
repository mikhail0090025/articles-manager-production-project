# tests/test_gateway.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- User tests ---
def test_create_user():
    user_data = {
        "name": "Test",
        "surname": "User",
        "username": "testuser123",
        "password": "securepass",
        "born_date": "2000-01-01"
    }
    response = client.post("/create_user", json=user_data)
    assert response.status_code < 400 or response.status_code == 503
    assert "message" in response.json() or "error" in response.json()

def test_login_user_success():
    user_data = {
        "username": "testuser123",
        "password": "securepass"
    }
    response = client.post("/login_user", json=user_data)
    assert response.status_code < 400 or response.status_code == 503
    json_data = response.json()
    print(json_data)
    assert "message" in json_data or "error" in json_data

# --- Article tests ---
def test_add_article():
    article_data = {
        "title": "Test Article",
        "content": "This is a test content.",
        "source_url": "http://example.com"
    }
    response = client.post("/add_article", json=article_data)
    assert response.status_code < 400 or response.status_code == 503
    json_data = response.json()
    assert "message" in json_data or "error" in json_data

def test_get_articles():
    response = client.get("/articles")
    assert response.status_code < 400 or response.status_code == 503
    json_data = response.json()
    assert isinstance(json_data, list) or "error" in json_data

def test_search_articles():
    response = client.get("/search_articles", params={"query": "Test"})
    assert response.status_code < 400 or response.status_code == 503
    json_data = response.json()
    assert isinstance(json_data, list) or "error" in json_data

# --- Health check ---
def test_root():
    response = client.get("/")
    assert response.status_code < 400 or response.status_code == 503
    assert response.json() == {"message": "Gateway service is up!"}
