from fastapi import APIRouter
from app.controllers.auth_controller import router as auth_router
from app.controllers.user_controller import router as user_router
from app.controllers.chatbot_cotroller import router as chat_bot_router
from app.controllers.user_data_controller import router as user_data_router


global_router = APIRouter(
    prefix="/api/v1",
)

global_router.include_router(auth_router)
global_router.include_router(user_router)
global_router.include_router(chat_bot_router)
global_router.include_router(user_data_router)


