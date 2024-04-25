from typing import List
from fastapi import APIRouter, FastAPI, File, Form, UploadFile,Request, HTTPException
import os
import shutil
from app.utils import ingestion,egression
from ..services.user_data_services import UserDataServices

router = APIRouter(
    prefix="/data",
    tags=['User data']
)

@router.post("/ingest")
async def ingestData(request: Request,
                     files: List[UploadFile] = File([]),
                     urls: List[str] = Form([])):
    
    
    if len(files) == 0 and len(urls)==0:
        raise HTTPException(status_code=404, detail="please send at least one file or url")
    
    TEMP_DIR = ""
    inserted_files = []
    for file in files:
            if file.filename != '':
                temp_file_path = os.path.join(TEMP_DIR, file.filename)
                    
                with open(temp_file_path, "wb") as temp:
                    shutil.copyfileobj(file.file, temp)
                    
                ids = ingestion.ingestData(temp_file_path, request.state.user_id)
                details = await UserDataServices.saveUserdata(file.filename, request.state.user_id, ids)
                inserted_files.append(file.filename)
                os.remove(temp_file_path)
    
    inserted_urls = []
    for url in urls:
        if url != '':
            ids = ingestion.ingestData(url, request.state.user_id)
            details = await UserDataServices.saveUserdata(url, request.state.user_id, ids)
            inserted_urls.append(url)
        
    
        
    return {"status": "Inserted successfully", "inserted_files": inserted_files , "inserted_urls": inserted_urls}


@router.get("/sources")
async def getSources(request: Request):
    
    sources = await UserDataServices.getSources(request.state.user_id) 
        
    return {"user_id":request.state.user_id,"sources":sources}


@router.delete("/delete")
async def getSources(request: Request,src_id:str):
    user_id = request.state.user_id
    # sources = await UserDataServices.getSources(request.state.user_id)
    # print(sources)
    sourceChunksIDs = await UserDataServices.getSourceChunksIds(user_id,src_id)
    if sourceChunksIDs is None:
        raise HTTPException(status_code=404, detail="No Source data is associated with this id")
    egression.deleteData(sourceChunksIDs,user_id)
    
    isDeleted = await UserDataServices.deleteSource(src_id)
    
    if isDeleted is False:
        raise HTTPException(status_code=404, detail="No Source data is associated with this id")
    
    return {"detail": f'Source data is deleted with id: {src_id}'}
     