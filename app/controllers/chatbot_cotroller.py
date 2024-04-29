import json
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
    
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
def person_details(name:str):
    return json.dumps({"name": "shivam", "age": "72", "unit": "unit"})

tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "person_details",
                "description": "get person details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "person's name",
                        }
                    }
                },
            },
        }
    ]
@router.post("/chat/functioncalling")
async def chat(chatData: ChatData, request: Request):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": chatData.question}],
        tools=tools,
        tool_choice="auto",
    )
    # print(response)
    messages = [{"role": "user", "content": "find details of shivam"}]
    response_message = response.choices[0].message
    messages.append(response_message)
    tool_calls = response_message.tool_calls
    # # Step 2: check if the model wanted to call a function
    if tool_calls:
    #     # Step 3: call the function
    #     # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
            "person_details": person_details
        }  # only one function in this example, but you can have multiple
    #     # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                # location=function_args.get("location"),
                # unit=function_args.get("unit"),
                name=function_args.get("name"),
                
            )
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            ) 
            print(messages)
                
    # #           # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )  # get a new response from the model where it can see the function response
    #     return {"response": second_response}
        return second_response
    # bot_response: str = bot