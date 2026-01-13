from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str = "https://adiletai-openai.openai.azure.com/"
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-5-mini"
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # Cookie Settings
    COOKIE_DOMAIN: str = "localhost"
    COOKIE_SECURE: bool = False  # True in production
    COOKIE_SAMESITE: str = "lax"
    COOKIE_MAX_AGE_STANDARD: int = 604800      # 7 days
    COOKIE_MAX_AGE_REMEMBER: int = 2592000     # 30 days

    # CSRF Settings
    CSRF_SECRET_KEY: str
    CSRF_TOKEN_EXPIRE_MINUTES: int = 60

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 5

    # Token Expiry
    REFRESH_TOKEN_EXPIRE_DAYS_REMEMBER: int = 30  # Remember Me

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,muscleup://"

    # Environment
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


# Global settings instance
settings = Settings()
