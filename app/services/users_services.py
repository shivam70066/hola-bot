from fastapi import HTTPException
from ..repository.user_repo import User_repo
from ..schemas.signup_schema import SignUpData

class UserService:
    
    @staticmethod 
    async def createUser(data:SignUpData):
            isExist = await User_repo.isUserExist(data.email)
            if isExist is not None:
                raise HTTPException(status_code=409, detail=f"User is already registerefered with email: {data.email}")
                
            return await User_repo.createUser(data)
