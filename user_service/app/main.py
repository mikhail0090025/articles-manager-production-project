from fastapi import FastAPI, Request
from db import insert_user, get_user, delete_user, db_connection_, get_all_users
import bcrypt
from fastapi.responses import JSONResponse
from models import UserCreate, UserLogin
import secrets

app = FastAPI()

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

@app.get("/users")
def get_all_users_endpoint():
    try:
        with db_connection_() as conn:
            users = get_all_users(conn)
        if not users:
            return JSONResponse(content={"error": "No users found"}, status_code=404)
        response = []
        for user in users:
            response.append({
                "name": user[0],
                "surname": user[1],
                "username": user[2],
                "born_date": str(user[3])
            })
        
        print("RESULT:", response, "TYPE:", type(response))
        return JSONResponse(content=response, status_code=200)
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

sessions = {}

@app.post("/login")
def login_user(user: UserLogin):
    print("DEBUG: User login request received:", user)
    try:
        with db_connection_() as conn:
            user_data = get_user(conn, user.username)
        
        print("DEBUG: User data retrieved:", user_data)
        print("DEBUG: user:", user)
        if not user_data:
            return JSONResponse(content={"error": "User not found"}, status_code=404)

        if bcrypt.checkpw(user.password.encode('utf-8'), user_data["password_hash"].encode('utf-8')):
            response = JSONResponse(content={"message": f"User {user.username} logged in successfully!"}, status_code=200)
            session_id = secrets.token_hex(16)
            sessions[session_id] = user_data["username"]
            print("DEBUG: Generated session ID:", session_id)
            print("DEBUG: Session data:", sessions)
            print("DEBUG: User data:", user_data)

            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=3600,
                path="/"
            )

            return response
        else:
            return JSONResponse(content={"error": "Invalid password"}, status_code=401)
    except Exception as e:
        print("Unexpected error while logging in user has occurred:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=503)

@app.get("/authenticated")
def get_authenticated_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        return JSONResponse(content={"authenticated": False}, status_code=401)
    return JSONResponse(content={"authenticated": True}, status_code=200)

@app.get("/me")
def get_current_user(request: Request):
    print("DEBUG: Current user request received")
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)

    username = sessions[session_id]
    with db_connection_() as conn:
        user = get_user(conn, username)
    
    print("DEBUG: Current user data:", user)
    print("DEBUG: Session ID:", session_id)
    print("DEBUG: Session data:", sessions)

    if not user:
        return JSONResponse(content={"error": "User not found"}, status_code=404)

    return JSONResponse(content={
        "name": user["name"],
        "surname": user["surname"],
        "username": user["username"]
    }, status_code=200)
