from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # API Configuration
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./lol_jungle_assistant.db"

    # Riot Games API
    RIOT_API_KEY: str = ""
    RIOT_BASE_URL: str = "https://americas.api.riotgames.com"

    # Claude API
    CLAUDE_API_KEY: str = ""
    CLAUDE_BASE_URL: str = "https://api.anthropic.com"

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS - Convertir string separado por comas a lista
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Usuario objetivo por defecto - AGREGADOS
    DEFAULT_USER_RIOT_ID: str = "Not Alet"
    DEFAULT_USER_TAG_LINE: str = "JCP"
    DEFAULT_USER_REGION: str = "las"

    @property
    def allowed_origins_list(self) -> List[str]:
        """Convertir ALLOWED_ORIGINS string a lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()