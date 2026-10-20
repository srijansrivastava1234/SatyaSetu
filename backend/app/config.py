import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = "SatyaSetu: TrustAI Misinformation Intelligence Engine"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_FACTCHECK_API_KEY: str = os.getenv("GOOGLE_FACTCHECK_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "satyasetu.db")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "127.0.0.1")

settings = Settings()
