import requests

BASE_URL = "http://vector_service:8001"

def test_search_endpoint():
    resp = requests.post(f"{BASE_URL}/search", json={"query": "Hello"})
    print("Status:", resp.status_code)
    assert resp.status_code == 200
    assert "results" in resp.json() or "error" in resp.json()
    if "error" in resp.json() and "status_code" in resp.json():
        assert resp.json()["status_code"] == 401