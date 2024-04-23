from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import jwt
from configs.settings import settings

def register_auth_middleware(apps: FastAPI):
    @apps.middleware("http")
    async def auth_middlware(request: Request, call_next):
        
        path = request.url.path.split('/')
        if 'auth' in path or 'docs' in path or 'redoc' in path or 'openapi.json' in path or 'healthcheck' in path or 'user_data' in path:
            pass
        else:
            if not request.headers.get("authorization"):
                    return JSONResponse(
                        content={
                            "message": "Unauthorized"
                        },
                        status_code=403             
                    )
            token:str = request.headers['authorization'].split(' ')[1]
            try:
                data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
                request.state.user_id = data.get('data').get('id')
            except jwt.ExpiredSignatureError:
                return JSONResponse(
                        content={
                            "message": "Token Expired"
                        },
                        status_code=403               
                    )
            except jwt.InvalidTokenError:
                return JSONResponse(
                        content={
                            "message": "Invalid Token"
                        },
                        status_code=403               
                    )
               
        response = await call_next(request)
        
        return response