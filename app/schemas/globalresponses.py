from typing import Any
from pydantic import BaseModel

  
class GetAllUsersResponse(BaseModel):
    data: Any | None = None