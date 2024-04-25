from fastapi import HTTPException
from app.schemas.login_schema import LoginData
from ..repository.user_repo import User_repo
from ..repository import user_repo
from ..schemas.signup_schema import SignUpData
from configs.settings import settings
from configs.database_connection import prisma_connection
from langchain_core.messages import HumanMessage, AIMessage

class ChatBotService:
    
    @staticmethod 
    async def createConversation(
        conversationID:str,
        conversationName:str,
        userID:int,
    ):
        
        return await prisma_connection.prisma.conversations.create({
            "id" : conversationID,
            "title":conversationName,
            "user_id":userID
        })
        
    @staticmethod
    async def saveResponse(
        question:str,
        response:str,
        chat_id:str
    ):
        return await prisma_connection.prisma.conversationsdata.create({
            "question":question,
            "response":response,
            "conversation_id":chat_id
        })
        
    @staticmethod
    async def findConversation(
        chat_id:str,
        user_id:int
    ):
        return await prisma_connection.prisma.conversations.find_first(
            where={
                "id":chat_id,
                "user_id":user_id
            }
        )
    
    @staticmethod
    async def getConversationData(chat_id: str):
        conversation_data = await prisma_connection.prisma.conversationsdata.find_many(
    where={"conversation_id": chat_id},
    take=10  
)
        
        if not conversation_data:
            return []
        else:
            formatted_data = []
            for item in conversation_data:
                formatted_data.append({"role": "user", "content": item.question})
                formatted_data.append({"role": "assistant", "content": item.response})

            return formatted_data
        
    @staticmethod
    async def getConversationDataForHistory(chat_id: str):
        count = await prisma_connection.prisma.conversationsdata.count(
            where={"conversation_id": chat_id},
        )
        if count <= 10:
            conversation_data = await prisma_connection.prisma.conversationsdata.find_many(
                where={"conversation_id": chat_id},
                
            )
        else:
            conversation_data = await prisma_connection.prisma.conversationsdata.find_many(
                where={"conversation_id": chat_id},
                skip= count-10
            )
            
        
        if not conversation_data:
            return []
        else:
            formatted_data = []
            for item in conversation_data:
                formatted_data.append(HumanMessage(content=item.question))
                formatted_data.append(AIMessage(content=item.response))

            return formatted_data
    
        
   

    
        
        
