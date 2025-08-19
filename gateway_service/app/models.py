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

class Article(BaseModel):
    title: str
    content: str
    source_url: str | None = None

class SearchQuery(BaseModel):
    query: str