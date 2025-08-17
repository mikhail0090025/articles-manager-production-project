from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    born_date: str

class UserLogin(BaseModel):
    username: str
    password: str