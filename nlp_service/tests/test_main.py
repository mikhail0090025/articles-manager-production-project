import pytest
from fastapi.testclient import TestClient
from main import app, add_article, SessionLocal
from sqlalchemy import text
import numpy as np

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "User service is up!"}

def test_get_articles():
    test_title = "Test Article"
    test_content = "This is a test content."
    test_source_url = "http://example.com"

    add_article(test_title, test_content, test_source_url)

    response = client.get("/articles")
    assert response.status_code == 200
    data = response.json()

    titles = [article["title"] for article in data]
    assert test_title in titles

def test_articles_structure():
    response = client.get("/articles")
    data = response.json()

    if data:
        article = data[0]
        assert "id" in article
        assert "title" in article
        assert "embedding" in article
        assert "created_at" in article

def test_create_article():
    new_article = {
        "title": "New Test Article",
        "content": "This is the content of the new test article.",
        "embedding": np.random.randn(386).tolist(),
        "source_url": "http://example.com/new-test-article"
    }
    response = client.post("/articles", json=new_article)
    assert response.status_code == 200
    print("RESPONSE:", response.json())
    assert response.json() == {"message": "Article 'New Test Article' added successfully!"}