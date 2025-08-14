import requests

BASE_URL = "http://localhost:8000"

def test_create_user():
    payload = {
        "name": "Bob",
        "surname": "Brown",
        "username": "bobb",
        "password": "securepassword",
        "born_date": "1990-07-01"
    }
    resp = requests.post(f"{BASE_URL}/users", json=payload)
    assert resp.status_code == 201
    assert resp.json()["username"] == "bobb"

def test_get_user():
    resp = requests.get(f"{BASE_URL}/users/bobb")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Bob"
