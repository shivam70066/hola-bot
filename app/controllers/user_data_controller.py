from fastapi import APIRouter, FastAPI, File, UploadFile
from app.schemas.login_schema import LoginData, LoginResponse
from ..services.users_services import UserService
from ..schemas.signup_schema import SignUpData,SignUpResponse
import pdfplumber
import tempfile
import os
import shutil


router = APIRouter(
    prefix="/user_data",
    tags=['User data']
)

@router.post("")
async def signup(file: UploadFile = File(...)):
    # file_extension = file.filename.split(".")[-1]
    file_extension = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(dir="",delete=False, suffix=file_extension) as temp:
        temp_file_path = file.filename
        

        # Save the uploaded file to the temporary file
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # if file.filename.endswith(".pdf"):
    #     with pdfplumber.open(file.file) as pdf:
            
    #         contents = ""
    #         for page in pdf.pages:
    #             contents += page.extract_text()

    #     print(contents)
    # else:
    #     # Read file contents as bytes
    #     contents = await file.read()
    #     print(contents.decode('utf-8'))
    
    os.remove(temp_file_path)
        
        
    return {"filename": file.filename, "temp_file_path": temp_file_path}



     