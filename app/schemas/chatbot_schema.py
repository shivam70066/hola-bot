from typing import Any
from pydantic import BaseModel,EmailStr, field_validator

class ChatData(BaseModel):
    question : str
    chat_id : str | None = None