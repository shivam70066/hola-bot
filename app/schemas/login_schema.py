from typing import Any
from pydantic import BaseModel

class LoginData(BaseModel):
    email: str
    password: str
    
class LoginResponse(BaseModel):
    message: str
    data: Any | None = None