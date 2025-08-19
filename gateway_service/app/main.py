from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
from models import UserCreate, UserLogin, Article, SearchQuery

load_dotenv()

app = FastAPI(title="Gateway Service")

user_service_url = os.getenv("USER_SERVICE_URL", "http://user_service:8000")
vector_service_url = os.getenv("VECTOR_SERVICE_URL", "http://vector_service:8001")
nlp_service_url = os.getenv("NLP_SERVICE_URL", "http://nlp_service:8002")

def service_request(method: str, url: str, **kwargs):
    try:
        resp = requests.request(method, url, timeout=10, **kwargs)
        resp.raise_for_status()
        return resp.json(), resp.status_code
    except requests.HTTPError as e:
        return {"error": "HTTP error", "details": str(e)}, resp.status_code
    except requests.RequestException as e:
        return {"error": "Service unavailable", "details": str(e)}, 503

@app.post("/create_user")
def create_user(user: UserCreate):
    json_data, status_code = service_request("POST", f"{user_service_url}/users", json=user.model_dump())
    return JSONResponse(content=json_data, status_code=status_code)

@app.post("/login_user")
def login_user(user: UserLogin):
    print("DEBUG: User login request received:", user)
    resp = requests.post(f"{user_service_url}/login", json=user.model_dump())

    response = JSONResponse(content=resp.json(), status_code=resp.status_code)

    if "set-cookie" in resp.headers:
        cookies = resp.headers.get("set-cookie")
        import re
        match = re.search(r"session_id=([^;]+)", cookies)
        if match:
            session_id = match.group(1)
            print("DEBUG: session_id:", session_id)
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=3600,
                path="/"
            )

    return response

@app.post("/add_article")
def add_article(article: Article):
    json_data, status_code = service_request("POST", f"{nlp_service_url}/articles", json=article.model_dump())
    return JSONResponse(content=json_data, status_code=status_code)

@app.get("/articles")
def get_articles():
    json_data, status_code = service_request("GET", f"{nlp_service_url}/articles")
    return JSONResponse(content=json_data, status_code=status_code)

@app.get("/search_articles")
def search_articles(query: SearchQuery):
    json_data, status_code = service_request("POST", f"{vector_service_url}/search", json=query.model_dump())
    return JSONResponse(content=json_data, status_code=status_code)

@app.post("/search_articles")
def search_articles_post(query: SearchQuery, request: Request):
    try:
        json_data, status_code = service_request("POST", f"{vector_service_url}/search", json=query.model_dump())
        return JSONResponse(content=json_data, status_code=status_code)
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)
    except Exception as e:
        return JSONResponse(content={"error": "Unexpected error", "details": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "Gateway service is up!"}

@app.get("/users/me")
def get_current_user(request: Request):
    try:
        resp = requests.get(
            f"{user_service_url}/me",
            cookies={"session_id": request.cookies.get("session_id")}
        )
        print("DEBUG: User data:", resp.json())
        print("DEBUG: Session ID:", request.cookies.get("session_id"))
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)

@app.get("/get_user")
def get_user(username: str):
    try:
        resp = requests.get(f"{user_service_url}/users/{username}")
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)