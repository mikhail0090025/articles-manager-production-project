from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import UserCreate, UserLogin, SearchQuery
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

@app.get("/search_page")
def search_page(request: Request):
    try:
        session_id = request.cookies.get("session_id")
        is_authenticated = requests.get("http://user_service:8000/authenticated", cookies=request.cookies)
        if is_authenticated.status_code == 401:
            return RedirectResponse(url="/login_page")
        
        user_data = requests.get("http://gateway_service:8003/users/me", cookies={"session_id": session_id})
        print("DEBUG: User data:", user_data.json())
        print("DEBUG: Session ID:", session_id)

        return templates.TemplateResponse("search.html", {"request": request, "user_data": user_data.json()})
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)
    except HTTPException as e:
        return JSONResponse(content={"error": "Internal server error", "details": str(e.detail)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"error": "Unexpected error", "details": str(e)}, status_code=500)

@app.post("/login_user")
def login_user(user: UserLogin):
    try:
        resp = requests.post("http://gateway_service:8003/login_user", json=user.model_dump())

        if resp.status_code == 200:
            session_id = resp.cookies.get("session_id")
            if session_id:
                print("DEBUG: session_id:", session_id)
                response = JSONResponse(content=resp.json(), status_code=resp.status_code)
                response.set_cookie(
                    key="session_id",
                    value=session_id,
                    httponly=True,
                    max_age=3600,
                    path="/"
                )
                return response
            else:
                print("DEBUG: didnt get cookie from gateway!")
                return JSONResponse(content={"error": "Session ID not found"}, status_code=500)

        if resp.status_code == 404:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        if resp.status_code == 401:
            return JSONResponse(content={"error": "Invalid password"}, status_code=401)
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)

@app.post("/search")
def search(query: SearchQuery, request: Request):
    try:
        session_id = request.cookies.get("session_id")
        if not session_id:
            return RedirectResponse(url="/login_page")
        response = requests.post("http://gateway_service:8003/search_articles", json=query.model_dump(), cookies={"session_id": session_id})
        print("DEBUG: Search response:", response.json())
        if response.status_code == 200:
            return JSONResponse(content=response.json(), status_code=200)
        else:
            return JSONResponse(content=response.json(), status_code=response.status_code)
    except requests.RequestException as e:
        return JSONResponse(content={"error": "Service unavailable", "details": str(e)}, status_code=503)