"""
Application configuration using Pydantic Settings.

Loads configuration from environment variables defined in .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database - defaults to SQLite for local development
    DATABASE_URL: str = "sqlite:///./todo.db"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # OpenAI Integration
    OPENAI_API_KEY: str = ""

    # Qwen Integration
    QWEN_API_KEY: str = ""
    QWEN_API_BASE: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1" # Default to Alibaba Cloud
    QWEN_MODEL_NAME: str = "qwen-plus"
    
    # AI Model Selection
    AI_MODEL: str = "openai" # "openai" or "qwen"

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = (".env", "../.env")
        case_sensitive = True
        extra = "ignore"


settings = Settings()
