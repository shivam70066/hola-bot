from fastapi import APIRouter, Path
from ..services.users_services import UserService
from ..schemas.signup_schema import SignUpData,SignUpResponse

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.post("/signup",response_model=SignUpResponse,response_model_exclude_none=True)
async def signup(userData: SignUpData):
    data = await UserService.createUser(userData)
    return SignUpResponse(message="Successfully Created.")