# core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    # Google Chat Configuration
    GOOGLE_PROJECT_ID: str
    GOOGLE_PRIVATE_KEY: str
    GOOGLE_CLIENT_EMAIL: str
    GOOGLE_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
    
    # Application Configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    load_dotenv()
    return Settings()