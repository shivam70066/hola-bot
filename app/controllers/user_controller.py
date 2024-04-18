from fastapi import APIRouter
from ..services.users_services import UserService
from ..schemas.globalresponses import GetAllUsersResponse

router = APIRouter(
    tags=['users']
)

@router.post("/users",response_model=GetAllUsersResponse,response_model_exclude_none=True)
async def getUsers():
    users = await UserService.getAllUsers()
        
    return GetAllUsersResponse(data=users)
