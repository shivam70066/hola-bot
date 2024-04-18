from fastapi import HTTPException
from ..schemas.signup_schema import SignUpData
from configs.database_connection import prisma_connection
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

class User_repo:
    @staticmethod
    async def createUser(user : SignUpData):
        return await prisma_connection.prisma.user.create({
            'name': user.name.capitalize(),
            'email': user.email.lower(),
            'phone_number': user.number,
            'password': hash_password(user.password)
        })
        
    @staticmethod
    async def isUserExist(email:str):
        return await prisma_connection.prisma.user.find_first(where={"email": email.lower()})
    
    @staticmethod
    async def getUsers():
        return await prisma_connection.prisma.user.find_many()
    
    
    
        

