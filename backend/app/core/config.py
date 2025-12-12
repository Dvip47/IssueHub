
from pydantic_settings import BaseSettings


class Settings(BaseSettings):


    DATABASE_URL: str = "postgresql://user:password@localhost:5432/issuehub"
    PROJECT_NAME: str = "IssueHub"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
 
    SECRET_KEY: str = "Ca12f9b32e40b72c9f998a6a4VIPINLOHARaf9e947afa7c910fa3d8a4431a"
    ALGORITHM: str = "HS256"

    class Config: env_file = ".env"

settings = Settings()
