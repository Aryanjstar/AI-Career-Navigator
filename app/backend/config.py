"""
Configuration management for AI Career Navigator
"""
import os
from typing import Optional


class Config:
    """Application configuration"""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1")
    AZURE_OPENAI_MODEL: str = os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    # Flask Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS Configuration
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    
    # Application Settings
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS: set = {'txt', 'pdf', 'doc', 'docx'}
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
        if not cls.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")
        return True

