from fastapi import FastAPI
from pydantic import BaseModel
from db import insert_user, get_user, db_connection_
import bcrypt

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    born_date: str

@app.get("/")
def root():
    return {"message": "User service is up!"}

@app.post("/users")
def create_user(user: UserCreate):
    try:
        with db_connection_() as conn:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            insert_user(
                conn,
                user.name,
                user.surname,
                user.username,
                hashed_password,
                user.born_date)
            return {"message": f"User {user.username} created!"}
    except Exception as e:
        print("Unexpected error while creating user has occured:", str(e))
        return {"error": str(e)}

@app.get("/users/{username}")
def read_user(username: str):
    try:
        with db_connection_() as conn:
            user = get_user(conn, username)
            if not user:
                return {"error": "User not found"}
            return {
                "username": user["username"],
                "name": user["name"],
                "surname": user["surname"],
                "born_date": user["born_date"]
            }
    except Exception as e:
        print("Unexpected error while reading user has occured:", str(e))
        return {"error": str(e)}
