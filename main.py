import uvicorn
from fastapi import FastAPI
from configs.database_connection import prisma_connection
from routes import global_router


def init_app():
    apps = FastAPI(
        title="ChatBot",
        description="Create ChatBot using FastApi and OpenAi.",
        version="1.0.0"
    )

    @apps.on_event("startup")
    async def startup():
        print("Server Started")
        await prisma_connection.connect()

    @apps.on_event("shutdown")
    async def shutdown():
        print("Server Stopped")
        await prisma_connection.disconnect()

    @apps.get('/')
    def home():
        return "welcome home!"
    
    apps.include_router(global_router)

    return apps


app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)