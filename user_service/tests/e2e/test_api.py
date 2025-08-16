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
    print(resp.json())
    print(type(resp.json()))
    assert resp.status_code == 200
    assert resp.json()["message"] == "User bobb created!"

def test_get_user():
    resp = requests.get(f"{BASE_URL}/users/bobb")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Bob"

def test_delete_user():
    resp = requests.delete(f"{BASE_URL}/users/bobb")
    assert resp.status_code == 200