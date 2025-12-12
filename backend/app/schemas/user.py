from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class UserCreate(UserLogin):
    name: str



class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str
