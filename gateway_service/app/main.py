from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
from models import UserCreate, UserLogin, Article

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
    json_data, status_code = service_request("POST", f"{user_service_url}/login", json=user.model_dump())
    return JSONResponse(content=json_data, status_code=status_code)

@app.post("/add_article")
def add_article(article: Article):
    json_data, status_code = service_request("POST", f"{nlp_service_url}/articles", json=article.model_dump())
    return JSONResponse(content=json_data, status_code=status_code)

@app.get("/articles")
def get_articles():
    json_data, status_code = service_request("GET", f"{nlp_service_url}/articles")
    return JSONResponse(content=json_data, status_code=status_code)

@app.get("/search_articles")
def search_articles(query: str):
    json_data, status_code = service_request("GET", f"{nlp_service_url}/search", params={"query": query})
    return JSONResponse(content=json_data, status_code=status_code)

@app.get("/")
def root():
    return {"message": "Gateway service is up!"}
