from fastapi import APIRouter, FastAPI, File, UploadFile,Request, HTTPException
import os
import shutil
from app.utils import ingestion,egression
from ..services.user_data_services import UserDataServices


router = APIRouter(
    prefix="/user_data",
    tags=['User data']
)

@router.post("")
async def saveData(request: Request,file: UploadFile = File(...)):
    TEMP_DIR = ""
    temp_file_path = os.path.join(TEMP_DIR, file.filename)
    
    with open(temp_file_path, "wb") as temp:
        shutil.copyfileobj(file.file, temp)
    
    ids = ingestion.ingestData(temp_file_path)
    details = await UserDataServices.saveUserdata(file.filename,request.state.user_id,ids)
    
    print(details)
    os.remove(temp_file_path)
        
        
    return {"status": "Inserted successfully"}


@router.get("/sources")
async def getSources(request: Request):
    
    sources = await UserDataServices.getSources(request.state.user_id) 
    print(sources)
        
        
    return {"user_id":request.state.user_id,"sources":sources}


@router.delete("/delete")
async def getSources(request: Request,src_id:str):
    user_id = request.state.user_id
    # sources = await UserDataServices.getSources(request.state.user_id) 
    # print(sources)
    sourceChunksIDs = await UserDataServices.getSourceChunksIds(user_id,src_id)
    if sourceChunksIDs is None:
        raise HTTPException(status_code=404, detail="No Source data is associated with this id")
    egression.deleteData(sourceChunksIDs)
    
    isDeleted = await UserDataServices.deleteSource(src_id)
    
    if isDeleted is False:
        raise HTTPException(status_code=404, detail="No Source data is associated with this id")
    
    return {"detail": f'Source data is deleted with id: {src_id}'}
     