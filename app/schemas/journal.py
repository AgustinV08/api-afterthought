import os

from pydantic import BaseModel, EmailStr, Field, field_validator

class JournalCreate(BaseModel):
    content: str = Field(min_length=2)
