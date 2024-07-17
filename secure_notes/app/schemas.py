from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        orm_mode = True
class Token(BaseModel):
    token: str

class Note(BaseModel):
    note: str

