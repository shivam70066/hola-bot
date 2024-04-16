from typing import Any
from pydantic import BaseModel

class SignUpData(BaseModel):
    name: str
    email: str
    password: str
    number: str
    
    
    
class SignUpResponse(BaseModel):
    message: str
    data: Any | None = None