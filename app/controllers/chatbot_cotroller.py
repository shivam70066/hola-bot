from fastapi import APIRouter,Request
from app.schemas.chatbot_schema import ChatData
from ..services.chatbot_services import ChatBotService
from openai import OpenAI
from fastapi import HTTPException
from ..utils.retrieval_chain import retrieval_chain
import uuid  
from configs.settings import settings
from langchain_openai import OpenAIEmbeddings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage

output_parser = StrOutputParser()
key= settings.OPEN_API_KEY
client = OpenAI(api_key=key)

router = APIRouter(
    prefix="/chatbot",
    tags=['chatbot']
)

@router.post("/chat/v1")
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

@router.post("/chat/v2")
async def chat(chatData: ChatData, request: Request):
    chat_id = ""
    chat_history=[]
    if chatData.chat_id is None:
        chat_id = str(uuid.uuid4())
    else:
        chat_id = chatData.chat_id
        
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
        
        chat_history = await ChatBotService.getConversationDataForHistory(
            chat_id
        )
        
    # conversation_data.append({"role": "user", "content": chatData.question})
    # print(conversation_data)
    userID = request.state.user_id
    response = retrieval_chain(question=chatData.question,userID=userID,chat_history=chat_history) 
    
    await ChatBotService.saveResponse(
            chatData.question,
            response['answer'],
            chat_id
        )
    return {"response": response,"chat_id":chat_id}
    # return {"resp":"ee"}
    
        
    # return {"chat_id":chat_id , "response": bot_response}