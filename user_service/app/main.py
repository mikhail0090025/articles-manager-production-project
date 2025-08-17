from fastapi import FastAPI
from pydantic import BaseModel
from db import insert_user, get_user, delete_user, db_connection_
import bcrypt
from fastapi.responses import JSONResponse

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    born_date: str

class UserLogin(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return JSONResponse(content={"message": "User service is up!"}, status_code=200)

@app.post("/users")
def create_user(user: UserCreate):
    try:
        with db_connection_() as conn:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            insert_user(conn, user.name, user.surname, user.username, hashed_password, user.born_date)
            return JSONResponse(content={"message": f"User {user.username} created!"}, status_code=201)
    except Exception as e:
        print("Unexpected error while creating user has occurred:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=503)

@app.get("/users/{username}")
def read_user(username: str):
    try:
        with db_connection_() as conn:
            user = get_user(conn, username)
        if not user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        return JSONResponse(content={
            "username": user["username"],
            "name": user["name"],
            "surname": user["surname"],
            "born_date": user["born_date"]
        }, status_code=200)
    except Exception as e:
        print("Unexpected error while reading user has occurred:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=503)

@app.delete("/users/{username}")
def delete_user_endpoint(username: str):
    try:
        with db_connection_() as conn:
            delete_user(conn, username)
        return JSONResponse(content={
            "message": f"User {username} was deleted!"
        }, status_code=200)
    except Exception as e:
        print("Unexpected error while deleting user has occurred:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=503)

@app.post("/login")
def login_user(user: UserLogin):
    try:
        with db_connection_() as conn:
            user_data = get_user(conn, user.username)
        if not user_data:
            return JSONResponse(content={"error": "User not found"}, status_code=404)

        if bcrypt.checkpw(user.password.encode('utf-8'), user_data["password"].encode('utf-8')):
            return JSONResponse(content={"message": f"User {user.username} logged in successfully!"}, status_code=200)
        else:
            return JSONResponse(content={"error": "Invalid password"}, status_code=401)
    except Exception as e:
        print("Unexpected error while logging in user has occurred:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=503)
