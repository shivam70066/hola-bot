from fastapi import HTTPException
from app.schemas.login_schema import LoginData
from ..repository.user_repo import User_repo
from ..repository import user_repo
from ..schemas.signup_schema import SignUpData
from configs.settings import settings
from datetime import datetime, timedelta
import jwt

class UserService:
    
    @staticmethod 
    async def createUser(data:SignUpData):
            isExist = await User_repo.isUserExist(data.email)
            if isExist is not None:
                raise HTTPException(status_code=409, detail=f"User is already registerefered with email: {data.email}")
                
            return await User_repo.createUser(data)
        
    @staticmethod
    async def checkCredentials(data:LoginData):
        userData = await User_repo.isUserExist(data.email)
        
        if userData is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        isPasswordcorrect= user_repo.verify_password(data.password,userData.password)
        
        if isPasswordcorrect:
            payload = {
                "data": {"id" : userData.id,
                        "email": userData.email,
                        "name" : userData.name},
                "exp": datetime.utcnow() + timedelta(days=3)
            }
            
            
            token = jwt.encode(payload, settings.JWT_SECRET_KEY , algorithm="HS256")
            
    #         try:
    # # Decode the JWT token
    #             token = jwt.decode("eyJhbGcpbC5jb20iLCJuYW1lIjoiSGFyc2gifSwiZXhwIjoxNzEzMzQ3MTc3fQ.Gks6aua7A76ZF0_wQvR7B9NsbAoMkomBhZ7kT12ztRU", settings.JWT_SECRET_KEY, algorithms=["HS256"])
    #             print("Token decoded successfully:", token)
    #         except jwt.ExpiredSignatureError:
    # # Handle token expiration
    #             print("Token has expired")
    #         except jwt.InvalidTokenError:
    # # Handle invalid token
    #             print("Invalid token")
            return token
        
        else: 
            raise HTTPException(status_code=401, detail="Invalid Credentials")
        
    @staticmethod
    async def getAllUsers():
        users = await User_repo.getUsers()
        if users is None:
            raise HTTPException(status_code=404, detail="No data Found")
        
        return users
        

    
        
        
