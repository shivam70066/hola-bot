from ..schemas.signup_schema import SignUpData
from configs.database_connection import prisma_connection

class User_repo:
    @staticmethod
    async def createUser(user : SignUpData):
        return await prisma_connection.prisma.user.create({
            'name': user.name.capitalize(),
            'email': user.email.lower(),
            'phone_number': user.number,
            'password':user.password
        })
        
    @staticmethod
    async def isUserExist(email:str):
        return await prisma_connection.prisma.user.find_first(where={"email": email.lower()})
    
    
        

