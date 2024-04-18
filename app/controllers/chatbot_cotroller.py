from fastapi import APIRouter,Request
from app.schemas.chatbot_schema import ChatData
from ..services.chatbot_services import ChatBotService
from openai import OpenAI
from fastapi import HTTPException
import uuid  
from configs.settings import settings
key= settings.OPEN_API_KEY
client = OpenAI(api_key=key)

router = APIRouter(
    prefix="/chatbot",
    tags=['chatbot']
)

@router.post("/chat")
async def chat(chatData: ChatData, request: Request):
    chat_id = ""
    if chatData.chat_id is None:
        chat_id = str(uuid.uuid4())
    else:
        chat_id = chatData.chat_id
        
    conversation_data = []
    if(chatData.chat_id is None):
        await ChatBotService.createConversation(
            chat_id,
            chatData.question,
            request.state.user_id
        )
    else:
        isConversationExists = await ChatBotService.findConversation(
            chat_id,
            request.state.user_id
        )
        if isConversationExists is None:
            raise HTTPException(status_code=404, detail="Invalid conversation ID.")
        
        conversation_data = await ChatBotService.getConversationData(
            chat_id
        )
    conversation_data.insert(0,{"role": "system", "content": "you are a helpfull AI Assistant your name is Roy and you are a math teacher,Your only task is to solve math quetions of users. if question is irrelevent then tell the user that you are only allowd to solve math questions."})
    conversation_data.append({"role": "user", "content": chatData.question})    
    
    bot = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= conversation_data
    )
    bot_response:str = bot.choices[0].message.content
    
    await ChatBotService.saveResponse(
            chatData.question,
            bot_response.strip(),
            chat_id
        )
        
    return {"chat_id":chat_id , "response": bot_response}

@router.post("/chat")
async def chat(chatData: ChatData, request: Request):
    chat_id = ""
    if chatData.chat_id is None:
        chat_id = str(uuid.uuid4())
    else:
        chat_id = chatData.chat_id
        
    conversation_data = []
    if(chatData.chat_id is None):
        await ChatBotService.createConversation(
            chat_id,
            chatData.question,
            request.state.user_id
        )
    else:
        isConversationExists = await ChatBotService.findConversation(
            chat_id,
            request.state.user_id
        )
        if isConversationExists is None:
            raise HTTPException(status_code=404, detail="Invalid conversation ID.")
        
        conversation_data = await ChatBotService.getConversationData(
            chat_id
        )
    conversation_data.insert(0,{"role": "system", "content": "you are a helpfull AI Assistant your name is Roy and you are not able to solve maths questions. if anyone asks you to solve or ask any maths question don't solve it or tell the answer"})
    conversation_data.append({"role": "user", "content": chatData.question})    
    
    bot = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= conversation_data
    )
    bot_response:str = bot.choices[0].message.content
    
    await ChatBotService.saveResponse(
            chatData.question,
            bot_response.strip(),
            chat_id
        )
        
    return {"chat_id":chat_id , "response": bot_response}
