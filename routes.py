from fastapi import APIRouter
from app.controllers.auth_controller import router as auth_router

global_router = APIRouter()

global_router.include_router(auth_router, prefix="/api/v1")