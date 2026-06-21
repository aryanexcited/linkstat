from pydantic_settings import BaseSettings

class settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = settings()
