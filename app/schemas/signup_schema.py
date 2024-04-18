from typing import Any
from pydantic import BaseModel, field_validator, EmailStr

class SignUpData(BaseModel):
    name: str
    email: EmailStr
    password: str
    number: str
    
    @field_validator('name')
    @classmethod
    def isNameValid(cls, name: str) -> str:
        name = name.strip()
        if name is "":
            raise ValueError('Name cannot be empty.')
        if any(char.isdigit() for char in name):
            raise ValueError('Name cannot contain any number.')
        return name
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        min_length = 8
        if len(v) < min_length:
            raise ValueError(f"Password must be at least {min_length} characters long.")
        return v
    
    @field_validator('number')
    @classmethod
    def validate_phone_number(cls, v):
        if not v.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(v) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        return v
    
    
class SignUpResponse(BaseModel):
    message: str
    data: Any | None = None