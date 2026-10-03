import os

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignin(BaseModel):
    name: str
    email: EmailStr
    access_token: str
    expiration_time: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    token_type: str = "bearer"