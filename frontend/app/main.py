from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models import UserCreate, UserLogin
import requests

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/styles", StaticFiles(directory="templates/styles"), name="styles")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"message": "Frontend service is up!"}

@app.get("/registration_page")
def registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.post("/create_user")
def create_user(user: UserCreate):
    try:
        response = requests.post("http://gateway_service:8003/create_user", json=user.model_dump())
        if response.status_code == 200:
            return JSONResponse(content=response.json(), status_code=200)
        else:
            return JSONResponse(content=response.json(), status_code=response.status_code)
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)

@app.get("/login_page")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login_user")
def login_user(user: UserLogin):
    try:
        print(user)
        print(type(user))
        response = requests.post("http://gateway_service:8003/login_user", json=user.model_dump())
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)