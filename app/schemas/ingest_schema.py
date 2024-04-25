from typing import Any
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, FastAPI, File, Form, UploadFile,Request, HTTPException

class Ingest(BaseModel):
    files: List[UploadFile] | None = File(...),
    urls: Any | None = None
    
    