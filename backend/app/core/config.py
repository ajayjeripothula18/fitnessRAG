from pydantic import Field, model_validator
from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FitnessRAG"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_DB: str = Field(...)
    POSTGRES_SERVER: str = Field(...)
    POSTGRES_PORT: int = Field(5432)
    SQLALCHEMY_DATABASE_URL: str | None = Field(default=None, alias="DATABASE_URL")

    # CORS
    BACKEND_CORS_ORIGINS: List[Union[str, str]] = Field(default=["*"])

    # OpenAI
    OPENAI_API_KEY: str | None = None

    # Ollama
    OLLAMA_BASE_URL: str | None = Field(default=None)
    OLLAMA_MODEL: str = Field(...)
    OLLAMA_EMBEDDING_MODEL: str = Field(...)
    OLLAMA_TIMEOUT: float = Field(default=5.0)

    @model_validator(mode="after")
    def validate_llm_config(self) -> "Settings":
        if not self.OPENAI_API_KEY and not self.OLLAMA_BASE_URL:
            raise ValueError(
                "Either OPENAI_API_KEY or OLLAMA_BASE_URL must be configured."
            )
        return self

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


settings = Settings()  # type: ignore[call-arg]
