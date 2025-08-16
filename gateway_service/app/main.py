from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Gateway Service")

user_service_url = os.getenv("USER_SERVICE_URL", "http://user_service:8000")
vector_service_url = os.getenv("VECTOR_SERVICE_URL", "http://vector_service:8001")
nlp_service_url = os.getenv("NLP_SERVICE_URL", "http://nlp_service:8002")

class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    born_date: str

class UserLogin(BaseModel):
    username: str
    password: str

class Article(BaseModel):
    title: str
    content: str
    source_url: str | None = None

def service_request(method, url, **kwargs):
    try:
        resp = requests.request(method, url, timeout=10, **kwargs)
        resp.raise_for_status()
        return resp.json(), resp.status_code
    except requests.HTTPError as e:
        return {"error": "HTTP error", "details": str(e)}, resp.status_code
    except requests.RequestException as e:
        return {"error": "Service unavailable", "details": str(e)}, status.HTTP_503_SERVICE_UNAVAILABLE

@app.post("/create_user")
def create_user(user: UserCreate, response: Response):
    json_data, status_code = service_request("POST", f"{user_service_url}/users", json=user.model_dump())
    response.status_code = status_code
    return json_data

@app.post("/login_user")
def login_user(user: UserLogin, response: Response):
    json_data, status_code = service_request("POST", f"{user_service_url}/login", json=user.model_dump())
    response.status_code = status_code
    return json_data

@app.post("/add_article")
def add_article(article: Article, response: Response):
    json_data, status_code = service_request("POST", f"{nlp_service_url}/articles", json=article.model_dump())
    response.status_code = status_code
    return json_data

@app.get("/articles")
def get_articles(response: Response):
    json_data, status_code = service_request("GET", f"{nlp_service_url}/articles")
    response.status_code = status_code
    return json_data

@app.get("/search_articles")
def search_articles(query: str, response: Response):
    json_data, status_code = service_request("GET", f"{nlp_service_url}/search", params={"query": query})
    response.status_code = status_code
    return json_data

@app.get("/")
def root():
    return {"message": "Gateway service is up!"}