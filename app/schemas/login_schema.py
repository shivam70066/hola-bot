from typing import Any
from pydantic import BaseModel,EmailStr, field_validator

class LoginData(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if v is '':
            raise ValueError("Password can't be empty")
        return v
    
class LoginResponse(BaseModel):
    message: str
    token: Any | None = None