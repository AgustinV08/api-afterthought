import os

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserLogin(BaseModel):
    email: str
    password: str

class UserSignin(BaseModel):
    name: str
    email: EmailStr
    access_token: str
    expiration_time: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    token_type: str = "bearer"