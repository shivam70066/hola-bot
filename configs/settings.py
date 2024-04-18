from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str = "none"
    OPEN_API_KEY : str = "none"
    

# Create an instance of the Settings model to load the environment variables
settings = Settings()